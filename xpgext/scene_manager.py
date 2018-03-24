class SceneLoadingError(Exception):
    """Raised when loading a scene was unsuccessful."""


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


class SimpleSceneManager(SceneManagerBase):

    def __init__(self):
        self._scenes = dict()
        self._current_scene = None
        self._sprites = list()

    def register_scene(self, scene, name):
        self._scenes[name] = scene

    def load_scene(self, name):
        try:
            self._current_scene = self._scenes[name](self)
        except IndexError:
            raise SceneLoadingError("Scene {} has not been registered.".format(name))
        else:
            self._sprites.clear()
            for sprite in self._current_scene.sprites:
                self._sprites.append(sprite)

    def draw(self, surface):
        for sprite in reversed(self._sprites):
            sprite.draw()

    def handle_event(self, event):
        for sprite in reversed(self._sprites):
            if sprite.handle_event(event):
                break

    def update(self):
        for sprite in reversed(self._sprites):
            sprite.update()
