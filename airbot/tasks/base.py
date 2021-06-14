from abc import abstractmethod


class TaskMeta(type):
    """Task metaclass created to keep track of all its inheritance"""

    __inh__ = []

    def __new__(mcs, name, bases, dct):
        class_ = type.__new__(mcs, name, bases, dct)
        mcs.__inh__.append(class_)
        return class_


class BaseTask(metaclass=TaskMeta):
    """ """

    name = ""
    key = ""
    tags = []
    form_tags = []

    def __init__(self, element=None, **kwargs):
        self._element = element

    @abstractmethod
    def perform(self, modal):
        """ """

    @classmethod
    def make_from_raw_text(cls, text: str, **kwargs) -> "BaseTask":
        for _PotentialTaskClass in cls.__inh__:
            text = text.lower()
            if _PotentialTaskClass.tags and all(
                [t in text for t in _PotentialTaskClass.tags]
            ):
                return _PotentialTaskClass(**kwargs)
