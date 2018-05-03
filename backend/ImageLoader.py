from typing import Tuple, List
import os
from scipy.ndimage import imread
import numpy as np

def load_test_images() -> Tuple[List[np.ndarray], np.ndarray, List[np.ndarray]]:
    test_folder = os.path.join(__file__,'..','..','test_images/')
    test_image_1 = imread(os.path.join(test_folder, 'color_test_1.jpg'))
    test_image_2 = imread(os.path.join(test_folder, 'color_test_2.jpg'))

    ground_truth = imread(os.path.join(test_folder, 'ground_truth_1.png'), flatten=True)
    ground_truth = ground_truth - np.min(ground_truth)
    ground_truth = ground_truth / np.max(ground_truth)

    submits = [imread(os.path.join(test_folder, 'submit_'+str(i)+'.png'), flatten=True) for i in [1,2,3,4]]

    return ([test_image_1, test_image_2], ground_truth, submits)

if __name__=='__main__':
    print(load_test_images())