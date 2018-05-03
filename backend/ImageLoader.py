from typing import Tuple, List
import os
from scipy.ndimage import imread
import numpy as np

def normalize_and_flatten(img: np.ndarray):
    if len(img.shape) > 3:
        raise TypeError()
    if len(img.shape) == 3:
        img = np.mean(img, axis=2)
    img = img - np.min(img)
    img = img / np.max(img)
    return img

def load_test_images() -> Tuple[List[np.ndarray], np.ndarray, List[np.ndarray]]:
    test_folder = os.path.join(__file__,'..','..','test_images/')
    test_image_1 = imread(os.path.join(test_folder, 'color_test_1.jpg'))
    test_image_2 = imread(os.path.join(test_folder, 'color_test_2.jpg'))

    ground_truth = imread(os.path.join(test_folder, 'ground_truth_1.png'), flatten=True)
    ground_truth = ground_truth - np.min(ground_truth)
    ground_truth = ground_truth / np.max(ground_truth)

    submits = [normalize_and_flatten(imread(os.path.join(test_folder, 'submit_'+str(i)+'.png'), flatten=True)) for i in [1,2,3,4]]

    return ([test_image_1, test_image_2], normalize_and_flatten(ground_truth), submits)


def load_guess() -> np.ndarray:
    test_folder = os.path.join(__file__, '..', '..', 'test_images/')
    guess = imread(os.path.join(test_folder, 'guess.png'), flatten=True)
    return normalize_and_flatten(guess)


if __name__=='__main__':
    print(load_test_images())