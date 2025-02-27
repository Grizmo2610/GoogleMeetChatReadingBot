import json
import logging
import os
from Model import *
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

config_path: str = 'data/config.json'
credentials_path = 'data/credentials.json'

driver = webdriver.Chrome(options=chrome_default_option())
ai = VoiceAI(driver, config_path, credentials_path)

ai.join_meeting()

seen_messages: set = set()
chat_history: List[Tuple[str, str, str, str]] = []

while True:
    try:
        seen_messages, chat_history = ai.run(seen_messages, chat_history)
    except LimitReach as E:
        print(E)
        break

ai.release()