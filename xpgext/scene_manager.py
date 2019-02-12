import pygame

SCENE_NOT_REGISTERED_ = "Scene {} has not been registered."
SCENE_ALREADY_REGISTERED_ = "Scene {} has already been registered."


class SceneRegisteringError(Exception):
    """Raised when registering a scene was unsuccessful."""


class SceneLoadingError(Exception):
    """Raised when loading a scene was unsuccessful."""


class SimpleSceneManager:
    """
    The class managing the scenes of the game.

    It governs registering and loading of the scenes and the execution of the methods of the currently loaded scene.
    This is the most basic version of such class that provides convenient defaults. If you want to alter the execution
    of the whole game, the methods of this class should be overridden.
    """

    def __init__(self):
        self._scenes = dict()
        self._current_scene = None
        self._sprites = list()
        self._static = dict()
        self._screen_rect = None

    @property
    def screen_rect(self):
        """
        Object of the type pygame.Rect with the values corresponding to the current display mode.
        """

        if self._screen_rect is None:
            self._screen_rect = pygame.display.get_surface().get_rect()
        return self._screen_rect

    @property
    def static(self):
        """
        Dictionary holding all the data, that should not be changed, reset or deleted when a new scene is loaded.

        This property provides an easy way to keep data like player character's info, gathered items and other
        variables, that should be common for all scenes.
        """

        return self._static

    def register_scene(self, scene, name):
        """
        Register new scene for later use. It will be accessible under the provided name.

        :param scene: scene to register
        :type scene: Scene
        :param name: key name for accessing the scene
        :type name: str
        """

        if name in self._scenes.keys():
            raise SceneRegisteringError(SCENE_ALREADY_REGISTERED_.format(name))
        self._scenes[name] = scene

    def load_scene(self, name):
        """
        Load a previously registered scene.

        :param name: name of the scene to load
        :type name: str
        """

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
            for sprite in self._sprites:
                for component in sprite.components:
                    component.on_spawn()

    def draw(self, surface):
        """
        Draw all the scene elements on the given surface.

        :param surface: the pygame main surface
        :type surface: pygame.Surface
        """

        surface.fill((0, 0, 0))
        for sprite in reversed(self._sprites):
            sprite.draw(surface)

    def handle_event(self, event):
        """
        Pass the event to each of the scene elements until one of them handles the event.

        :param event: event to handle
        :type event: pygame.event.Event
        """

        for sprite in reversed(self._sprites):
            if sprite.handle_event(event):
                break

    def update(self):
        """
        Update all the scene elements. Called every frame.
        """

        for sprite in reversed(self._sprites):
            sprite.update()

    def spawn(self, sprite):
        """
        Spawn the sprite.

        :param sprite: the sprite to spawn
        """

        self._sprites.append(sprite)
        for component in sprite.components:
            component.on_spawn()

    def kill(self, sprite):
        """
        Remove the sprite from the game.

        :param sprite: the sprite to remove
        """

        try:
            self._sprites.remove(sprite)
        except ValueError:
            msg = "sprite '{}' cannot be killed, because it is not alive in the scene manager"
            raise ValueError(msg.format(sprite.name))
        else:
            for component in sprite.components:
                component.on_kill()

    def find_by_name(self, name):
        """
        Find elements of the given name.

        :param name: name of the elements to find
        :type name: str
        :return: list of elements of the given name
        :rtype: list
        """

        result = list()
        for sprite in self._sprites:
            result.extend(sprite.find_by_name(name))
        return result

    def get_by_name(self, name):
        """
        Get the first element whose name matches the given one.

        :param name: name to check
        :type name: str
        :return: element
        """

        sprites = self.find_by_name(name)
        if len(sprites) == 0:
            return None
        return sprites[0]
