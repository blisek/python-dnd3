__author__ = 'bartek'
from dnd3 import models, flags


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
        'Czasowo zyskuje +4 do Siły, +4 do Budowy, +2 do RO na Wolę, -2 do KP'
    )

    def __init__(self):
        super().__init__('rage', False)
        self.will_mod = "{0}_{1}".format(models.P_WILL, self.sys_name)
        self.ac_mod = "{0}_{1}".format(models.P_ARMOR_CLASS, self.sys_name)

    def turn_on(self, controller, *args, **kwargs):
        controller.model[models.P_SPECIAL_ABILITIES][self.sys_name] = kwargs[PARG_USE_PER_DAY]

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