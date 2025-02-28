from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import gc
import os
# import pyttsx3
import json
import time
from time import sleep
import logging
import logging.config

from Models.Gemini import GeminiTranscript
from CustomExeption.CustomExeption import *
from Models.VoiceModel import GoogleTextToSpeechModel as Engine
from Models.VoiceModel import STATUS
from typing import List, Tuple, Optional

if not os.path.exists('log'):
    os.makedirs('log')
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"log/AI{int(time.time())}.log", encoding="utf-8")])

logging.info("Starting program!")

def reading_config(path: str = 'configurations/config.json'):
    try:
        logging.info("Reading configuration file")
        with open(path, 'r') as f:
            config = json.load(f)
        logging.info("Configuration file loaded successfully")
    except FileNotFoundError:
        logging.warning("Config file not found! Initializing default config")
        norm_path = os.path.normpath(path)
        dir_path = os.path.dirname(norm_path)
        if dir_path:
            os.makedirs(dir_path)
        config = {
            "PATH": "audio.mp3",
            "REMOVE": True,
            "SPEED": 1.0,
            "LANG": "vi"
            }
        
        with open(path, 'w') as f:
            json.dump(config, f, indent=4)
        logging.info("Default configuration file created")
    return config

def verify(credentials_path: str = 'data/credentials.json'):
    try:
        logging.info("Loading credentials file")
        with open(credentials_path, "r") as f:
            account: dict = json.load(f)
        logging.info("Credentials file loaded successfully")
    except FileNotFoundError as FFE:
        logging.error("Credentials file does not exist!")
        raise FFE  # Stop execution if credentials file is missing
    return account

class VoiceAI:
    def __init__(self, driver: WebDriver,
                 config_path: str = 'data/config.json',
                 credentials_path: str = 'data/credentials.json'):

        self.driver = driver
        logging.info("WebDriver initialized")
        self.account = verify(credentials_path)
        # self.engine = pyttsx3.init()
        self.engine = Engine('vi')
        self.gemini_model = GeminiTranscript()
        self.config_path = config_path

    def config_chatbot(self):
        config = reading_config(self.config_path)
        try:
            status = self.engine.config_voice(config)
            for k, v in status.items():
                if v == STATUS.CHANGE:
                    logging.info(f"{k} set to: {config[k]}")
                elif v == STATUS.INVALID:
                    logging.info(f"{k}Is not a valid key, config failed")
        except KeyError as e:
            logging.info("Invalid config setting")

    def join_meeting(self):
        self.__login()
        self.__join_meeting()

    def __login(self) -> None:
        logging.info("Starting Google login process")
        self.driver.get("https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ")

        try:
            self.driver.find_element(By.ID, "identifierId").send_keys(self.account['email'])
            self.driver.find_element(By.ID, "identifierNext").click()
            logging.info("Email entered and proceeding to password input")

            self.driver.implicitly_wait(10)
            self.driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.account['password'])
            self.driver.find_element(By.ID, "passwordNext").click()
            logging.info("Password entered and login submitted")

            self.driver.implicitly_wait(10)
            self.driver.get("https://accounts.google.com/")
            logging.info("Google login successful")
        except Exception as e:
            logging.error(f"Login failed: {e}")
            raise e

    def __turnOffMicCam(self) -> None:
        logging.info("Attempting to turn off microphone and camera")
        wait = WebDriverWait(self.driver, 10)
        sleep(2)

        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Tắt micrô']")))
            button.click()
            logging.info("Microphone turned off")
        except Exception as e:
            logging.warning("Microphone button not found:", e)

        sleep(1)
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Tắt máy ảnh']")))
            button.click()
            logging.info("Camera turned off")
        except Exception as e:
            logging.warning("Camera button not found!", e)

        try:
            button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "XCoPyb")))
            button.click()
            logging.info("Joining the Meeting room")
        except Exception as e:
            logging.error("Failed to join meeting room", e)

    def __join_meeting(self) -> None:
        logging.info(f"Joining Google Meet with link: {self.account['meeting_link']}")
        self.driver.get(self.account['meeting_link'])
        
        sleep(0.5)
        
        self.driver.get(self.account['meeting_link'])

        self.__turnOffMicCam()

        wait = WebDriverWait(self.driver, 10)
        try:
            alert = self.driver.switch_to.alert
            logging.info(f"Popup found: {alert.text}")
            alert.dismiss()
        except Exception as e:
            logging.info("No popup found")

        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div[36]/div[4]/div[10]/div/div/div[3]/nav/div[3]/div')))
            button.click()
            logging.info("Clicked on join button")
        except Exception as e:
            logging.warning("Join button not found", e)

    def get_chat_messages(self) -> List[Tuple[str, str, str, str]]:
        logging.info("Fetching chat messages from Google Meet")
        chat_data: List[Tuple[str, str, str, str]] = []

        messages = self.driver.find_elements(By.CSS_SELECTOR, ".Ss4fHf")

        for msg in messages:
            try:
                name: str = msg.find_element(By.CSS_SELECTOR, ".poVWob").text.strip()
                timestamp: str = msg.find_element(By.CSS_SELECTOR, ".MuzmKe").text.strip()

                msg_elements = msg.find_elements(By.CSS_SELECTOR, '[jsname="dTKtvb"]')
                for msg_element in msg_elements:
                    parent_msg = msg_element.find_element(By.XPATH, "./ancestor::div[@data-message-id]")
                    message_id = parent_msg.get_attribute("data-message-id") if parent_msg else None
                    text: str = msg_element.text.strip()

                    if text and message_id:
                        chat_data.append((timestamp, name, message_id, text))

            except Exception:
                continue
        return sorted(chat_data, key=lambda x: x[0])

    def process_and_read_messages(self, chat_data: List[Tuple[str, str, str, str]], history: List[Tuple[str, str, str, str]]) -> None:
        for idx, (timestamp, name, message_id, text) in enumerate(chat_data):
            if name != "Bạn" and not text.startswith("https:"):
                logging.info(f"New chat message: [{timestamp}] {name}: {text}")

                if len(history) < 2 or history[-1][1] != name or history[-1][0] != timestamp:
                    self.engine.speech(name)

                flag = False
                if text.startswith('/respone'):
                    text = text.replace('/respone','')
                    flag = True

                self.engine.speech(text)

                if flag:
                    respone = self.gemini_model.respone(text)
                    self.engine.speech('Tôi sẽ trả lời câu hỏi của bạn như sau: ' + respone)
                    
    def run(self,seen_messages: set = set(), chat_history: List[Tuple[str, str, str, str]] = [], limit_message: int = -1):
        self.config_chatbot()
        chat_data = self.get_chat_messages()
        new_messages = [(t, n, m, txt) for (t, n, m, txt) in chat_data if m not in seen_messages]
        seen_messages.update(m for (_, _, m, _) in new_messages)
        try:
            if new_messages:
                self.process_and_read_messages(new_messages, chat_history)
                chat_history.extend(new_messages)
            sleep(0.1)
        except Exception as e:
            logging.error(f"Meeting error: {e}")
            self.release()
            raise Exception("Meeting ended. Chrome tab closed")
        finally:
            gc.collect()
            if limit_message != -1:
                if len(chat_history) >= limit_message:
                    raise LimitReach()

        return seen_messages, chat_history

    def release(self):
        self.driver.quit()