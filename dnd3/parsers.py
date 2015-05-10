__author__ = 'bartek'
import functools
import xml.etree.ElementTree
import dnd3.feats
import dnd3.controllers
import dnd3.skills


TAG_NAME = 'name'
INDEX_FUNCTION = 1
INDEX_PROVIDER = 0


def generator_provider(attr, func, controller):
    val = None
    if hasattr(controller, attr):
        val = getattr(controller, attr)
    else:
        val = getattr(controller.model, attr)
    return func(val)


def generator_provider_skill(skill_name, func, controller):
    val = controller.model.skills[skill_name] if skill_name in controller.model.skills else 0
    return func(val)


def generator_min(min_val, val):
    return min_val <= val


def generator_max(max_val, val):
    return max_val >= val


def generator_eq(eq_val, val):
    return eq_val == val


class Setter:
    def __init__(self):
        self.is_on = False

    def set(self):
        raise NotImplementedError()

    def unset(self):
        raise NotImplementedError()

    def is_it_on(self):
        return self.is_on


class AttributeSetter(Setter):
    def __init__(self, controller, attr_name, value):
        super().__init__()
        self.controller = controller
        self.attr_name = attr_name
        self.value = value

    def set(self):
        if self.is_on:
            return
        self.__setunset()

    def unset(self):
        if not self.is_on:
            return
        self.__setunset()

    def __setunset(self):
        if hasattr(self.controller, self.attr_name):
            tmp = getattr(self.controller, self.attr_name)
            setattr(self.controller, self.attr_name, self.value)
            self.value = tmp
            self.is_on = not self.is_on
        else:
            tmp = getattr(self.controller.model, self.attr_name)
            setattr(self.controller.model, self.attr_name, self.value)
            self.value = tmp
            self.is_on = not self.is_on


class AddSetter(Setter):
    def __init__(self, controller, attr_name, value):
        super().__init__()
        self.controller = controller
        self.attr_name = attr_name
        self.value = value

    def set(self):
        if self.is_on:
            return None
        try:
            tmp = getattr(self.controller, self.attr_name, 0)
            setattr(self.controller, self.attr_name, tmp + self.value)
            self.is_on = True
        except AttributeError:
            pass
        else:
            tmp = getattr(self.controller.model, self.attr_name, 0)
            setattr(self.controller.model, self.attr_name, tmp + self.value)
            self.is_on = True

    def unset(self):
        if not self.is_on:
            return None
        try:
            tmp = getattr(self.controller, self.attr_name, 0)
            setattr(self.controller, self.attr_name, tmp - self.value)
            self.is_on = False
        except AttributeError:
            pass
        else:
            tmp = getattr(self.controller.model, self.attr_name, 0)
            setattr(self.controller.model, self.attr_name, tmp - self.value)
            self.is_on = False


def generator_set(attr_name, value, controller):
    """ Zwraca Setter z metodami do ustawiania i wyłączania atutu
    :param attr_name: nazwa parametru
    :param value: wartość do ustawienia
    :return: Setter
    """
    return AttributeSetter(controller, attr_name, value)


def generator_add(attr_name, value, controller):
    return AddSetter(controller, attr_name, value)


CONDITIONS_GENERATORS = {
    'min': (generator_provider, generator_min),
    'max': (generator_provider, generator_max),
    'eq': (generator_provider, generator_eq),
    'min_skill': (generator_provider_skill, generator_min)
}


EFFECTS_GENERATORS = {
    'set': generator_set,
    'add': generator_add
}


def parse_conditions(element):
    cond = []
    for c in element:
        tag = c.tag
        if tag not in CONDITIONS_GENERATORS:
            continue
        name = c.attrib[TAG_NAME]
        func = functools.partial(CONDITIONS_GENERATORS[tag][INDEX_FUNCTION], int(c.text))
        provider = functools.partial(CONDITIONS_GENERATORS[tag][INDEX_PROVIDER], name, func)
        cond.append(provider)
    return cond


def parse_effects(element):
    setters = []
    for e in element:
        if e.tag not in EFFECTS_GENERATORS:
            continue
        name = e.attrib[TAG_NAME]
        text = e.text
        try:
            text = int(text)
        except ValueError:
            pass
        eff = functools.partial(EFFECTS_GENERATORS[e.tag], name, text)
        setters.append(eff)
    return setters


def parse_triggers(element):
    triggers = []
    for _ in element:
        pass
    return triggers


def parse_feats(file_like):
    tree = xml.etree.ElementTree.parse(file_like)
    root_element = tree.getroot()
    feats = dict()
    if root_element.tag.lower() != 'feats':
        return feats
    for element in root_element:
        try:
            if element.tag.lower() != 'feat':
                continue
            sys_name = element.attrib['system_name']
            name, desc, reqs, effects, conds, triggers = None, None, None, None, None, None
            for n in element:
                nn = n.tag.lower()
                if nn == 'name':
                    name = n.text
                elif nn == 'desc':
                    desc = n.text
                elif nn == 'reqs':
                    reqs = n.text
                elif nn == 'conditions':
                    conds = parse_conditions(n)
                elif nn == 'effects':
                    effects = parse_effects(n)
                elif nn == 'triggers':
                    triggers = parse_triggers(n)
            feat_desc = dnd3.feats.FeatDescription(name, desc, reqs)
            feats[sys_name] = dnd3.feats.ExternFeat(sys_name, conds, effects, triggers, feat_desc)
        except:
            pass
    return feats


def parse_skills(file_like):
    tree = xml.etree.ElementTree.parse(file_like)
    root = tree.getroot()
    skill_dict = dict()
    if root.tag.lower() != 'skills':
        return skill_dict
    for se in root:
        try:
            if se.tag.lower() != 'skill':
                continue
            sys_name = se.attrib['system_name']
            s_params = dict()
            name, desc, restricted, synergies = None, None, None, []
            for n in se:
                nn = n.tag.lower()
                if nn == dnd3.skills.SP_NAME.lower():
                    name = n.text
                elif nn == dnd3.skills.SP_DESCRIPTION.lower():
                    desc = n.text
                elif nn == dnd3.skills.SP_KEY_ABILITY.lower():
                    s_params[dnd3.skills.SP_KEY_ABILITY] = getattr(dnd3.controllers.CreatureController, n.text + '_mod')
                elif nn == dnd3.skills.SP_RESTRICTED.lower():
                    restricted = bool(n.text)
                elif nn == dnd3.skills.SP_SYNERGIES.lower():
                    for s in n:
                        if s.tag.lower() != dnd3.skills.SP_SYNERGY.lower():
                            continue
                        d = dict(s.attrib)
                        d[dnd3.skills.SP_MIN_RANK] = int(d[dnd3.skills.SP_MIN_RANK])
                        d[dnd3.skills.SP_TEST_BONUS] = int(d[dnd3.skills.SP_TEST_BONUS])
                        synergies.append(dnd3.skills.Synergy(**d))
            s_params[dnd3.skills.SP_SYSTEM_NAME] = sys_name
            s_params[dnd3.skills.SP_NAME] = name
            s_params[dnd3.skills.SP_DESCRIPTION] = desc
            s_params[dnd3.skills.SP_RESTRICTED] = restricted
            s_params[dnd3.skills.SP_SYNERGIES] = tuple(synergies)
            skill_dict[sys_name] = dnd3.skills.Skill(**s_params)
        except Exception as err:
            print(err)
    return skill_dict


def parse_classes(file_like):
    pass