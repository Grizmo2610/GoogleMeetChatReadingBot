from gtts import gTTS
from gtts.lang import tts_langs
import os
import pygame

from pydub import AudioSegment

import time
from enum import Enum
import re

pygame.mixer.init()

class STATUS(Enum):
    NOTHING = 0
    CHANGE = 1
    INVALID = 2


def has_text(content: str) -> bool:
    return bool(re.search(r'\w', content))

def replace_special_chars(content: str) -> str:
    special_chars = {
        "@": "a còng",
        "#": "thăng",
        "$": "đô la",
        "%": "phần trăm",
        "^": "mũ",
        "&": "và",
        "*": "sao",
        "!": "chấm than",
        "?": "hỏi chấm",
        ":": "Hai chấm",
        "=": "Bằng",
        ")": "Đóng ngoặc",
        "(": "mở ngoặc"
        
    }
    for char, replacement in special_chars.items():
        content = content.replace(char, replacement)
    return content

class GoogleTextToSpeechModel:
    def __init__(self, lang: str = "vi", remove_audio: bool = True, speed: float = 1.0):
        self.config = {
            "REMOVE": remove_audio,
            "SPEED": max(0.5, min(2.0, float(speed))),
            "LANG": lang if lang in tts_langs() else "vi",
        }
        if not os.path.exists("data/voices/"):
            os.makedirs("data/voices/")
        self.PATH = "data/voices/audio.mp3"

    def config_voice(self, new_config: dict):
        status = {k: STATUS.NOTHING for k in self.config}
        for key, value in new_config.items():
            if key in self.config and self.config[key] != value:
                self.config[key] = value
                status[key] = STATUS.CHANGE
            elif key not in self.config:
                status[key] = STATUS.INVALID
        return status

    def __text_to_speech(self, text: str):
        if not has_text(text):
            text = replace_special_chars(text)
        try:
            tts = gTTS(text=text, lang=self.config["LANG"], timeout=(60, 120))
        except Exception as E:
            tts = gTTS(text='Error', lang=self.config["LANG"], timeout=(60, 120), tokenizer_func=None)
            
        if self.config["REMOVE"]:
            path = self.PATH
        else:
            path = f"data/voices/sound_{int(time.time())}.mp3"

        tts.save(path)
        try:
            if self.config["SPEED"] != 1.0:
                audio = AudioSegment.from_file(path)
                audio = audio.speedup(playback_speed=self.config["SPEED"])
                new_path = "new_audio.mp3"
                audio.export(new_path, format="mp3")
                if self.config["REMOVE"] and os.path.exists(path):
                    os.remove(path)
                path = new_path
        except Exception as E:
            pass
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as E:
            print(E)
        finally:
            pygame.mixer.music.unload()

        if os.path.exists(path):
            os.remove(path)

    def speech(self, text: str):
        self.__text_to_speech(text)
