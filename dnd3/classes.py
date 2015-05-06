__author__ = 'bartek'
import collections
from dnd3 import flags


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

    def assign(self, model, class_data_provider):
        pass