import os
from openai import OpenAI
import assemblyai as aai

from utils.app_utils import AppUtils
from utils.app_constants import app_strings


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
