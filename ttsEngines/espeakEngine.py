from ttsEngines.ttsManager import AbstractTTSEngine


# Concrete Espeak implementation
class EspeakTTS(AbstractTTSEngine):
    def synthesize(self, text: str, output_path: str) -> None:
        # Uses the espeak command-line tool to generate WAV audio
        import subprocess

        subprocess.run(["espeak", "-w", output_path, text], check=True)
