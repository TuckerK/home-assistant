import board
import neopixel

from . import config

PIN = getattr(board, config.PIXEL_PIN)


class LedRing:
    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            PIN,
            config.PIXEL_COUNT,
            brightness=config.BRIGHTNESS,
            auto_write=True,
            pixel_order=neopixel.GRB,
        )

    def set(self, color, label=""):
        print(f"LED -> {label}")
        self.pixels.fill(color)
