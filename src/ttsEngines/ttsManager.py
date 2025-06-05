from abc import ABC, abstractmethod


# Abstract TTS interface
class AbstractTTSEngine(ABC):
    @abstractmethod
    def synthesize(self, text: str, output_path: str) -> None:
        """
        Synthesize speech from text and save to output_path (WAV format).
        """
        pass


# from ttsEngines.gttsEngine import GTTSTTS
from ttsEngines.espeakEngine import EspeakTTS
# from ttsEngines.piperEngine import PiperTTS
# from ttsEngines.kokoroEngine import KokoroTTS


def get_tts_engines():
    print("Available TTS engines:")
    # for name, engine in get_available_engines().items():
    # print(f"- {name}: {engine.__doc__}")
    """
    Returns a dictionary of available TTS engines.
    """
    return {
        "espeak": EspeakTTS,
        # "gtts": GTTSTTS,
        # "piper": PiperTTS,
        # "kokoro": KokoroTTS,
    }
