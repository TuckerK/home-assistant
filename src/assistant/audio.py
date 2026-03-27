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
            "cd",
            "-V",
            "mono",
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
