__author__ = 'bartek'

P_NAME = 'name'
P_AGE = 'age'
P_CLASSES = 'classes'
P_FEATS = 'feats'
P_SKILLS = 'skills'
P_STR = 'STR'
P_DEX = 'DEX'
P_CON = 'CON'
P_INT = 'INT'
P_WIS = 'WIS'
P_CHA = 'CHA'


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
        self.classes = kwargs[P_CLASSES] if P_CLASSES in kwargs else dict()

        #atuty
        self.feats = kwargs[P_FEATS] if P_FEATS in kwargs else []

        # umiejętności
        self.skills = kwargs[P_SKILLS] if P_SKILLS in kwargs else dict()
