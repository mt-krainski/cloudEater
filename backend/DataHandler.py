import os
import glob
from scipy.misc import imsave

class DataHandler:
    """
    Container for handling data on disk.
    """

    def __init__(self, db_abs_path_root):
        self._db_abs_path_root = os.path.abspath(db_abs_path_root+"/test_database")
        self._Scene_list = glob.glob(self._db_abs_path_root+"/scene_*")


    def new_Scene(self, SceneObject):
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
        if SceneObject.

    def pull_Scene(self, Scene_id):
        """
        Returns a Scene object from the database
        """
        if not os.path.isdir(self._db_abs_path_root+"/scene_"+str(Scene_id)):
            return 1
        else:
            return 0

    def add_guess(self, Scene_id, guess):
        pass

    @property
    def db_abs_path_root(self):
        return self._db_abs_path_root


    @property
    def scene_list(self):
        return [os.path.basename(x) for x in self._Scene_list]

if __name__ == "__main__":
    db = DataHandler(os.getcwd())
    print(db.scene_list)