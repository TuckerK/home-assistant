import signal
import subprocess
import time

from . import config


def record_audio(filename="input.wav"):
    proc = subprocess.Popen(
        [
            "arecord",
            "-D",
            config.MIC_DEVICE,
            "-f",
            "S16_LE",
            "-c",
            "1",
            "-r",
            "16000",
            filename,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        input()
    finally:
        proc.send_signal(signal.SIGINT)
        proc.wait()

    time.sleep(0.3)
    return filename
