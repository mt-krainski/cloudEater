from backend.Scene import Scene
from backend.ImageLoader import load_test_images, load_guess, normalize_and_flatten
from backend.DataHandler import DataHandler
import numpy as np
import os

class SceneProvider:
    def __init__(self):
        self.data_handler = DataHandler(os.path.join(__file__,'..','..'))
        self._scene_counter = 0
        self._sat_counter = 0

        self._scene_list = self.data_handler.scene_list

    @property
    def current_scene(self):
        return self.data_handler.get_scene_from_name(
            self._scene_list[self._scene_counter % len(self._scene_list)])

    def increment_scene(self):
        self._scene_counter += 1
        return self.current_scene

    def get_next_satellite_image(self):
        self._sat_counter += 1
        return self.current_scene.satellite_images[self._sat_counter % len(self.current_scene.satellite_images)]

    def get_submit(self, id):
        if len(self.current_scene.past_submits) == 0:
            return None
        return self.current_scene.past_submits[id % len(self.current_scene.past_submits)]

    def get_random_scene(self):
        self._scene_counter = np.random.randint(1,7)
        return self.current_scene


    def end_round(self, pixels: np.ndarray):
        img = np.swapaxes(pixels.astype(np.float64),0,1)
        self.data_handler.add_guess(self.current_scene.id, img)
        self.current_scene.submit_map(img)