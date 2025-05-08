# from ttsEngines.ttsManager import AbstractTTSEngine
# from TTS.api import TTS
# import os


# # Concrete implementation using Coqui TTS
# class CoquiTTSEngine(AbstractTTSEngine):
#     def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
#         # Load the TTS model only once
#         self.tts_model = TTS(model_name=model_name)

#     def synthesize(self, text: str, output_path: str) -> None:
#         # Generate speech and save to file
#         self.tts_model.tts_to_file(text=text, file_path=output_path)
