__author__ = 'bartek'
import collections
from dnd3 import flags, models
import math


class Class:
    def __init__(self, system_name, handle_epic, alignments=flags.A_ALL_ALIGNMENTS):
        self.sys_name = system_name
        self.handle_epic = handle_epic
        self.alignments = alignments

    def assign(self, model, class_data_provider):
        """ Aktywuje klasę dla modelu.
        Oprócz tego model
        :type model: dnd3.models.Creature
        :param model:
        :return:
        """
        raise NotImplementedError()

    def is_assigned(self, model):
        """ Informuje czy klasa jest przypisana do modelu
        :param controller: kontroler postaci
        :return: 2-elem. krotka, w której 1. element to wartość True/False zależnie od tego
        czy postać ma co najmniej jeden poziom w klasie oraz sumaryczny poziom w danej klasie
        """
        name = self.system_name()
        suma = sum(map(lambda x: x[1], filter(lambda x: x[0] == name, model.classes)))
        return suma > 0, suma

    def increase_level(self, model, class_data_provider, lvl):
        raise NotImplementedError()

    def is_handling_epic(self):
        return self.handle_epic

    def system_name(self):
        return self.sys_name

    def class_description(self):
        raise NotImplementedError()

    def class_skills(self):
        """ Zwraca umiejętności klasowe
        :return: zbiór z systemowymi nazwami umiejętności
        """
        raise NotImplementedError()

    def hit_dice(self):
        """ KW tej klasy.
        Metody increase_level, turn_on, turn_off nie modyfikują PW modelu.
        :return: zwraca kość wytrzymałości
        """
        raise NotImplementedError()

    def skill_ranks_per_level(self):
        """ Zwraca liczbę ramg co poziom
        :return: liczba rang co poziom
        """
        raise NotImplementedError()

    def available_for_alignment(self, a):
        return bool(self.alignments & a)

    def fortitude_modifier(self, level):
        raise NotImplementedError()

    def reflex_modifier(self, level):
        raise NotImplementedError()

    def will_modifier(self, level):
        raise NotImplementedError()

    def base_attack_modifier(self, level):
        raise NotImplementedError()

    def num_of_attacks(self, level):
        raise NotImplementedError()


ClassDescription = collections.namedtuple('ClassDescription', ['name', 'description', 'reqs', 'alignments', 'others'])


class Barbarian(Class):
    """ Barbarzyńca
    """
    SKILLS = frozenset((
        'jezdziectwo', 'nasluchiwanie', 'plywanie', 'postepowanie_ze_zwierzetami', 'rzemioslo', 'skakanie',
        'wspinaczka', 'wyczucie_kierunku', 'zastraszanie', 'znajomosc_dziczy'
    ))

    DESCRIPTION = ClassDescription()

    def __init__(self):
        super().__init__(system_name='barbarian', handle_epic=False,
                         alignments=flags.A_ALL_CHAOTIC | flags.A_ALL_NEUTRAL)

    def hit_dice(self):
        return 12

    def class_skills(self):
        return Barbarian.SKILLS

    def skill_ranks_per_level(self):
        return 4

    def class_description(self):
        return Barbarian.DESC

    def fortitude_modifier(self, level):
        return 2 + level // 2

    def reflex_modifier(self, level):
        return level // 3

    def will_modifier(self, level):
        return level // 3

    def base_attack_modifier(self, level):
        return level

    def num_of_attacks(self, level):
        return math.ceil(level / 5)

    def assign(self, model, class_data_provider):
        """ Przypisuje klasę do modelu postaci oraz ustawia poziom w tej klasie na 1
        :type model: dnd3.models.CreatureModel
        :type class_data_provider: dnd3.providers.ClassDataProvider
        :param model: model postaci
        :param class_data_provider: klasa używana do komunikacji
        :return:
        """
        # dodanie 1 poziomu
        model[models.P_CLASSES].append((self.system_name(), 1))

        fortitude_name = "{0}_{1}".format(models.P_FORTITUDE, self.sys_name)
        model[fortitude_name] = self.fortitude_modifier(1)

        reflex_name = "{0}_{1}".format(models.P_REFLEX, self.sys_name)
        model[reflex_name] = self.reflex_modifier(1)

        will_name = "{0}_{1}".format(models.P_WILL, self.sys_name)
        model[will_name] = self.will_modifier(1)

        base_attack_name = "{0}_{1}".format(models.P_BASE_ATTACK, self.sys_name)
        model[base_attack_name] = self.base_attack_modifier(1)

        pass