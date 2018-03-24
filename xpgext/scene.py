class SceneBase:
    """
    Abstract base class for all the scene types.

    :param scene_manager: scene manager that owns this scene
    :type scene_manager: SceneManagerBase
    """

    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
