__author__ = 'bartek'


class CreatureBuilder:
    def __init__(self):
        pass

    def assign_race(self):
        raise NotImplementedError()

    def assign_class(self):
        raise NotImplementedError()

    def assign_skills(self):
        raise NotImplementedError()

    def assign_feats(self):
        raise NotImplementedError()