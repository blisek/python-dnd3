__author__ = 'bartek'
import dnd3.models
import dnd3.flags
import dnd3.creature_classes
import dnd3.controllers


PARG_USE_PER_DAY = 'use_per_day'


class SpecialAbility:
    def __init__(self, sys_name: str, passive: bool):
        self.sys_name = sys_name
        self.passive = passive

    def system_name(self) -> str:
        return self.sys_name

    def is_passive(self) -> bool:
        return self.passive

    def is_activated(self, controller: dnd3.controllers.CreatureController) -> bool:
        return self.sys_name in controller.model[dnd3.models.P_EFFECTS]

    def turn_on(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> None:
        raise NotImplementedError()

    def turn_off(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> None:
        raise NotImplementedError()

    def activate(self, controller: dnd3.controllers.CreatureController) -> None:
        pass

    def deactivate(self, controller: dnd3.controllers.CreatureController) -> None:
        pass

    def duration(self, controller: dnd3.controllers.CreatureController) -> tuple:
        """ Zwraca czas trwania po aktywacji
        :param controller:
        :return: 2 elementowa krotka (czas trwania, jednostka czasu np. rundy)
        """
        pass

    def description(self):
        raise NotImplementedError()

    def get_uses(self, controller: dnd3.controllers.CreatureController) -> tuple:
        """ Zwraca liczbę użyć zdolności
        :param controller:
        :return: krotka (liczba użyć, jednostka czasu)
        """
        pass

    def get_flags(self) -> int:
        return 0


class SpecialAbilityDescription:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def get_name(self) -> str:
        return self.name

    def get_description(self):
        return self.description


class Rage(SpecialAbility):

    DESCRIPTION = SpecialAbilityDescription(
        'Szał',
        'Czasowo zyskuje +4 do Siły, +4 do Budowy, +2 do RO na Wolę, -2 do KP.\n'
        'Czas trwanie: 3 + mod. z Bd (po zwiększeniu przez szał)'
    )

    FLAGS = dnd3.flags.F_ALLTIME | dnd3.flags.F_FIGHT | dnd3.flags.F_LIMITED_DURATION

    SYSTEM_NAME = 'rage'

    def __init__(self):
        super().__init__(Rage.SYSTEM_NAME, False)
        self.will_mod = "{0}_{1}".format(dnd3.models.P_WILL, self.sys_name)
        self.ac_mod = "{0}_{1}".format(dnd3.models.P_ARMOR_CLASS, self.sys_name)

    def get_flags(self):
        return Rage.FLAGS

    def turn_on(self, controller, *args, **kwargs):
        controller.model[dnd3.models.P_SPECIAL_ABILITIES][self.sys_name] = True

    def turn_off(self, controller, *args, **kwargs):
        del controller.model[dnd3.models.P_SPECIAL_ABILITIES][self.sys_name]

    def description(self):
        return Rage.DESCRIPTION

    def activate(self, controller):
        """ Aktywuje
        :type controller: dnd3.controllers.CreatureController
        :param controller:
        :return:
        """
        model = controller.model
        model[dnd3.models.P_STR] += 4
        controller.strength_mod(True)
        model[dnd3.models.P_CON] += 4
        controller.constitution_mod(True)
        model[self.will_mod] = 2
        controller.st_will(True)
        model[self.kp_mod] = -2
        controller.ac_total(True)
        model[dnd3.models.P_EFFECTS].add(self.sys_name)

    def deactivate(self, controller):
        model = controller.model
        model[dnd3.models.P_STR] -= 4
        controller.strength_mod(True)
        model[dnd3.models.P_CON] -= 4
        controller.constitution_mod(True)
        del model[self.will_mod]
        controller.st_will(True)
        del model[self.kp_mod]
        controller.ac_total(True)
        model[dnd3.models.P_EFFECTS].remove(self.sys_name)

    def get_uses(self, controller):
        return 1 + (controller.class_total_level(dnd3.creature_classes.Barbarian.SYSTEM_NAME) // 4)

    def duration(self, controller):
        """
        :type controller: dnd3.controllers.CreatureController
        :param controller:
        :return:
        """
        if self.sys_name in controller.model[dnd3.models.P_EFFECTS]:
            return 3 + controller.constitution_mod()
        else:
            return 5 + controller.constitution_mod()


# TODO: deaktywacja atutu gdy wkłada pancerz ciężki
class FastMovement(SpecialAbility):

    DESCRITPTION = SpecialAbilityDescription(
        'szybkie poruszanie się',
        'szybkość wzrasta o +3 metry jeśli jest bez pancerza, w pancerzu lekkim lub średnim'
    )

    SYSTEM_NAME = 'fast_movement'

    def __init__(self):
        super().__init__(sys_name=FastMovement.SYSTEM_NAME, passive=True)

    def get_flags(self) -> int:
        return dnd3.flags.F_ALLTIME

    def description(self):
        return FastMovement.DESCRITPTION

    def turn_off(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> None:
        d = controller.model[dnd3.models.P_SPECIAL_ABILITIES]
        if self.sys_name in d:
            del d[self.sys_name]

    def turn_on(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> None:
        controller.model[dnd3.models.P_SPECIAL_ABILITIES][self.sys_name] = True