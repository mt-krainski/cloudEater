from typing import List, Tuple
from backend.ImageLoader import load_test_images, load_guess, normalize_and_flatten
from scipy.ndimage import gaussian_filter
import numpy as np

import matplotlib.pyplot as plt


class Scene:
    """ Wrapper for the entire (one place on earth with clouds)

    """
    def __init__(self, id, satellite_images: List[np.ndarray], ground_truth: np.ndarray, submits: List[np.ndarray]):
        """

        :param satellite_images: List of images of size [m x n x i], where i can be anything, usually 3 for RGB
        :param ground_truth: [m x n] binary image
        :param submits: List of [m x n] binary images
        """
        self._id = id
        self._satellite_images = satellite_images
        self._ground_truth = ground_truth
        self._submits = submits
        if len(satellite_images) < 1:
            raise TypeError("Need at least one satellite image.")
        #if any(s.shape[0:2] != satellite_images[0].shape[0:2] for s in satellite_images):
        #    raise TypeError(f"Satellite images are not all the same shape: {[s.shape for s in satellite_images]}")

        self._shape = (600, 800)

        #if ground_truth.shape != self.shape:
        #    raise TypeError(f"Ground truth must have shape {self.shape}, not {ground_truth.shape}")
        #if any(s.shape != self.shape for s in submits):
        #    raise TypeError(f"Submits must have shape {self.shape}, not {[s.shape for s in submits]}")

    @property
    def id(self) -> int:
        return self._id

    @property
    def satellite_images(self) -> List[np.ndarray]:
        """

        :return: List of real satellite images to be used as underlay
        """
        return self._satellite_images

    @property
    def ground_truth(self) -> np.ndarray:
        return self._ground_truth

    @property
    def past_submits(self) -> List[np.ndarray]:
        return self._submits

    @property
    def best_guess(self) -> np.ndarray:
        return (self.heatmap - 0.5) * 2
        # TODO incorporate submits, instead of just looking at ground truth
        # return (self.ground_truth - 0.5) * 2

    @property
    def heatmap(self) -> np.ndarray:
        heatmap = np.zeros(self.shape)
        for s in self.past_submits:
            heatmap = np.add(heatmap, s)
        heatmap = heatmap / np.max(heatmap)
        return heatmap

    def get_scoremap(self, image_to_score: np.ndarray) -> np.ndarray:
        return np.multiply(image_to_score, self.best_guess)

    @property
    def shape(self) -> Tuple[int, int]:
        return self._shape

    def submit_map(self, marked_image: np.ndarray, show_info = True) -> float:
        """ Call this method when you are done with a round. It will return the score.

        :param marked_image: Binary image where 1 is marked by player, and 0 is not marked by player
        :param show_info: Whether to show additional information (plots)
        :return: Evaluated score
        """
        # TODO evaluate score
        marked_image = normalize_and_flatten(marked_image)
        score = self._evaluate_score(marked_image)
        if show_info:
            self._show_information(marked_image)
        # TODO store submit in database

        return score

    def _show_information(self, marked_image: np.ndarray):
        stdev = 3
        blurred_marks = gaussian_filter(marked_image, stdev)
        plt.imshow(blurred_marks,cmap='plasma')
        plt.title("Your submitted marks")
        plt.show()

        blurred_heatmap = gaussian_filter(self.heatmap, 2*stdev)
        plt.imshow(blurred_heatmap,cmap='hot')
        plt.title("Previous guess heatmap")
        plt.show()

        blurred_scoremap = gaussian_filter(self.get_scoremap(marked_image), stdev)
        plt.imshow(blurred_scoremap, cmap='RdYlGn', vmin=-1, vmax=1)
        plt.title("Score map")
        plt.show()

    def _evaluate_score(self, marked_image: np.ndarray) -> float:
        return np.sum(self.get_scoremap(marked_image))

if __name__=='__main__':
    import matplotlib.image as mpimg

    imgs = load_test_images()
    s = Scene(*imgs)
    print(f"Score: {s.submit_map(load_guess())}")
    for img in imgs[0] + [imgs[1]]:
        plt.imshow(img)
        plt.show()

    plt.imshow(s.heatmap, cmap='plasma')
    plt.show()