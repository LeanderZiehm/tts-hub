from ttsEngines.ttsManager import AbstractTTSEngine
import os


# Concrete gTTS implementation
class GTTSTTS(AbstractTTSEngine):
    def synthesize(self, text: str, output_path: str) -> None:
        from gtts import gTTS

        tts = gTTS(text)
        # gTTS outputs MP3 by default; convert to WAV if needed
        mp3_path = output_path.replace(".wav", ".mp3")
        tts.save(mp3_path)
        # Convert MP3 to WAV using ffmpeg
        import subprocess

        subprocess.run(["ffmpeg", "-y", "-i", mp3_path, output_path], check=True)
        os.remove(mp3_path)
