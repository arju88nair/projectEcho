

import sys
import time
from datetime import datetime

from brain.skills.skill import AssistantSkill
from brain.utils.startup import play_activation_sound
from brain.utils.mongoDB import db
from brain.enumerations import InputMode, MongoCollections


class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, **kwargs):
        """
        Plays activation sound and creates the assistant response according to the day hour.
        """

        input_mode = db.get_documents(collection=MongoCollections.GENERAL_SETTINGS.value)[0]['input_mode']
        if input_mode == InputMode.VOICE.value:
            play_activation_sound()

    @classmethod
    def disable_assistant(cls, **kwargs):
        """
        - Clear console
        - Shutdown the assistant service
        """

        cls.response('Bye')
        time.sleep(1)
        cls.console(info_log='Application terminated gracefully.')
        sys.exit()

    @classmethod
    def assistant_greeting(cls, **kwargs):
        """
        Assistant greeting based on day hour.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            cls.response('Good morning sir')
        elif 12 <= day_time < 18:
            cls.response('Good afternoon sir')
        else:
            cls.response('Good evening sir')
