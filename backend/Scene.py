from typing import List, Tuple

import numpy as np


class Scene:
    """ Wrapper for the entire (one place on earth with clouds)

    """
    def __init__(self, satellite_images: List[np.ndarray], ground_truth: np.ndarray, submits: List[np.ndarray]):
        self._satellite_images = satellite_images
        self._ground_truth = ground_truth
        self._submits = submits
        if len(satellite_images) < 1:
            raise TypeError("Need at least one satellite image.")
        if any(s.size[0:2] != satellite_images[0].size[0:2] for s in satellite_images):
            raise TypeError(f"Satellite images are not all the same size: {[s.size for s in satellite_images]}")

        self._size = tuple(self._satellite_images[0].size[0:2])

        if ground_truth.size != self.size:
            raise TypeError(f"Ground truth must have size {self.size}, not {ground_truth.size}")

    @property
    def satellite_images(self) -> List[np.ndarray]:
        return self._satellite_images

    @property
    def ground_truth(self) -> np.ndarray:
        return self._ground_truth

    @property
    def past_submits(self) -> List[np.ndarray]:
        return self._submits

    @property
    def best_guess(self) -> np.ndarray:
        # TODO incorporate submits, instead of just looking at ground truth
        return (self.ground_truth - 0.5) * 2

    @property
    def size(self) -> Tuple[int, int]:
        return self._size

    def submit_map(self, marked_image: np.ndarray):
        # TODO evaluate score
        score = self._evaluate_score(marked_image)
        # TODO store submit in database

        return score

    def _evaluate_score(self, marked_image: np.ndarray):
        return np.sum(np.multiply(marked_image, self.best_guess))