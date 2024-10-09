import os
from openai import OpenAI
import assemblyai as aai
from flask_app import app

from services.llm_service import LLMService
from services.vectorstore_service import VectorStoreService

from utils.app_utils import AppUtils
from utils.app_constants import app_strings
from utils.llm_tools.retriver_tools import policy_retriver_tool

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # noqa
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser  # noqa
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import (  # noqa
    create_tool_calling_agent,
    AgentExecutor,
    create_openai_tools_agent,
    create_react_agent,
    create_openai_functions_agent,
)  # noqa
from langchain import hub  # noqa

from schemas.llm_schemas.requirements_schema import RequirementsResponseSchema
from schemas.llm_schemas.rankings_response_schema import RankingsResponseSchema
import time
import json


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
        """Method to get the audio transcription with dirization"""

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

            return summarization_response
        except Exception as e:
            print("error while generating the summary")
            print(str(e))
            raise e

    @staticmethod
    def generate_policy_ranking(summary):
        try:
            model = LLMService.get_gpt_model(model="gpt-4o-mini")
            # model = LLMService.get_gpt_model()

            data, isFilePresent = TranscribeSummary.check_json_file()

            if isFilePresent:
                time.sleep(3)
                return data

            # user requirements chain
            requirements_prompt = ChatPromptTemplate.from_template(
                # app_strings["generate_requirements_prompt"]
                app_strings["generate_requirements_prompt_v2"]
            )

            requirements_chain = (
                {"summary": RunnablePassthrough()}
                | requirements_prompt
                | model.with_structured_output(RequirementsResponseSchema)
            )

            requirements_response = requirements_chain.invoke(summary)  # noqa

            # retriver logic
            vector_store_service: VectorStoreService = app.config[
                "vectorstore_service"
            ]  # noqa

            retriver = vector_store_service.get_vector_store().as_retriever(
                search_kwargs={"k": 8}
            )

            parsed_retrived_docs = []
            ranking = None

            for cycle_number, requirement in enumerate(
                requirements_response["requirements"][0:5], start=1
            ):  # noqa
                temp_parsed_docs = []

                docs = retriver.invoke(requirement)

                for i, doc in enumerate(docs):
                    temp_parsed_docs.append(
                        {
                            "content": doc.page_content,
                            "policy_path": doc.metadata["source"],
                        }
                    )
                parsed_retrived_docs.append([i for i in temp_parsed_docs])

            # ranking chain
            ranking_prompt = ChatPromptTemplate.from_template(
                # app_strings["generate_ranking_prompt"]
                app_strings["policy_ranking"]
            )

            ranking_chain = ranking_prompt | model.with_structured_output(  # noqa
                RankingsResponseSchema
            )  # noqa

            current_ranking = ranking_chain.invoke(
                {
                    "conversation": summary,
                    "policy_documents": str(parsed_retrived_docs),
                    "existing_policy_ranking": str(ranking),
                }  # noqa
            )
            ranking = current_ranking

            TranscribeSummary.store_data_in_file(
                "./assets/policy.json", "w+", ranking
            )  # noqa

            return ranking
        except Exception as e:
            print("error while generating the summary")
            print(str(e))
            raise e

    @staticmethod
    def check_json_file(file_path="./assets/policy.json"):
        # check if the fact_sheet.json file exists
        if os.path.exists(file_path):
            # check if the data with fact_sheets key exists in json file
            with open(file_path, "r") as f:
                data = json.load(f)
                if "policy_rankings" in data:
                    return (data, True)
                else:
                    return ({}, False)
        else:
            return ({}, False)

    @staticmethod
    def store_data_in_file(file_path: str, mode: str, data: any):
        """
        Parameters:
        ----------
        mode (str): mode to open the file, 'w' for write, 'w+' to first create the
        file and then write to it if the file does not exists
        """

        # creating json
        fact_sheet_json_object = json.dumps(data, indent=4)

        # storing json in file
        with open(file_path, mode) as jsonFile:
            jsonFile.write(fact_sheet_json_object)
            print("data stored successfully")
            return True

    @staticmethod
    def generate_policy_agent(summary):
        try:
            model = LLMService.get_gpt_model()

            # retriver logic
            vector_store_service: VectorStoreService = app.config[
                "vectorstore_service"
            ]  # noqa

            retriver = vector_store_service.get_vector_store().as_retriever(
                search_kwargs={"k": 5}
            )

            policy_retriver = policy_retriver_tool(retriver=retriver)

            tools = [policy_retriver]

            prompt = hub.pull("hwchase17/openai-functions-agent")

            agent = create_openai_functions_agent(
                llm=model, prompt=prompt, tools=tools
            )  # noqa

            agent_executor = AgentExecutor(
                agent=agent, tools=tools, verbose=True, return_intermediate_steps=True
            )  # noqa

            agent_response = agent_executor.invoke({"input": {summary}})

            print(agent_response)
            return agent_response
        except Exception as e:
            print("error while generating the summary")
            print(str(e))
            raise e
