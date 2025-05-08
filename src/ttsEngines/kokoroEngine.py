from ttsEngines.ttsManager import AbstractTTSEngine
import numpy as np
import soundfile as sf
from kokoro import KPipeline


class KokoroTTS(AbstractTTSEngine):
    def __init__(
        self, lang_code: str = "a", voice: str = "af_heart", speed: float = 1.0
    ):
        """
        lang_code: Kokoro language code (e.g. 'a' = US English)
        voice: the specific voice identifier
        speed: playback speed multiplier
        """
        super().__init__()
        self.pipeline = KPipeline(lang_code=lang_code)
        self.voice = voice
        self.speed = speed
        # Kokoro always outputs at 24 kHz
        self.sample_rate = 24000

    def synthesize(self, text: str, output_path: str) -> None:
        """
        Generates speech for `text` and writes a single WAV file to `output_path`.
        """
        # Run the TTS pipeline, which yields chunks (graphemes, phonemes, audio)
        generator = self.pipeline(text, voice=self.voice, speed=self.speed)

        # Collect all audio chunks
        chunks = []
        for _, _, audio in generator:
            chunks.append(audio)

        if not chunks:
            raise RuntimeError("Kokoro generated no audio for input text!")

        # Concatenate and write out as one WAV
        full_audio = np.concatenate(chunks, axis=0)
        sf.write(output_path, full_audio, self.sample_rate)
