from faster_whisper import WhisperModel

model_size = 'small'

model = WhisperModel(model_size, device="cpu", compute_type='int8')


def generate_transcription():
    try:

        segments, info = model.transcribe('audio_files/harvard.wav', beam_size=5)

        combined_text = " ".join(segment.text for segment in segments)

        return {"text": combined_text}

    except Exception as e:
        return {"error": str(e)}
