from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import gc
import os
import pyttsx3
import json
import time
from time import sleep
import logging
import logging.config

import Gemini
from Gemini import GeminiTranscript

from typing import List, Tuple, Optional

if not os.path.exists('log'):
    os.makedirs('log')
logging.basicConfig(level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(f"log/{int(time.time())}.log", encoding="utf-8")])

logging.info("Starting program!")

try:
    logging.info("Loading credentials file")
    credentials_path = "data/credentials.json"  # Replace with real credentials.json path 
    with open(credentials_path, "r") as f:
        account: dict = json.load(f)
    logging.info("Credentials file loaded successfully")
except FileNotFoundError as FFE:
    logging.error("Credentials file does not exist!")
    raise FFE  # Stop execution if credentials file is missing

email: str = account["email"]
password: str = account["password"]
meeting_link: str = account["meeting_link"]

engine = pyttsx3.init()
current_voice_name = None

def config():
    global current_voice_name
    try:
        logging.info("Reading configuration file")
        with open("data/config.json", 'r') as f:
            config = json.load(f)
        logging.info("Configuration file loaded successfully")
    except FileNotFoundError:
        logging.warning("Config file not found! Initializing default config")
        if not os.path.exists('data'):
            os.makedirs('data')
        config = {"speed_rate": 150, "lang": "Vietnam"}
        with open("data/config.json", 'w') as f:
            json.dump(config, f, indent=4)
        logging.info("Default configuration file created")

    if engine.getProperty('rate') != config['speed_rate']:
        engine.setProperty("rate", config['speed_rate'])
        logging.info(f"Speed set to: {config['speed_rate']}")
        
    voices = engine.getProperty('voices')
    
    for voice in voices:
        if config['lang'] in voice.name:
            engine.setProperty("voice", voice.id)
            # logging.info(f"Voice set to: {voice.name}")
            # current_voice_name = voice.name
            break

config()
gemini_model = GeminiTranscript()


def login_to_google(driver: WebDriver, email: str, password: str) -> None:
    logging.info("Starting Google login process")
    driver.get("https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ")
    
    try:
        driver.find_element(By.ID, "identifierId").send_keys(email)
        driver.find_element(By.ID, "identifierNext").click()
        logging.info("Email entered and proceeding to password input")
        
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
        driver.find_element(By.ID, "passwordNext").click()
        logging.info("Password entered and login submitted")
        
        driver.implicitly_wait(10)
        driver.get("https://accounts.google.com/")
        logging.info("Google login successful")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        raise e

def turnOffMicCam(driver: WebDriver) -> None:
    logging.info("Attempting to turn off microphone and camera")
    wait = WebDriverWait(driver, 10)
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

def join_meeting(driver: WebDriver, meeting_link: str) -> None:
    logging.info(f"Joining Google Meet with link: {meeting_link}")
    driver.get(meeting_link)
    sleep(2)
    driver.get(meeting_link)
    
    turnOffMicCam(driver)
    
    wait = WebDriverWait(driver, 10)
    try:    
        alert = driver.switch_to.alert
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

def get_chat_messages(driver: WebDriver) -> List[Tuple[str, str, str, str]]:
    logging.info("Fetching chat messages from Google Meet")
    chat_data: List[Tuple[str, str, str, str]] = []
    
    messages = driver.find_elements(By.CSS_SELECTOR, ".Ss4fHf")
    
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

    logging.info(f"Retrieved {len(chat_data)} chat messages")
    return sorted(chat_data, key=lambda x: x[0])

def process_and_read_messages(chat_data: List[Tuple[str, str, str, str]], history: List[Tuple[str, str, str, str]]) -> None:
    for idx, (timestamp, name, message_id, text) in enumerate(chat_data):
        if name != "Bạn" and not text.startswith("https:"):
            logging.info(f"New chat message: [{timestamp}] {name}: {text}")
                
            if len(history) < 2 or history[-1][1] != name or history[-1][0] != timestamp:
                engine.say(name)
                engine.runAndWait()
                
            flag = False
            if text.startswith('/respone'):
                text = text.replace('/respone','')
                flag = True
                
            engine.say(text)
            engine.runAndWait()
            
            if flag:
                respone = gemini_model.respone(text)
                engine.say('Tôi sẽ trả lời câu hỏi của bạn như sau: ' + respone)
                engine.runAndWait()
    
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1,
})

driver: WebDriver = webdriver.Chrome(options=chrome_options)
logging.info("WebDriver initialized")

login_to_google(driver, email, password)
join_meeting(driver, meeting_link)

seen_messages: set = set()
chat_history: List[Tuple[str, str, str, str]] = []

while True:
    chat_data = get_chat_messages(driver)
    new_messages = [(t, n, m, txt) for (t, n, m, txt) in chat_data if m not in seen_messages]
    seen_messages.update(m for (_, _, m, _) in new_messages)

    try:
        if new_messages:
            process_and_read_messages(new_messages, chat_history)
            chat_history.extend(new_messages)
        sleep(0.1)
    except Exception as e:
        logging.error(f"Meeting error: {e}")
        driver.quit()
        logging.info("Meeting ended. Chrome tab closed")
        break
    finally:
        gc.collect()
        config()
