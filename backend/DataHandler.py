import os
import glob
from scipy.misc import imsave
from scipy.ndimage import imread
from backend.Scene import Scene
from typing import List, Tuple


class DataHandler:
    """
    Container for handling data on disk.
    """

    def __init__(self, db_abs_path_root: List[str]):
        self._db_abs_path_root = os.path.abspath(db_abs_path_root+"/test_database")
        self._Scene_list = glob.glob(self._db_abs_path_root+"/scene_*")


    def new_Scene(self, SceneObject: List[Scene]):
        """
        Creates a data entry from the Scene object
        """
        # make new scene object id
        new_scene_id = len(self._Scene_list)
        new_scene_path = self._db_abs_path_root+"/scene_" + new_scene_id
        # make directory structure for new scene
        os.mkdir(new_scene_path)
        os.mkdir(new_scene_path + "/SAT")
        os.mkdir(new_scene_path + "/TRUTH")
        os.mkdir(new_scene_path + "/SUBMITS")
        # Save satellite images
        for i, satellite_image in enumerate(SceneObject.satellite_images):
            fname = "sat_image"+str(i)+".png"
            imsave(new_scene_path + "/SAT/" + fname, satellite_image)
        # Save ground truth if exists
        if SceneObject.ground_truth:
            imsave(new_scene_path + "/TRUTH/truth.png", satellite_image)

    def pull_Scene(self, Scene_id):
        """
        Returns a Scene object from the database
        """
        scene_path = self._db_abs_path_root+"/scene_"+str(Scene_id)
        if not os.path.isdir(scene_path):
            return 1
        else:
            satellite_images = []
            submits = []
            # Read satellite images
            for f in glob.glob(scene_path+"/SAT/*.png"):
                image = imread(f)
                satellite_images.append(image[:,:,0:3])
            # Read ground truth
            f = glob.glob(scene_path + "/TRUTH/*.png")[0]
            try:
                ground_truth = imread(f, flatten=True)
            except FileNotFoundError:
                ground_truth = []
            # Read previous submits
            try:
                for f in glob.glob(scene_path+"/SUBMITS/*.png"):
                    image = imread(f, flatten=True)
                    submits.append(image)
            except FileNotFoundError:
                pass
            requested_scene = Scene(Scene_id, satellite_images, ground_truth, submits)
            return requested_scene

    def get_scene_from_name(self, scene_folder_name: str):
        return self.pull_Scene(int(scene_folder_name[6:]))


    def add_guess(self, Scene_id, guess):
        """
        Add new guess to Scene with number Scene_id
        """
        scene_path = self._db_abs_path_root+"/scene_"+str(Scene_id)
        num = len(glob.glob(scene_path+"/SUBMITS/submit_*.png")) + 1
        new_guess_name = scene_path + "/SUBMITS/submit_" + str(num) + ".png"
        if os.path.isfile(new_guess_name):
            raise IOError("File {} already exists! This should not happen!".format(new_guess_name))
        imsave(new_guess_name, guess)

    @property
    def db_abs_path_root(self):
        return self._db_abs_path_root


    @property
    def scene_list(self):
        return [os.path.basename(x) for x in self._Scene_list]

if __name__ == "__main__":
    db = DataHandler(os.getcwd())
    test_scene = db.pull_Scene(1)