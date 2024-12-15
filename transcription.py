import subprocess
from io import BytesIO
import numpy as np
import whisper
from scipy.io import wavfile

def transcribe_audio(audio_bytes):
    try:
        process = subprocess.run(
            [
                "ffmpeg", "-i", "pipe:0", "-ar", "16000", "-ac", "1", "-f", "wav", "pipe:1"
            ],
            input=audio_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        wav_data = BytesIO(process.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al convertir el archivo de audio: {e.stderr.decode('utf-8')}")
        raise

    wav_data.seek(0)
    sample_rate, audio_np = wavfile.read(wav_data)

    if audio_np.dtype == np.int16:
        audio_np = audio_np.astype(np.float32) / 32768.0

    model = whisper.load_model("base")
    transcription = model.transcribe(audio_np, language="Spanish", fp16=False)

    return transcription['text']