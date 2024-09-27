from langchain_openai import ChatOpenAI


class LLMService:

    @staticmethod
    def get_gpt_model(model="gpt-3.5-turbo"):
        return ChatOpenAI(model=model)
