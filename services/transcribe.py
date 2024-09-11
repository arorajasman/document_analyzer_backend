from openai import OpenAI


openai_client = OpenAI(api_key="API_KEY", base_url="http://localhost:8000/v1/")


def generate_transcription():

    try:

        audio_file = open('audio_files/harvard.wav', 'rb')

        response = openai_client.audio.transcriptions.create(
            model="medium",
            file=audio_file,
            # response_format="verbose_json",
            # timestamp_granularities=['word']
        )

        transcription_data = response if isinstance(
            response, dict) else response.to_dict()

        return transcription_data

    except Exception as e:

        return {'error': str(e)}
