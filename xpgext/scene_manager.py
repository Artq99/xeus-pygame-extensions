class SceneManagerBase:
    """Abstract base class for all the scene manager types."""

    def register_scene(self, scene, name):
        """
        Register new scene for later use. It will be accessible under the provided name.

        :param scene: scene to register
        :type scene: Scene
        :param name: key name for accessing the scene
        :type name: str
        """

    def load_scene(self, name):
        """
        Load a previously registered scene.

        :param name: name of the scene to load
        :type name: str
        """

    def draw(self, surface):
        """
        Draw all the scene elements on the given surface.

        :param surface: the pygame main surface
        :type surface: pygame.Surface
        """

    def handle_event(self, event):
        """
        Pass the event to each of the scene elements until one of them handles the event.

        :param event: event to handle
        :type event: pygame.event.Event
        """

    def update(self):
        """
        Update all the scene elements. Called every frame.
        """
