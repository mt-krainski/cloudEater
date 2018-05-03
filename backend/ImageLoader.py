from typing import Tuple, List
import os
from scipy.ndimage import imread
import numpy as np

def load_test_images() -> Tuple[List[np.ndarray], np.ndarray, List[np.ndarray]]:
    test_folder = os.path.join(__file__,'..','..','test_images/')
    test_image_1 = imread(os.path.join(test_folder, 'color_test_1.jpg'))
    test_image_2 = imread(os.path.join(test_folder, 'color_test_2.jpg'))

