from ttsEngines.ttsManager import AbstractTTSEngine
import os
import tempfile
import subprocess


class PiperTTS(AbstractTTSEngine):
    """
    Concrete Piper TTS implementation.

    Args:
        model_path (str): Path to the Piper ONNX model file.
        piper_binary (str): Path to the Piper executable. Defaults to "ttsEngines/piper/piper".
    """

    def __init__(self, model_path: str, piper_binary: str = "ttsEngines/piper/piper"):
        self.model_path = model_path
        self.piper_binary = piper_binary

    def synthesize(self, text: str, output_path: str) -> None:
        """
        Synthesize speech from text and save as a WAV file.

        This method uses the Piper TTS engine to generate raw PCM audio,
        then converts it to a WAV file via ffmpeg.

        Args:
            text (str): Input text to synthesize.
            output_path (str): Path where the output WAV will be saved.
        """
        # Create a temporary text file for Piper input
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt") as txt_file:
            txt_file.write(text)
            txt_path = txt_file.name

        # Define temporary raw output path
        raw_path = output_path.replace(".wav", ".raw")

        # Run Piper to generate raw PCM data
        subprocess.run(
            [
                self.piper_binary,
                "--model",
                self.model_path,
                "--text",
                txt_path,
                "--output-raw",
                raw_path,
            ],
            check=True,
        )

        # Convert raw PCM to WAV using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "s16le",
                "-ar",
                "22050",
                "-ac",
                "1",
                "-i",
                raw_path,
                output_path,
            ],
            check=True,
        )

        # Cleanup temporary files
        os.remove(txt_path)
        os.remove(raw_path)
