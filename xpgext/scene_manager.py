SCENE_NOT_REGISTERED_ = "Scene {} has not been registered."
SCENE_ALREADY_REGISTERED_ = "Scene {} has already been registered."


class SceneRegisteringError(Exception):
    """Raised when registering a scene was unsuccessful."""


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

    def find_by_name(self, name):
        """
        Find elements of the given name.

        :param name: name of the elements to find
        :type name: str
        :return: list of elements of the given name
        :rtype: list
        """

    def get_by_name(self, name):
        """
        Get the first element whose name matches the given one.

        :param name: name to check
        :type name: str
        :return: element
        """


class SimpleSceneManager(SceneManagerBase):

    def __init__(self):
        self._scenes = dict()
        self._current_scene = None
        self._sprites = list()

    def register_scene(self, scene, name):
        if name in self._scenes.keys():
            raise SceneRegisteringError(SCENE_ALREADY_REGISTERED_.format(name))
        self._scenes[name] = scene

    def load_scene(self, name):
        try:
            self._current_scene = self._scenes[name](self)
        except KeyError:
            raise SceneLoadingError(SCENE_NOT_REGISTERED_.format(name))
        else:
            self._sprites.clear()
            for sprite in self._current_scene.sprites:
                self._sprites.append(sprite)
            for sprite in self._sprites:
                for component in sprite.components:
                    component.on_scene_loaded()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        for sprite in reversed(self._sprites):
            sprite.draw(surface)

    def handle_event(self, event):
        for sprite in reversed(self._sprites):
            if sprite.handle_event(event):
                break

    def update(self):
        for sprite in reversed(self._sprites):
            sprite.update()

    def find_by_name(self, name):
        result = list()
        for sprite in self._sprites:
            result.extend(sprite.find_by_name(name))
        return result

    def get_by_name(self, name):
        sprites = self.find_by_name(name)
        if len(sprites) == 0:
            return None
        return sprites[0]
