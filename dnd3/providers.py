__author__ = 'bartek'
import random
import collections
import math
import dnd3.skills


class ClassDataProvider:
    def get_hit_points(self, walls: int) -> int:
        raise NotImplementedError()

    def get_skills(self, skills: list, class_skills: list, points: int) -> dict:
        raise NotImplementedError()

    def get_abilities(self, min_value: int=8) -> dict:
        """ Zwraca słownik z wartościami atrybutów. W słowniku muszą znaleźć się wartości dla WSZYSTKICH atrybutów
        :return: dict
        """
        raise NotImplementedError()


class RandomClassDataProvider(ClassDataProvider):

    # Procentowy udział umiejętności klasowych wśród wszystkich umiejętności
    CLASS_SKILLS_PARTICIPATION = 0.7

    def get_hit_points(self, walls):
        return random.randint(1, walls)

    def get_skills(self, skills, class_skills, points):
        choosen_skills = collections.defaultdict(lambda: 0)
        for i in range(math.floor(points * RandomClassDataProvider.CLASS_SKILLS_PARTICIPATION)):
            try:
                name = getattr(random.choice(class_skills), dnd3.skills.SP_SYSTEM_NAME)
                choosen_skills[name] += 1
            except IndexError:
                pass

        for i in range(math.ceil(points * (1 - RandomClassDataProvider.CLASS_SKILLS_PARTICIPATION))):
            try:
                name = getattr(random.choice(skills), dnd3.skills.SP_SYSTEM_NAME)
                choosen_skills[name] += 1
            except IndexError:
                pass
        return choosen_skills