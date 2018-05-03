from backend.Scene import Scene
from backend.ImageLoader import load_test_images, load_guess, normalize_and_flatten


class SceneProvider:
    def __init__(self):
        self.scene = Scene(*load_test_images())
        self._sat_counter = 0

    def get_next_satellite_image(self):
        self._sat_counter += 1
        return self.scene.satellite_images[self._sat_counter % len(self.scene.satellite_images)]