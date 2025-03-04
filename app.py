import platform
import logging
from Models.Model import *
from Models.GetDriver import *

# Configuration file paths
CONFIG_PATH: str = "configurations/config.json"
CREDENTIALS_PATH: str = "configurations/credentials.json"

def get_browser(os_name: str) -> DriverType:
    """Select the appropriate browser based on the operating system."""
    if os_name == "Windows":
        return DriverType.EDGE  # Default for Windows
    elif os_name == "Darwin":
        return DriverType.SAFARI  # Default for macOS
    elif os_name == "Linux":
        return DriverType.CHROME  # Prefer Chrome, fallback to Firefox if needed
    else:
        raise Exception("Unsupported operating system")

def main():
    """Main function to initialize WebDriver and automate Google Meet."""
    os_name = platform.system()
    driver = get_driver(get_browser(os_name))  # Initialize WebDriver
    # driver = get_driver(driver_type=DriverType.CHROME)  # Initialize WebDriver
    ai = VoiceAI(driver, CONFIG_PATH, CREDENTIALS_PATH)

    try:
        ai.join_meeting()  # Join the meeting

        seen_messages: set = set()
        chat_history: List[Tuple[str, str, str, str]] = []

        while True:
            try:
                # Continuously process messages during the meeting
                seen_messages, chat_history = ai.run(seen_messages, chat_history)
            except LimitReach as e:
                logging.warning(f"Limit reached: {e}")
                break  # Exit the loop if message limit is reached

    finally:
        ai.release()  # Ensure resources are properly released

if __name__ == "__main__":
    main()
