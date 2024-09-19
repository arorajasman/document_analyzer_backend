import os
from openai import OpenAI
import assemblyai as aai
from flask_app import app

from services.llm_service import LLMService
from services.vectorstore_service import VectorStoreService

from utils.app_utils import AppUtils
from utils.app_constants import app_strings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser # noqa
from langchain_core.runnables import RunnablePassthrough

from schemas.llm_schemas.requirements_schema import RequirementsResponseSchema
from schemas.llm_schemas.rankings_response_schema import RankingsResponseSchema


class TranscribeSummary:

    @staticmethod
    def generate_transcription(audio_file: str):
        """Method for audio transcription"""

        try:
            return TranscribeSummary().get_transcription_with_assembly_ai(
                audio_file
            )  # noqa
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def generate_summary(prompt_data):
        client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
        response_data = client.chat.completions.create(
            model="gpt-3.5-turbo",
            stream=False,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": AppUtils.get_prompt_text(
                                app_strings["summarization_prompt"],
                                conversation=prompt_data,
                            ),
                        }
                    ],
                },
            ],
        )
        return response_data.choices[0].message.content

    def generate_requirements(summary):
        client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))
        response_data = client.chat.completions.create(
            model="gpt-3.5-turbo",
            stream=False,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": AppUtils.get_prompt_text(
                                app_strings["generate_requirements_prompt"],
                                summary=summary,
                            ),
                        }
                    ],
                },
            ],
        )
        return response_data.choices[0].message.content

    def get_transcription_with_assembly_ai(self, file_url: str):
        try:
            aai.settings.api_key = os.getenv("ASSEMBLY_AI_API_KEY")
            config = aai.TranscriptionConfig(speaker_labels=True)
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(file_url, config=config)
            result = []
            for utterance in transcript.utterances:
                result.append(f"{utterance.speaker}: {utterance.text}")
            combined_text = " ".join(result)
            return {"transcript": combined_text}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def generate_summary_v2(prompt_data):
        try:
            model = LLMService.get_gpt_model()

            # summarization chain
            summarization_prompt = ChatPromptTemplate.from_template(
                app_strings["summarization_prompt"]
            )

            output_parser = StrOutputParser()

            summarization_chain = (
                {"conversation": RunnablePassthrough()}
                | summarization_prompt
                | model
                | output_parser
            )

            summarization_response = summarization_chain.invoke(prompt_data)

            # user requirements chain
            requirements_prompt = ChatPromptTemplate.from_template(
                app_strings["generate_requirements_prompt"]
            )

            requirements_chain = (
                {"summary": RunnablePassthrough()}
                | requirements_prompt
                | model.with_structured_output(RequirementsResponseSchema)
            )

            requirements_response = requirements_chain.invoke(
                summarization_response
            )  # noqa

            # retriver logic
            vector_store_service: VectorStoreService = app.config["vectorstore_service"]  # noqa

            retriver = vector_store_service.get_vector_store().as_retriever()

            parsed_retrived_docs = []

            for requirement in requirements_response["requirements"]:
                docs = retriver.invoke(requirement)
                for i, doc in enumerate(docs):
                    parsed_retrived_docs.append({
                        "content": doc.page_content,
                        "policy_name": doc.metadata["source"]
                    })

            # ranking chain
            ranking_prompt = ChatPromptTemplate.from_template(
                app_strings["generate_ranking_prompt"]
            )

            ranking_chain = (
               ranking_prompt | model.with_structured_output(RankingsResponseSchema) # noqa
            )

            ranking_response = ranking_chain.invoke({
                "conversation": summarization_response,
                "policy_documents": str(parsed_retrived_docs)
            })

            return (
                summarization_response,
                requirements_response,
                parsed_retrived_docs,
                ranking_response
            )
        except Exception as e:
            print("error while generating the summary")
            print(str(e))
            raise e
