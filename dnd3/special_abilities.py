__author__ = 'bartek'
from dnd3 import models, flags, classes


PARG_USE_PER_DAY = 'use_per_day'


class SpecialAbility:
    def __init__(self, sys_name, passive):
        self.sys_name = sys_name
        self.passive = passive

    def system_name(self):
        return self.sys_name

    def is_passive(self):
        return self.passive

    def turn_on(self, controller, *args, **kwargs):
        raise NotImplementedError()

    def turn_off(self, controller, *args, **kwargs):
        raise NotImplementedError()

    def activate(self, controller):
        pass

    def deactivate(self, controller):
        pass

    def duration(self, controller):
        """ Zwraca czas trwania po aktywacji
        :param controller:
        :return: 2 elementowa krotka (czas trwania, jednostka czasu np. rundy)
        """
        pass

    def description(self):
        raise NotImplementedError()

    def get_uses(self, controller):
        """ Zwraca liczbę użyć zdolności
        :param controller:
        :return: krotka (liczba użyć, jednostka czasu)
        """
        pass

    def get_flags(self):
        return 0


class SpecialAbilityDescription:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


class Rage(SpecialAbility):

    DESCRIPTION = SpecialAbilityDescription(
        'Szał',
        'Czasowo zyskuje +4 do Siły, +4 do Budowy, +2 do RO na Wolę, -2 do KP.\n'
        'Czas trwanie: 3 + mod. z Bd (po zwiększeniu przez szał)'
    )

    FLAGS = flags.F_ALLTIME | flags.F_FIGHT | flags.F_LIMITED_DURATION

    def __init__(self):
        super().__init__('rage', False)
        self.will_mod = "{0}_{1}".format(models.P_WILL, self.sys_name)
        self.ac_mod = "{0}_{1}".format(models.P_ARMOR_CLASS, self.sys_name)

    def get_flags(self):
        return Rage.FLAGS

    def turn_on(self, controller, *args, **kwargs):
        controller.model[models.P_SPECIAL_ABILITIES][self.sys_name] = True

    def turn_off(self, controller, *args, **kwargs):
        del controller.model[models.P_SPECIAL_ABILITIES][self.sys_name]

    def description(self):
        return Rage.DESCRIPTION

    def activate(self, controller):
        """ Aktywuje
        :type controller: dnd3.controllers.CreatureController
        :param controller:
        :return:
        """
        model = controller.model
        model[models.P_STR] += 4
        controller.strength_mod(True)
        model[models.P_CON] += 4
        controller.constitution_mod(True)
        model[self.will_mod] = 2
        controller.st_will(True)
        model[self.kp_mod] = -2
        controller.ac_total(True)
        model[models.P_EFFECTS].add(self.sys_name)

    def deactivate(self, controller):
        model = controller.model
        model[models.P_STR] -= 4
        controller.strength_mod(True)
        model[models.P_CON] -= 4
        controller.constitution_mod(True)
        del model[self.will_mod]
        controller.st_will(True)
        del model[self.kp_mod]
        controller.ac_total(True)
        model[models.P_EFFECTS].remove(self.sys_name)

    def get_uses(self, controller):
        return 1 + (controller.class_total_level(classes.Barbarian.SYSTEM_NAME) // 4)

    def duration(self, controller):
        """
        :type controller: dnd3.controllers.CreatureController
        :param controller:
        :return:
        """
        if self.sys_name in controller.model[models.P_EFFECTS]:
            return 3 + controller.constitution_mod()
        else:
            return 5 + controller.constitution_mod()