__author__ = 'bartek'
import functools
import xml.etree.ElementTree as etree
from dnd3.feats import ExternFeat, FeatDescription


TAG_NAME = 'name'
INDEX_FUNCTION = 1
INDEX_PROVIDER = 0


def generator_provider(attr, func, controller):
    val = getattr(controller, attr)
    return func(val)


def generator_provider_skill(skill_name, func, controller):
    val = controller.skills[skill_name] if skill_name in controller.skills else 0
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
            return None
        self.__setunset()

    def unset(self):
        if not self.is_on:
            return None
        self.__setunset()

    def __setunset(self):
        try:
            tmp = getattr(self.controller, self.attr_name)
            setattr(self.controller, self.attr_name, self.value)
            self.value = tmp
            self.is_on = not self.is_on
        except AttributeError:
            pass
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
    for t in element:
        pass
    return triggers


def parse_feats(file_like):
    tree = etree.parse(file_like)
    root_element = tree.getroot()
    feats = []
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
                    print(name)
                elif nn == 'desc':
                    desc = n.text
                    print(desc)
                elif nn == 'reqs':
                    reqs = n.text
                    print(reqs)
                elif nn == 'conditions':
                    conds = parse_conditions(n)
                    print(conds)
                elif nn == 'effects':
                    effects = parse_effects(n)
                    print(effects)
                elif nn == 'triggers':
                    triggers = parse_triggers(n)
                    print(triggers)
            feat_desc = FeatDescription(name, desc, reqs)
            feats.append(ExternFeat(sys_name, conds, effects, triggers, feat_desc))
        except:
            pass
    return feats
