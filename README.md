# **REAL-TIME GOOGLE MEET CHAT-TO-SPEECH**  

Google Meet is an essential tool for virtual meetings, and its chat feature allows participants to communicate effectively without interrupting the speaker. However, presenters often focus on their presentation and may miss important chat messages. This can lead to overlooked questions, unaddressed concerns, or reduced engagement.

To address this issue, this project provides a **real-time chat-to-speech** solution that converts incoming chat messages into speech with minimal delay. This allows presenters to stay informed of chat discussions without diverting attention from their main presentation.

By using this tool, Google Meet participants can ensure that every message is heard, making meetings more interactive and inclusive.

---

# **SETUP GUIDE**  

## **1. Install Dependencies**  

Before running the program, install the necessary dependencies by executing the setup script:  

```bash
python setup.py
```

Additionally, ensure that the **FFmpeg binary path** (`bin` folder) is added to the system's PATH environment variable. A system restart is recommended for the changes to take effect.

---

## **2. Initialize Configuration Files**  

### **2.1 `credentials.json` (Login & Meeting Configuration)**  

This file contains the login credentials and meeting link required for the bot to join a Google Meet session.  

- **`email` and `password`**: Enter the email and password of the Google account that will be used to join the meeting.  
  - **Important:** The account **must have two-step verification disabled**. If two-step verification is enabled, manual login is required.  
  - **Recommendation:** It is advisable to use a separate Gmail account for this purpose to avoid security risks.  

- **`meeting_link`**: Specify the Google Meet link where the bot should join.  

#### **Example of `credentials.json` file:**  

```json
{
    "email": "example@gmail.com",
    "password": "your-password",
    "meeting_link": "https://meet.google.com/sample-meeting-link"
}
```

Once the `credentials.json` file is created, update the `CREDENTIALS_PATH` variable in the `app.py` file to point to the correct file location.

---

### **2.2 `config.json` (Speech & Language Configuration)**  

This file controls the speech output settings, including language, speech speed, and message handling.  

#### **Example of `config.json` file:**  

```json
{
    "REMOVE": true,
    "SPEED": 1.0,
    "LANG": "en"
}
```

- **`REMOVE`**: If set to `true`, processed messages will be removed from the chat after being read aloud.  
- **`SPEED`**: Controls the speech synthesis speed (e.g., `1.0` is normal speed, `1.5` is faster, `0.8` is slower).  
- **`LANG`**: Defines the language for text-to-speech conversion. Use `"en"` for English, `"vi"` for Vietnamese, etc.  

Once configured, update the `CONFIG_PATH` variable in `app.py` to reflect the correct file location.

---

### **2.3 `gemini.key` (Google Gemini AI API Key - Optional)**  

If you want the bot to generate responses based on chat messages using Google's **Gemini AI**, you need to provide an API key.  

1. Create a file named `gemini.key`.  
2. Paste your Google API key inside the file.  

#### **Example of `gemini.key` file:**  

```
AIxxxxxxxxxxxx
```

3. Update the `path` variable in `Models/Gemini.py` to point to the `gemini.key` file.  

- If you do not need AI-generated responses, you can skip this step.  
- To obtain a Gemini API key, follow the instructions here: [Gemini API Key Documentation](https://ai.google.dev/gemini-api/docs/api-key).  

---

## **3. Selecting a Suitable Browser**  

In `app.py`, configure the browser using the `GetDriver.py` class. Supported browsers include:
- Google Chrome
- Microsoft Edge
- Firefox
- Safari

For other browsers, update the `GetDriver.py` file accordingly.

### **3.1. Modify `binary_location`**
Change `binary_location` to the desired browser path:

- **Cốc Cốc**:  
  ```python
  options.binary_location = "C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe"
  ```
- **Brave**:  
  ```python
  options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
  ```
- **Opera**:  
  ```python
  options.binary_location = "C:\\Users\\YourUser\\AppData\\Local\\Programs\\Opera\\opera.exe"
  ```

### **3.2. Call `get_driver`**
Use `DriverType.OTHER` for custom browsers:  
```python
driver = get_driver(DriverType.OTHER)
```

### **3.3. Add a New Browser**
Modify `DriverType` and include browser-specific handling:
```python
class DriverType(Enum):
    COCCOC = "coccoc"
    BRAVE = "brave"
    OPERA = "opera"
```
```python
elif driver_type == DriverType.BRAVE:
    options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
```
Call Selenium:
```python
driver = get_driver(DriverType.BRAVE)
```

> 🔹 **Note:** Ensure you download the correct ChromeDriver version for the chosen browser.

---

# **RUNNING THE PROGRAM**  

After completing the setup, execute the following command to start the chat-to-speech system:  

```bash
python app.py
```

The bot will automatically join the specified Google Meet session, listen for new chat messages, and convert them into speech in real time. If Gemini AI integration is enabled, the bot can also generate and read responses aloud when necessary.

---

# **NOTES & RECOMMENDATIONS**  

- **Use a dedicated Google account for login** to avoid security risks.
- **Adjust speech settings in `config.json`** to match your language and speed preferences.
- **If chat messages are not being converted into speech,** ensure FFmpeg is installed and properly configured in the system's PATH.
- **For AI-powered responses, ensure the Gemini API key is correctly set up.** If no key is provided, the bot will function as a chat-to-speech system only.

This tool enhances online presentations by ensuring that chat messages are never overlooked.

---

# **AUTHOR INFORMATION**  

- **Developer:** Hoàng Tuấn Tú | Tu Hoang | Grizmo
- **Nationality** Vietnamese
- **Contact:** hoangtuantu893@gmail.com
- **GitHub Repository:** https://github.com/Grizmo2610
- **License:** MIT License

Feel free to contribute, report issues, or suggest improvements!