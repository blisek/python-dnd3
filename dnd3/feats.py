__author__ = 'bartek'


class Feat:
    def system_name(self):
        """ Zwraca nazwę systemową atutu
        :return: systemowa nazwa atutu
        """
        raise NotImplementedError()

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
    def __init__(self, conditions, effects, triggers, description):
        self.conditions = conditions
        self.effects = effects
        self.triggers = triggers
        self.description = description

    def is_available_for(self, controller):
        pass