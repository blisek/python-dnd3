__author__ = 'bartek'
import xml.etree.ElementTree as etree


TAG_NAME = 'name'
INDEX_FUNCTION = 1
INDEX_PROVIDER = 0


def generator_provider(attr, lambda_cond):
    return lambda c: lambda_cond(getattr(c, attr))


def generator_provider_skill(skill_name, lambda_cond):
    return lambda c: lambda_cond(c.skills[skill_name] if skill_name in c.skills else 0)


def generator_min(min_val):
    return lambda x: x >= min_val


def generator_max(max_val):
    return lambda x: x <= max_val


def generator_eq(val):
    return lambda x: x == val


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


def generator_set(attr_name, value):
    """ Zwraca Setter z metodami do ustawiania i wyłączania atutu
    :param attr_name: nazwa parametru
    :param value: wartość do ustawienia
    :return: (l1, l2) para funkcji pierwsza ustawia, druga przywraca
    """
    return lambda controller: AttributeSetter(controller, attr_name, value)


def generator_add(attr_name, value):
    return lambda c: AddSetter(c, attr_name, value)


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
        lambda_func = CONDITIONS_GENERATORS[tag][INDEX_FUNCTION](int(c.text))
        cond.append(CONDITIONS_GENERATORS[tag][INDEX_PROVIDER](name, lambda_func))
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
        eff = EFFECTS_GENERATORS[e.tag](name, text)
        setters.append(eff)
    return setters


def parse_triggers(element):
    triggers = []
    for t in element:
        pass
    return triggers