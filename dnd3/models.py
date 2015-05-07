__author__ = 'bartek'

P_NAME = 'name'
P_AGE = 'age'
P_CLASSES = 'classes'
P_FEATS = 'feats'
P_SKILLS = 'skills'
P_STR = 'strength'
P_DEX = 'dexterity'
P_CON = 'constitution'
P_INT = 'intelligence'
P_WIS = 'wisdom'
P_CHA = 'charisma'
P_EFFECTS = 'effects'
P_SPECIAL_ABILITIES = 'special_abilities'
P_FORTITUDE = 'fortitude'
P_REFLEX = 'reflex'
P_WILL = 'will'
P_BASE_ATTACK = 'base_attack'
P_ARMOR_CLASS = 'ac'


class Creature:
    def __init__(self, **kwargs):
        self.name = kwargs[P_NAME] if P_NAME in kwargs else None
        self.age = kwargs[P_AGE] if P_AGE in kwargs else None

        # atrybuty
        self.strength = kwargs[P_STR] if P_STR in kwargs else None
        self.dexterity = kwargs[P_DEX] if P_DEX in kwargs else None
        self.constitution = kwargs[P_CON] if P_CON in kwargs else None
        self.intelligence = kwargs[P_INT] if P_INT in kwargs else None
        self.wisdom = kwargs[P_WIS] if P_WIS in kwargs else None
        self.charisma = kwargs[P_CHA] if P_CHA in kwargs else None


        #klasy
        # lista par (nazwa systemowa, poziom)
        self.classes = kwargs[P_CLASSES] if P_CLASSES in kwargs else list()

        #atuty
        self.feats = kwargs[P_FEATS] if P_FEATS in kwargs else []

        # umiejętności
        self.skills = kwargs[P_SKILLS] if P_SKILLS in kwargs else dict()

        # efekty różnych atutów, specjalnych zdolności
        self.effects = set(kwargs[P_EFFECTS]) if P_EFFECTS in kwargs else set()


class CreatureModel(dict):
    def __init__(self, **kwargs):
        super().__init__()

        self.__setitem__(P_NAME, kwargs[P_NAME] if P_NAME in kwargs else '')
        self.__setitem__(P_AGE, kwargs[P_AGE] if P_AGE in kwargs else None)

        # atrybuty
        self.__setitem__(P_STR, kwargs[P_STR] if P_STR in kwargs else 0)
        self.__setitem__(P_DEX, kwargs[P_DEX] if P_DEX in kwargs else 0)
        self.__setitem__(P_CON, kwargs[P_CON] if P_CON in kwargs else 0)
        self.__setitem__(P_INT, kwargs[P_INT] if P_INT in kwargs else 0)
        self.__setitem__(P_WIS, kwargs[P_WIS] if P_WIS in kwargs else 0)
        self.__setitem__(P_CHA, kwargs[P_CHA] if P_CHA in kwargs else 0)

        # KP
        self.__setitem__(P_ARMOR_CLASS, kwargs[P_ARMOR_CLASS] if P_ARMOR_CLASS in kwargs else 0)

        # rzuty obronne
        self.__setitem__(P_FORTITUDE, kwargs[P_FORTITUDE] if P_FORTITUDE in kwargs else 0)
        self.__setitem__(P_REFLEX, kwargs[P_REFLEX] if P_REFLEX in kwargs else 0)
        self.__setitem__(P_WILL, kwargs[P_WILL] if P_WILL in kwargs else 0)

        #klasy
        # lista par (nazwa systemowa, poziom)
        self.__setitem__(P_CLASSES, kwargs[P_CLASSES] if P_CLASSES in kwargs else list())

        #atuty
        self.__setitem__(P_FEATS, kwargs[P_FEATS] if P_FEATS in kwargs else list())

        # umiejętności
        self.__setitem__(P_SKILLS, kwargs[P_SKILLS] if P_SKILLS in kwargs else dict())

        # specjalne zdolności
        self.__setitem__(P_SPECIAL_ABILITIES, kwargs[P_SPECIAL_ABILITIES] if P_SPECIAL_ABILITIES in kwargs else dict())

        # efekty różnych atutów, specjalnych zdolności
        self.__setitem__(P_EFFECTS, set(kwargs[P_EFFECTS]) if P_EFFECTS in kwargs else set())