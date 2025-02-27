from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from enum import Enum

class DriverType(Enum):
    EDGE = "edge"
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"

def get_default_options(driver_type: DriverType):
    options_mapping = {
        DriverType.CHROME: ChromeOptions,
        DriverType.EDGE: EdgeOptions,
        DriverType.FIREFOX: FirefoxOptions,
        DriverType.SAFARI: SafariOptions,
    }
    
    options = options_mapping.get(driver_type, ChromeOptions)()
    
    if isinstance(options, (ChromeOptions, EdgeOptions)):
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1,
        })
    elif isinstance(options, FirefoxOptions):
        options.set_preference("permissions.default.microphone", 1)
        options.set_preference("permissions.default.camera", 1)
        options.set_preference("permissions.default.geo", 2)  # 2 = Chặn truy cập
        options.set_preference("dom.webnotifications.enabled", True)
    
    return options

def get_driver(driver_type: DriverType):
    return {
        DriverType.EDGE: webdriver.Edge,
        DriverType.FIREFOX: webdriver.Firefox,
        DriverType.CHROME: webdriver.Chrome,
        DriverType.SAFARI: webdriver.Safari,
    }.get(driver_type, webdriver.Chrome)(options=get_default_options(driver_type))