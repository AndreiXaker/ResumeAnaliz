import sys
import subprocess
import time


def launch_streamlit_app(app_file):

    cmd = [sys.executable, "-m", "streamlit", "run", app_file]
    return subprocess.Popen(cmd, start_new_session=True)


if __name__ == "__main__":
    streamlit_process = launch_streamlit_app("Resume_requirements_comparison.py")
    while True:
        time.sleep(5)
