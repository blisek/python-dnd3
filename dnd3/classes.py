__author__ = 'bartek'
import collections
from dnd3 import flags, models, special_abilities
import dnd3.controllers
import dnd3.providers
import math


class Class:
    def __init__(self, system_name: str, handle_epic: bool, alignments=flags.A_ALL_ALIGNMENTS):
        self.sys_name = system_name
        self.handle_epic = handle_epic
        self.alignments = alignments

    def assign(self, controller: dnd3.controllers.CreatureController,
               class_data_provider: dnd3.providers.ClassDataProvider,
               extra_return_arguments: dict) -> None:
        """ Aktywuje klasę dla modelu.
        Oprócz tego model
        """
        raise NotImplementedError()

    def is_assigned(self, controller: dnd3.controllers.CreatureController) -> bool:
        """ Informuje czy klasa jest przypisana do modelu
        :param controller: kontroler postaci
        :return: 2-elem. krotka, w której 1. element to wartość True/False zależnie od tego
        czy postać ma co najmniej jeden poziom w klasie oraz sumaryczny poziom w danej klasie
        """
        name = self.system_name()
        suma = sum(map(lambda x: x[1], filter(lambda x: x[0] == name, controller.model.classes)))
        return suma > 0, suma

    def increase_level(self, controller: dnd3.controllers.CreatureController,
                       class_data_provider: dnd3.providers.ClassDataProvider,
                       lvl: int, extra_return_arguments: dict) -> None:
        raise NotImplementedError()

    def is_handling_epic(self) -> bool:
        return self.handle_epic

    def system_name(self) -> str:
        return self.sys_name

    def class_description(self):
        raise NotImplementedError()

    def class_skills(self) -> list:
        """ Zwraca umiejętności klasowe
        :return: zbiór z systemowymi nazwami umiejętności
        """
        raise NotImplementedError()

    def hit_dice(self) -> int:
        """ KW tej klasy.
        Metody increase_level, turn_on, turn_off nie modyfikują PW modelu.
        :return: zwraca kość wytrzymałości
        """
        raise NotImplementedError()

    # TODO: NIEPOTRZEBNE (przekazywanie za pomocą extra arguments)
    def skill_ranks_per_level(self) -> int:
        """ Zwraca liczbę ramg co poziom
        :return: liczba rang co poziom
        """
        raise NotImplementedError()

    def available_for_alignment(self, a: int) -> bool:
        return bool(self.alignments & a)

    def fortitude_modifier(self, level: int) -> int:
        raise NotImplementedError()

    def reflex_modifier(self, level: int) -> int:
        raise NotImplementedError()

    def will_modifier(self, level: int) -> int:
        raise NotImplementedError()

    def base_attack_modifier(self, level: int) -> int:
        raise NotImplementedError()

    def num_of_attacks(self, level: int) -> int:
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

    SYSTEM_NAME = 'barbarian'

    def __init__(self):
        super().__init__(system_name=Barbarian.SYSTEM_NAME, handle_epic=False,
                         alignments=flags.A_ALL_CHAOTIC | flags.A_ALL_NEUTRAL)
        self.fortitude_name = "{0}_{1}".format(models.P_FORTITUDE, self.sys_name)
        self.reflex_name = "{0}_{1}".format(models.P_REFLEX, self.sys_name)
        self.will_name = "{0}_{1}".format(models.P_WILL, self.sys_name)
        self.base_attack_name = "{0}_{1}".format(models.P_BASE_ATTACK, self.sys_name)
        self.hp_barbarian = "{0}_{1}".format(models.P_HP, self.sys_name)

    def system_name(self):
        return Barbarian.SYSTEM_NAME

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

    def assign(self, controller, class_data_provider, extra_return_arguments):
        """ Przypisuje klasę do modelu postaci oraz ustawia poziom w tej klasie na 1
        :type controller: dnd3.controllers.CreatureController
        :type class_data_provider: dnd3.providers.ClassDataProvider
        :param model: model postaci
        :param class_data_provider: klasa używana do komunikacji
        :return:
        """
        # dodanie 1 poziomu
        model = controller.model
        model[models.P_CLASSES].append((self.system_name(), 1))
        model[self.fortitude_name] = self.fortitude_modifier(1)
        model[self.reflex_name] = self.reflex_modifier(1)
        model[self.will_name] = self.will_modifier(1)
        model[self.base_attack_name] = self.base_attack_modifier(1)
        new_speca = [special_abilities.Rage.SYSTEM_NAME, special_abilities.FastMovement.SYSTEM_NAME]
        if flags.E_NEW_FEATS in extra_return_arguments:
            extra_return_arguments[flags.E_NEW_SPECA].extend(new_speca)
        else:
            extra_return_arguments[flags.E_NEW_SPECA] = new_speca

        # TODO: dodać biegłości