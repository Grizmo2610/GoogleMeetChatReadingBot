from gtts import gTTS
from gtts.lang import tts_langs
import os
import pygame
from pydub import AudioSegment
import time
import re
from enum import Enum

# Initialize pygame mixer
pygame.mixer.init()

class STATUS(Enum):
    NOTHING = 0
    CHANGE = 1
    INVALID = 2

def has_text(content: str) -> bool:
    """Check if the content contains any alphanumeric character."""
    return bool(re.search(r'\w', content))

def replace_special_chars(content: str) -> str:
    """Replace special characters with their corresponding spoken words in Vietnamese."""
    special_chars = {
        "@": "a còng", "#": "thăng", "$": "đô la", "%": "phần trăm",
        "^": "mũ", "&": "và", "*": "sao", "!": "chấm than", "?": "hỏi chấm",
        ":": "Hai chấm", "=": "Bằng", ")": "Đóng ngoặc", "(": "mở ngoặc"
    }
    for char, replacement in special_chars.items():
        content = content.replace(char, replacement)
    return content

class GoogleTextToSpeechModel:
    def __init__(self, lang: str = "vi", remove_audio: bool = True, speed: float = 1.0):
        """Initialize TTS model with language, audio removal option, and playback speed."""
        self.config = {
            "REMOVE": remove_audio,
            "SPEED": max(0.5, min(2.0, float(speed))),  # Constrain speed between 0.5x and 2.0x
            "LANG": lang if lang in tts_langs() else "vi",  # Default to Vietnamese if invalid
        }
        os.makedirs("data/voices/", exist_ok=True)
        self.PATH = "data/voices/audio.mp3"

    def config_voice(self, new_config: dict):
        """Update voice configuration and return status of each config change."""
        status = {k: STATUS.NOTHING for k in self.config}
        for key, value in new_config.items():
            if key in self.config and self.config[key] != value:
                self.config[key] = value
                status[key] = STATUS.CHANGE
            elif key not in self.config:
                status[key] = STATUS.INVALID
        return status

    def __text_to_speech(self, text: str):
        """Convert text to speech and play the generated audio."""
        if not has_text(text):
            text = replace_special_chars(text)
        
        try:
            tts = gTTS(text=text, lang=self.config["LANG"], timeout=(60, 120))
        except Exception:
            tts = gTTS(text='Error', lang=self.config["LANG"], timeout=(60, 120), tokenizer_func=None)
        
        path = self.PATH if self.config["REMOVE"] else f"data/voices/sound_{int(time.time())}.mp3"
        tts.save(path)
        
        # Adjust speed if necessary
        try:
            if self.config["SPEED"] != 1.0:
                audio = AudioSegment.from_file(path)
                audio = audio.speedup(playback_speed=self.config["SPEED"])
                new_path = "new_audio.mp3"
                audio.export(new_path, format="mp3")
                if self.config["REMOVE"] and os.path.exists(path):
                    os.remove(path)
                path = new_path
        except Exception:
            pass
        
        # Play the generated audio
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(e)
        finally:
            pygame.mixer.music.unload()
            if os.path.exists(path):
                os.remove(path)
    
    def speech(self, text: str):
        """Public method to convert text to speech."""
        self.__text_to_speech(text)
