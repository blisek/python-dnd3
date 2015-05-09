__author__ = 'bartek'
import dnd3.controllers


class RaceDescription:
    def __init__(self, name: str, desc: str):
        self._name = name
        self._description = desc

    def name(self) -> str:
        return self._name

    def description(self) -> str:
        return self._description


class Race:
    def __init__(self, system_name: str):
        self.sys_name = system_name

    def system_name(self) -> str:
        return self.sys_name

    def turn_on(self, controller: dnd3.controllers.CreatureController) -> None:
        raise NotImplementedError()

    def turn_off(self, controller: dnd3.controllers.CreatureController) -> None:
        raise NotImplementedError()

    def description(self) -> RaceDescription:
        raise NotImplementedError()


class Human(Race):

    DESCRIPTION = RaceDescription(
        'człowiek',
        ''
    )

    def __init__(self):
        super().__init__('human')

    def description(self):
        return Human.DESCRIPTION

    # TODO: osbługa rasy Człowiek - darmowy atut na 1. poziomie, darmowe punkty umiejętności