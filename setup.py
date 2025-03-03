import os
import zipfile
import urllib.request
import platform
import subprocess
import sys

def install_ffmpeg_windows():
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    ffmpeg_dir = "C:\\ffmpeg"
    zip_path = "ffmpeg.zip"

    print("Downloading ffmpeg...")
    urllib.request.urlretrieve(url, zip_path)

    print("Extracting...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(ffmpeg_dir)

    os.remove(zip_path)

    bin_path = os.path.join(ffmpeg_dir, os.listdir(ffmpeg_dir)[0], "bin")
    os.environ["PATH"] += os.pathsep + bin_path

    print(f"FFmpeg installed at {bin_path}")

def install_ffmpeg_linux():
    os.system("sudo apt update && sudo apt install -y ffmpeg")
    print("FFmpeg installed on Linux.")

def install_ffmpeg_macos():
    os.system("brew install ffmpeg")
    print("FFmpeg installed on macOS.")

def install_ffmpeg():
    system_name = platform.system()
    if system_name == "Windows":
        install_ffmpeg_windows()
    elif system_name == "Linux":
        install_ffmpeg_linux()
    elif system_name == "Darwin":
        install_ffmpeg_macos()
    else:
        print("Unsupported OS for FFmpeg installation.")

def install_requirements():
    requirements_file = "requirements.txt"
    if os.path.exists(requirements_file):
        print("Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
    else:
        print(f"{requirements_file} not found. Skipping package installation.")

def main():
    install_ffmpeg()
    install_requirements()
    print("Setup completed.")

if __name__ == "__main__":
    main()
