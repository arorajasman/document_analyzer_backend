class AppUtils:
    """Utils class for the project"""

    @staticmethod
    def get_prompt_text(content: str, **kwargs):
        """Returns the system prompt text"""

        try:
            text = content.format(**kwargs)
            return text
        except KeyError as e:
            raise KeyError(f"Error: Missing key {e} in the format string.")
        except ValueError as e:
            raise ValueError(
                f"Error: Invalid format string or mismatch in arguments. {e}"
            )  # noqa
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
