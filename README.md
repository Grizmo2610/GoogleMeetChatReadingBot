# **REAL-TIME GOOGLE MEET CHAT-TO-SPEECH**  

Google Meet is an essential tool for virtual meetings, and its chat feature allows participants to communicate effectively without interrupting the speaker. However, in many cases, presenters may be too focused on their presentation and miss important messages sent in the chat. This can lead to overlooked questions, unaddressed concerns, or a lack of engagement.  

To solve this problem, this project provides a **real-time chat-to-speech** solution that converts incoming chat messages into speech with minimal delay. This allows presenters to stay informed of discussions in the chat without needing to divert their attention from the main presentation.  

By using this tool, Google Meet participants can ensure that every message is heard, making meetings more interactive and inclusive.  

---

# **SETUP GUIDE**  

## **1. Install Dependencies**  

Before running the program, install the necessary dependencies by executing the setup script:  

```bash
python setup.py
```  

Additionally, ensure that the **FFmpeg binary path** (`bin` folder) is added to the system's PATH environment variable. A system restart is recommended for the changes to take full effect.  

---

## **2. Initialize Configuration Files**  

### **2.1 `credentials.json` (Login & Meeting Configuration)**  

This file contains the login credentials and meeting link required for the bot to join a Google Meet session.  

- **`email` and `password`**: Enter the email and password of the Google account that will be used for joining the meeting.  
  - **Important:** The account **must have two-step verification disabled**. If two-step verification is enabled, you will need to log in manually.  
  - **Recommendation:** It is advisable to use a separate Gmail account exclusively for this purpose to avoid security risks.  

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
    "LANG": "vi"
}
```  

- **`REMOVE`**: If set to `true`, processed messages will be removed from the chat after being read aloud.  
- **`SPEED`**: Controls the speed of speech synthesis (e.g., `1.0` is normal speed, `1.5` is faster, and `0.8` is slower).  
- **`LANG`**: Defines the language for text-to-speech conversion. Use `"vi"` for Vietnamese, `"en"` for English, etc.  

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

- If you do not need the bot to generate responses, you can skip this step.  
- To obtain a Gemini API key, follow the instructions here: [Gemini API Key Documentation](https://ai.google.dev/gemini-api/docs/api-key).  

---

# **RUNNING THE PROGRAM**  

After completing the setup, execute the following command to start the chat-to-speech system:  

```bash
python app.py
```  

The bot will automatically join the specified Google Meet session, listen for new chat messages, and convert them into speech in real-time. If the Gemini AI integration is enabled, the bot can also generate and read responses aloud when necessary.  

---

# **NOTES & RECOMMENDATIONS**  

- **Ensure that the Google account used for login is dedicated to this purpose.** Using a personal account may lead to security risks or access issues.  
- **Adjust the speech settings in `config.json`** to match your language and speed preferences.  
- **If chat messages are not being converted into speech,** verify that your system has FFmpeg installed and properly configured in the system's PATH.  
- **For AI-powered responses, ensure the Gemini API key is correctly set up.** If no key is provided, the bot will function purely as a chat-to-speech system.  

This tool is designed to enhance online presentations and discussions by ensuring that chat messages are never overlooked.