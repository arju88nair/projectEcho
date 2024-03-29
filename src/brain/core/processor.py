

import brain

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from brain.skills.analyzer import SkillAnalyzer
from brain.skills.registry import skill_objects
from brain.core.nlp import ResponseCreator
from brain.skills.collection.activation import ActivationSkills
from brain.utils.mongoDB import db
from brain.skills.collection.wolframalpha import WolframSkills


class Processor:
    def __init__(self, console_manager, settings_):
        self.console_manager = console_manager
        self.settings = settings_
        self.response_creator = ResponseCreator()
        self.skill_analyzer = SkillAnalyzer(
            weight_measure=TfidfVectorizer,
            similarity_measure=cosine_similarity,
            args=self.settings.SKILL_ANALYZER.get('args'),
            sensitivity=self.settings.SKILL_ANALYZER.get('sensitivity'),
        )

    def run(self):
        """
         Assistant starting point.

        - STEP 1: Get user input based on the input mode (voice or text)
        - STEP 2: Matches the input with a skill
        - STEP 3: Create a response
        - STEP 4: Execute matched skill
        - STEP 5: Insert user transcript and response in history collection (in MongoDB)

        """

        transcript = brain.input_engine.recognize_input()
        skill = self.skill_analyzer.extract(transcript)

        if skill:
            # ----------------------------------------------------------------------------------------------------------
            # Successfully extracted skill
            # ----------------------------------------------------------------------------------------------------------

            # ---------------
            # Positive answer
            # ---------------
            response = self.response_creator.create_positive_response(transcript)
            brain.output_engine.assistant_response(response)

            # ---------------
            # Skill execution
            # ---------------
            skill_to_execute = {'voice_transcript': transcript, 'skill': skill}
            self._execute_skill(skill_to_execute)

        else:
            # ----------------------------------------------------------------------------------------------------------
            # No skill extracted
            # ----------------------------------------------------------------------------------------------------------

            # ---------------
            # Negative answer
            # ---------------
            response = self.response_creator.create_negative_response(transcript)
            brain.output_engine.assistant_response(response)

            # ---------------
            # WolframAlpha API Call
            # ---------------
            skill_to_execute = {'voice_transcript': transcript,
                                'skill': {'name': WolframSkills.call_wolframalpha.__name__}
                                }

            response = WolframSkills.call_wolframalpha(transcript)

        # --------------------------------------------------------------------------------------------------------------
        # Add new record to history
        # --------------------------------------------------------------------------------------------------------------

        record = {'user_transcript': transcript,
                  'response': response if response else '--',
                  'executed_skill': skill_to_execute if skill_to_execute else '--'
                  }

        db.insert_many_documents('history', [record])

    def _execute_skill(self, skill):
        if skill:
            skill_func_name = skill.get('skill').get('func')
            self.console_manager.console_output(info_log='Executing skill {0}'.format(skill_func_name))
            try:
                ActivationSkills.enable_assistant()
                skill_func_name = skill.get('skill').get('func')
                skill_func = skill_objects[skill_func_name]
                skill_func(**skill)
            except Exception as e:
                self.console_manager.console_output(error_log="Failed to execute skill {0} with message: {1}"
                                                    .format(skill_func_name, e))
