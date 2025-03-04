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
    """Enum representing different statuses of configuration changes."""
    NORMAL = 0   # Normal operation
    NOTHING = 1  # No change
    CHANGE = 2   # Configuration changed
    INVALID = 3  # Invalid configuration
    ERROR = -1   # Error occurred
    

def has_text(content: str) -> bool:
    """
    Check if the content contains any alphanumeric character.
    
    Args:
        content (str): The input text.
    
    Returns:
        bool: True if content contains at least one alphanumeric character, otherwise False.
    """
    return bool(re.search(r'\w', content))

def replace_special_chars(content: str) -> str:
    """
    Replace special characters with their corresponding spoken words in Vietnamese.
    
    Args:
        content (str): The input text containing special characters.
    
    Returns:
        str: The text with special characters replaced by their spoken equivalents.
    """
    special_chars = {
        "@": "a còng", "#": "thăng", "$": "đô la", "%": "phần trăm",
        "^": "mũ", "&": "và", "*": "sao", "!": "chấm than", "?": "hỏi chấm",
        ":": "hai chấm", "=": "bằng", ")": "đóng ngoặc", "(": "mở ngoặc"
    }
    for char, replacement in special_chars.items():
        content = content.replace(char, replacement)
    return content

class GoogleTextToSpeechModel:
    """A text-to-speech (TTS) model using Google TTS."""
    
    def __init__(self, lang: str = "vi", remove_audio: bool = True, speed: float = 1.0) -> None:
        """
        Initialize the TTS model with language, audio removal option, and playback speed.
        
        Args:
            lang (str): Language for the speech (default: "vi").
            remove_audio (bool): Whether to remove the audio file after playing (default: True).
            speed (float): Playback speed, constrained between 0.5x and 2.0x (default: 1.0).
        """
        self.config = {
            "REMOVE": remove_audio,
            "SPEED": max(0.5, min(2.0, float(speed))),  # Limit speed between 0.5x and 2.0x
            "LANG": lang if lang in tts_langs() else "vi",  # Default to Vietnamese if invalid
        }
        os.makedirs("data/voices/", exist_ok=True)
        self.PATH = "data/voices/audio.mp3"

    def config_voice(self, new_config: dict) -> dict:
        """
        Update voice configuration and return the status of each change.
        
        Args:
            new_config (dict): Dictionary containing new configuration values.
        
        Returns:
            dict: Status of each configuration key (STATUS.NOTHING, STATUS.CHANGE, STATUS.INVALID).
        """
        status = {k: STATUS.NOTHING for k in self.config}
        for key, value in new_config.items():
            if key in self.config and self.config[key] != value:
                self.config[key] = value
                status[key] = STATUS.CHANGE
            elif key not in self.config:
                status[key] = STATUS.INVALID
        return status

    def __text_to_speech(self, text: str) -> list[dict]:
        """
        Convert text to speech and play the generated audio.
        
        Args:
            text (str): The input text to be converted into speech.
        
        Returns:
            list[dict]: A list of status messages describing each step of the process.
        """
        messages = []

        if not has_text(text):
            text = replace_special_chars(text)
            messages.append({'status': STATUS.NORMAL, 'message': 'Replaced special characters with Vietnamese words.'})

        try:
            tts = gTTS(text=text, lang=self.config["LANG"], timeout=(60, 120))
            messages.append({'status': STATUS.NORMAL, 'message': 'Text converted to speech successfully.'})
        except Exception as e:
            tts = gTTS(text='Error', lang=self.config["LANG"], timeout=(60, 120), tokenizer_func=None)
            messages.append({'status': STATUS.ERROR, 'message': f'Error in text-to-speech conversion: {e}'})
        
        try:
            if self.config["REMOVE"]:
                path = self.PATH
            else:
                path = f"data/voices/sound_{int(time.time())}.mp3"

            tts.save(path)
            messages.append({'status': STATUS.NORMAL, 'message': f'Audio file saved at: {path}'})
        except Exception as e:
            messages.append({'status': STATUS.ERROR, 'message': f'Error saving audio file: {e}'})
            return messages

        # Adjust speed if necessary
        if self.config["SPEED"] != 1.0:
            try:
                audio = AudioSegment.from_file(path)
                audio = audio.speedup(playback_speed=self.config["SPEED"])
                new_path = "data/voices/new_audio.mp3"
                audio.export(new_path, format="mp3")
                messages.append({'status': STATUS.NORMAL, 'message': f'Audio speed adjusted to {self.config["SPEED"]}x, saved at: {new_path}'})

                if self.config["REMOVE"] and os.path.exists(path):
                    os.remove(path)
                    messages.append({'status': STATUS.NORMAL, 'message': f'Removed temporary file: {path}'})

                path = new_path
            except Exception as e:
                messages.append({'status': STATUS.ERROR, 'message': f'Error adjusting audio speed: {e}'})

        # Play the generated audio
        try:
            pygame.mixer.music.load(path)
            messages.append({'status': STATUS.NORMAL, 'message': f'Loaded audio file: {path}'})
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            messages.append({'status': STATUS.NORMAL, 'message': 'Audio playback completed.'})
        except Exception as e:
            messages.append({'status': STATUS.ERROR, 'message': f'Error playing audio file: {e}'})
        finally:
            pygame.mixer.music.unload()
            messages.append({'status': STATUS.NORMAL, 'message': 'Released audio file from memory.'})

            if os.path.exists(path):
                os.remove(path)
                messages.append({'status': STATUS.NORMAL, 'message': f'Deleted audio file: {path}'})
            else:
                messages.append({'status': STATUS.ERROR, 'message': f'File not found: {path}'})

        return messages
    
    def speech(self, text: str) -> list[dict]:
        """
        Convert text to speech and play the generated audio.
        
        Args:
            text (str): The input text to be spoken.
        
        Returns:
            list[dict]: Status messages describing the process.
        """
        return self.__text_to_speech(text)
