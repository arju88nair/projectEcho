
import importlib


from brain.skills.skill import AssistantSkill
from brain import settings
from brain.utils.mongoDB import db
from brain.enumerations import InputMode, MongoCollections
from brain.utils import console
from brain.utils import input

input_mode = db.get_documents(collection='general_settings')[0]['input_mode']
response_in_speech = db.get_documents(collection='general_settings')[0]['response_in_speech']
assistant_name = db.get_documents(collection='general_settings')[0]['assistant_name']


class ConfigurationSkills(AssistantSkill):

    @classmethod
    def configure_assistant(cls, **kwargs):

        console.print_console_header('Configure assistant')
        cls.console('NOTE: Current name: {0}'.format(assistant_name), refresh_console=False)
        console.headerize()
        cls.response('Set new assistant name: ', refresh_console=False)
        new_assistant_name = cls.user_input()

        console.headerize()

        cls.console('NOTE: Current mode: {0}'.format(input_mode), refresh_console=False)
        console.headerize()
        cls.response('Set new input mode (text or voice): ')
        input_mode_values = [mode.value for mode in InputMode]
        new_input_mode = input.validate_input_with_choices(available_choices=input_mode_values)

        console.headerize()
        cls.response('Do you want response in speech?', refresh_console=False)
        new_response_in_speech = input.check_input_to_continue()

        new_settings = {
            'assistant_name': new_assistant_name,
            'input_mode': new_input_mode,
            'response_in_speech': new_response_in_speech,
        }

        cls.console("\n The new settings are the following: \n", refresh_console=False)
        for setting_desc, value in new_settings.items():
            cls.console('* {0}: {1}'.format(setting_desc, value), refresh_console=False)

        cls.response('Do you want to save new settings? ', refresh_console=False)
        save = input.check_input_to_continue()
        if save:
            db.update_collection(collection=MongoCollections.GENERAL_SETTINGS.value, documents=[new_settings])

            import brain
            importlib.reload(brain)

