__author__ = 'bartek'
import dnd3.controllers
import dnd3.models
from dnd3 import flags


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

    def turn_on(self, controller: dnd3.controllers.CreatureController, extra_return_arguments: dict) -> None:
        raise NotImplementedError()

    def turn_off(self, controller: dnd3.controllers.CreatureController) -> None:
        raise NotImplementedError()

    def description(self) -> RaceDescription:
        raise NotImplementedError()

    def increase_level(self, controller: dnd3.controllers.CreatureController,
                       class_data_provider: dnd3.providers.ClassDataProvider,
                       lvl: int, extra_return_arguments: dict) -> None:
        raise NotImplementedError()


class Human(Race):

    DESCRIPTION = RaceDescription(
        'człowiek',
        ''
    )

    SYSTEM_NAME = 'human'

    def __init__(self):
        super().__init__(Human.SYSTEM_NAME)

    def description(self):
        return Human.DESCRIPTION

    # TODO: osbługa rasy Człowiek - darmowy atut na 1. poziomie, darmowe punkty umiejętności
    def turn_on(self, controller: dnd3.controllers.CreatureController, extra_return_arguments: dict):
        controller.model[dnd3.models.P_RACE] = self.sys_name

        if flags.E_FEATS_NUM in extra_return_arguments:
            extra_return_arguments[flags.E_FEATS_NUM] += 1
        else:
            extra_return_arguments[flags.E_FEATS_NUM] = 1

        if flags.E_SKILLS_NUM in extra_return_arguments:
            extra_return_arguments[flags.E_SKILLS_NUM] += 4
        else:
            extra_return_arguments[flags.E_SKILLS_NUM] = 4