__author__ = 'bartek'
import dnd3.controllers
import dnd3.models
import dnd3.flags
import dnd3.others


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

    def turn_on(self, controller: dnd3.controllers.CreatureController, extra_return_arguments: dict):
        controller.model[dnd3.models.P_RACE] = self.sys_name
        controller.model[dnd3.models.P_SIZE] = dnd3.others.S_MEDIUM
        prev_speed = controller.model[dnd3.models.P_SPEED]
        controller.model[dnd3.models.P_SPEED] = prev_speed if prev_speed > 9 else 9

        if dnd3.flags.E_FEATS_NUM in extra_return_arguments:
            extra_return_arguments[dnd3.flags.E_FEATS_NUM] += 1
        else:
            extra_return_arguments[dnd3.flags.E_FEATS_NUM] = 1

        if dnd3.flags.E_SKILLS_NUM in extra_return_arguments:
            extra_return_arguments[dnd3.flags.E_SKILLS_NUM] += 4
        else:
            extra_return_arguments[dnd3.flags.E_SKILLS_NUM] = 4

        if dnd3.flags.E_LANGUAGES in extra_return_arguments:
            extra_return_arguments[dnd3.flags.E_LANGUAGES].add(dnd3.others.L_COMMON)
        else:
            extra_return_arguments[dnd3.flags.E_LANGUAGES] = {dnd3.others.L_COMMON}

        if dnd3.flags.E_LANGUAGES_NUM in extra_return_arguments:
            extra_return_arguments[dnd3.flags.E_LANGUAGES_NUM] += 1
        else:
            extra_return_arguments[dnd3.flags.E_LANGUAGES_NUM] = 1

    def turn_off(self, controller: dnd3.controllers.CreatureController):
        controller.model[dnd3.models.P_RACE] = None
        controller.model[dnd3.models.P_SIZE] = None
        controller.model[dnd3.models.P_SPEED] = 0

    def increase_level(self, controller: dnd3.controllers.CreatureController,
                       class_data_provider: dnd3.providers.ClassDataProvider,
                       lvl: int, extra_return_arguments: dict):
        level = controller.class_total_level(self.sys_name)

        diff = lvl - level
        if diff <= 0:
            return

        # na każdym poziomie człowiek otrzymuje dodatkowy punkt umiejętności
        if dnd3.flags.E_SKILLS_NUM in extra_return_arguments:
            extra_return_arguments[dnd3.flags.E_SKILLS_NUM] += diff  # *1
        else:
            extra_return_arguments[dnd3.flags.E_SKILLS_NUM] = diff
