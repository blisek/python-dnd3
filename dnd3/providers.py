__author__ = 'bartek'
import random


class ClassDataProvider:
    def get_hit_points(self, walls):
        raise NotImplementedError()


class RandomClassDataProvider(ClassDataProvider):
    def get_hit_points(self, walls):
        return random.randint(1, walls)
