# **REAL-TIME GOOGLE MEET CHAT-TO-SPEECH**

> Google Meet is incredibly convenient, and its chat feature allows participants to communicate seamlessly. However, if users rely solely on chat, presenters might miss important messages. To address this issue, a solution is needed to convert chat messages into speech with minimal delay, allowing presenters to stay informed about discussions in the chat while continuing their presentation.

---

# Source Code Analysis

The project consists of the following key files and directories:

- **app.py**: The main file containing the logic to connect and read messages from Google Meet.
- **requirements.txt**: A list of required Python libraries for the project.
- **configurations/**: A directory containing configuration files for the project.
- **Models/**: A directory that stores data models used in the application.
- **CustomException/**: A directory containing custom exception classes for error handling.
- **docs/**: A directory that includes documentation related to the project.

### **app.py**
This file establishes a connection to the Google Meet session and listens for chat messages. When a new message is detected, it is processed and either displayed or stored as needed.

### **requirements.txt**
This file lists the necessary Python libraries, including `selenium` for browser automation and `requests` for making HTTP requests.

---

# Installation and Usage Guide

Below is a step-by-step guide to installing and running the project on a local environment.

## 1. System Requirements

- Python 3.11 or later
- `pip` package manager
- Google Chrome/Edge/Safari browser

## 2. Installation

### **Step 1**: Clone the repository

```bash
git clone https://github.com/Grizmo2610/GoogleMeetChatReadingBot.git
cd GoogleMeetChatReadingBot
```

### **Step 2**: Create and activate a virtual environment

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### **Step 3**: Install required dependencies

```bash
pip install -r requirements.txt
```

## 3. Configuration

Edit the configuration files in the `configurations/` directory to add Google login credentials and other settings such as the Google Meet session URL.

## 4. Running the Application

Once installation and configuration are complete, run the application using:

```bash
python app.py
```

The application will automatically open a browser, log in to the Google account, join the meeting, and start reading chat messages in real time.