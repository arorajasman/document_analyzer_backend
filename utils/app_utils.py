class AppUtils:
    """Utils class for the project"""

    @staticmethod
    def get_system_prompt_text(content: str, conversation: str):
        """Returns the system prompt text"""
        text = content.format(conversation=conversation)
        return text
