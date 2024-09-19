import os
from faster_whisper import WhisperModel
from pyannote.audio import Pipeline


def generate_transcription(audio_file="audio_files/policy_conv.mp3"):
    try:
        model_size = "small"
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=os.getenv("HUGGING_FACE_API_KEY"),
        )
        segments, info = model.transcribe(audio_file, beam_size=5)

        diarization = diarization_pipeline(audio_file)

        speaker_turns = [
            (turn.start, turn.end, speaker)
            for turn, _, speaker in diarization.itertracks(yield_label=True)
        ]

        result = []

        for segment in segments:
            matching_speaker = next(
                (
                    speaker
                    for start, end, speaker in speaker_turns
                    if start <= segment.start <= end
                    or start <= segment.end <= end  # noqa
                ),
                "Unknown",
            )

            result.append(f"{matching_speaker}: {segment.text.strip()}")

        combined_text = " ".join(result)

        return {"text": combined_text}

    except Exception as e:
        return {"error": str(e)}
