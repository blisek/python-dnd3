__author__ = 'bartek'


class CreatureBuilder:
    def __init__(self):
        pass

    def assign_before(self, **kwargs):
        pass

    def assign_race(self, **kwargs):
        raise NotImplementedError()

    def assign_class(self, **kwargs):
        raise NotImplementedError()

    def assign_skills(self, **kwargs):
        raise NotImplementedError()

    def assign_feats(self, **kwargs):
        raise NotImplementedError()

    def assign_after(self, **kwargs):
        pass

    def build(self):
        pass