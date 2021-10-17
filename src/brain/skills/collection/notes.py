from brain.skills.skill import AssistantSkill


class NoteSkill(AssistantSkill):
    @classmethod
    def blah(cls, voice_transcript, **kwargs):
        print(voice_transcript)
        return "Fd"
