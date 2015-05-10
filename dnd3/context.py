__author__ = 'bartek'
import inspect
import dnd3.controllers
import dnd3.parsers
import dnd3.feats
import dnd3.skills
import dnd3.creature_classes


class Context:
    def __init__(self):
        self.feats = {}
        self.skills = {}
        self.classes = {}

    def get_feats(self):
        """ Zwraca iterator do listy atutów tego kontekstu w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return iter(self.feats)

    def get_feats_available_for_creature(self, controller: dnd3.controllers.CreatureController):
        """ Zwraca iterator do listy atutów tego kontekstu, których wymagania spełnia kontroler, w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return filter(lambda l: l.is_available_for(controller), self.feats)

    def get_skills(self):
        return iter(self.skills.values())

    def get_classes(self):
        return iter(self.classes.values())

    def get_available_classes_for_alignments(self, flags):
        return filter(lambda x: x.available_for_alignment(flags), self.classes.values())


_DEFAULT_CONTEXT = None


# wyrzucić?
def default_context() -> Context:
    if _DEFAULT_CONTEXT is None:
        pass
    return _DEFAULT_CONTEXT


class ContextBuilder:
    def __init__(self):
        self._feats = []
        self._skills = {}
        self._special_abilities = []
        self._classes = {}
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
        self._skills[getattr(skill, dnd3.skills.SP_SYSTEM_NAME)] = skill
        return self

    def add_skills_from_list(self, skills: list):
        self._skills.update({getattr(s, dnd3.skills.SP_SYSTEM_NAME): s for s in skills})
        return self

    def add_skills_from_dict(self, skills: dict):
        self._skills.update(skills)
        return self

    def add_special_ability(self, spec_a):
        pass

    def add_special_abilities(self, spec_abs):
        pass

    def add_class(self, c_class: dnd3.creature_classes.Class):
        self._classes[c_class.system_name()] = c_class
        return self

    def add_classes_from_list(self, c_classes: list):
        self._classes.update({c.system_name(): c for c in c_classes})
        return self

    def add_classes_from_dict(self, c_classes: dict):
        self._classes.update(c_classes)
        return self

    def build(self) -> Context:
        self._context.classes = self._classes
        self._context.skills = self._skills
        return self._context


class StandardContextBuilder(ContextBuilder):
    def __init__(self, skills_xml: str=None):
        super().__init__()

        # dodanie klas
        self.add_classes_from_list(map(lambda x: x[1](),
                                       filter(lambda x: dnd3.creature_classes.Class != x[1] and issubclass(x[1], dnd3.creature_classes.Class),
                                              inspect.getmembers(dnd3.creature_classes, lambda x: inspect.isclass(x)))))

        # umiejętności
        if skills_xml is not None:
            self.add_skills_from_dict(dnd3.parsers.parse_skills(skills_xml))