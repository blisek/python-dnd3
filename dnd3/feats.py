__author__ = 'bartek'


class Feat:
    def __init__(self, system_name, passive):
        self.sys_name = system_name
        self.passive = passive

    def system_name(self):
        """ Zwraca nazwę systemową atutu
        :return: systemowa nazwa atutu
        """
        return self.sys_name

    def is_available_for(self, controller):
        """ Sprawdza czy postać spełnia wymagania atutu
        :param controller: kontroler postaci
        :return: True jeśli spełnia wymagania, inaczej False
        """
        raise NotImplementedError()

    def turn_on(self, controller, *args, **kwargs):
        """ Aktywuje atut dla danej postaci
        :param controller: kontroler postaci
        :param args: dodatkowe argumenty
        :param kwargs: dodatkowe argumenty
        :return: True jeśli aktywowano atut, inaczej False
        """
        raise NotImplementedError()

    def turn_off(self, controller, *args, **kwargs):
        """ Dezaktywuje atut
        :param controller: kontroler postaci
        :param args: dodatkowe argumenty
        :param kwargs: dodatkowe argumenty
        :return: True jeśli aktywowano atut, inaczej False
        """
        raise NotImplementedError()

    def feat_description(self):
        """ Zwraca nazwę atutu
        :return: FeatDescription z tekstowym opisem atutu
        """
        raise NotImplementedError()

    def is_passive(self):
        return self.passive

    def activate(self, controller):
        pass

    def deactivate(self, controller):
        pass


class FeatDescription:
    def __init__(self, name, description, requirements):
        self.__name = name
        self.__description = description
        self.__requirements = requirements

    def name(self):
        return self.__name

    def description(self):
        return self.__description

    def requirements(self):
        return self.__requirements


# Definicje atutów
class ExternFeat(Feat):
    def __init__(self, system_name, conditions, effects, triggers, description):
        super().__init__(system_name, False)
        self.conditions = conditions
        self.effects = effects
        self.triggers = triggers
        self.description = description

    def is_available_for(self, controller):
        return all(map(lambda x: x(controller), self.conditions))

    def turn_on(self, controller, *args, **kwargs):
        effects_prod = []
        for e in self.effects:
            tmp = e(controller)
            effects_prod.append(tmp)
            tmp.set()
        controller.feats_on[self.sys_name] = effects_prod

    def turn_off(self, controller, *args, **kwargs):
        if self.sys_name not in controller.feats_on:
            return None
        for e in controller.feats_on[self.sys_name]:
            e.unset()
        controller.feats_on[self.sys_name] = ()

    def feat_description(self):
        return self.description
