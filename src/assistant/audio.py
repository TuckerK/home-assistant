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
        ]
    )
    try:
        input()
    finally:
        proc.terminate()
        proc.wait()

    time.sleep(0.3)
    return filename
