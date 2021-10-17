from brain.skills.skill import AssistantSkill
import re


class NoteSkill(AssistantSkill):
    @classmethod
    def blah(cls, voice_transcript, skill):
        tags = cls.extract_tags(voice_transcript, skill['tags'])
        print(voice_transcript)
        print(tags)
        only_text_pattern = '([a-zA-Z]+)'
        for tag in tags:
            reg_ex = re.search(tag + ' ' + only_text_pattern, voice_transcript)
            print(reg_ex)
            print("sda")
            if reg_ex:
                topic = reg_ex.group(1)
                print(topic)
