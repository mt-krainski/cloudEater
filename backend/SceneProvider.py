from backend.Scene import Scene
from backend.ImageLoader import load_test_images, load_guess, normalize_and_flatten

import numpy as np

class SceneProvider:
    def __init__(self):
        self.scene = Scene(*load_test_images())
        self._sat_counter = 0

    def get_next_satellite_image(self):
        self._sat_counter += 1
        return self.scene.satellite_images[self._sat_counter % len(self.scene.satellite_images)]

    def end_round(self, pixels: np.ndarray):
        self.scene.submit_map(np.swapaxes(pixels.astype(np.float64),0,1))