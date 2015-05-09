__author__ = 'bartek'
from dnd3 import controllers
import dnd3.feats
import dnd3.skills


class Context:
    def __init__(self):
        self.feats = []
        self.skills = []

    def get_feats(self):
        """ Zwraca iterator do listy atutów tego kontekstu w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return iter(self.feats)

    def get_feats_available_for_creature(self, controller: controllers.CreatureController):
        """ Zwraca iterator do listy atutów tego kontekstu, których wymagania spełnia kontroler, w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return filter(lambda l: l.is_available_for(controller), self.feats)

    def get_skills(self):
        return iter(self.skills)


_DEFAULT_CONTEXT = None

# wyrzucić?
def default_context() -> Context:
    if _DEFAULT_CONTEXT is None:
        pass
    return _DEFAULT_CONTEXT


class ContextBuilder:
    def __init__(self):
        self._feats = []
        self._skills = []
        self._special_abilities = []
        self._classes = []
        self._races = []
        self._context = Context()

    def add_race(self, race):
        pass

    def add_races(self, races):
        pass

    def add_feat(self, feat: dnd3.feats.Feat):
        self._context.feats.append(feat)
        return self

    def add_feats(self, feats: list):
        self._context.feats.extend(feats)
        return self

    def add_skill(self, skill: dnd3.skills.Skill):
        self._context.skills.append(skill)
        return self

    def add_skills(self, skills: list):
        self._context.skills.extend(skills)
        return self

    def add_special_ability(self, spec_a):
        pass

    def add_special_abilities(self, spec_abs):
        pass

    def add_class(self, c_class):
        pass

    def add_classes(self, c_classes):
        pass

    def build(self) -> Context:
        return self._context