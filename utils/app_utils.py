class AppUtils:
    """Utils class for the project"""

    @staticmethod
    def get_prompt_text(content: str, **kwargs):
        """Returns the system prompt text"""

        text = content.format(**kwargs)
        return text
