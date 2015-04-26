__author__ = 'bartek'


def ability_mod_calc(val):
    """ Wylicza modyfikator dla danego atrybutu.
    :param val: wartość atrybutu
    :return: modyfikator
    """
    if val >= 1:
        return (val - 10) // 2
    else:
        return -5


class CreatureController:
    def __init__(self, model):
        """ Tworzy kontroler dla modelu Creature
        :type model: dnd3.models.Creature
        :param model: model
        :return:
        """
        self.model = model

        self.s_mod = None
        self.dex_mod = None
        self.con_mod = None
        self.int_mod = None
        self.wis_mod = None
        self.cha_mod = None

    def strength_mod(self, reload=False):
        """ Zwraca modyfikator z siły
        :param reload: jeśli True modyfikator zostanie ponownie wyliczony
        :return: modyfikator z siły
        """
        if self.s_mod is None or reload:
            self.s_mod = ability_mod_calc(self.model.strength)
        return self.s_mod

    def dexterity_mod(self, reload=False):
        """ Zwraca modyfikator ze zręczności
        :param reload: jeśli True modyfikator zostanie ponownie wyliczony
        :return: modyfikator ze zręczności
        """
        if self.dex_mod is None or reload:
            self.dex_mod = ability_mod_calc(self.model.dexterity)
        return self.dex_mod

    def constitution_mod(self, reload=False):
        if self.con_mod is None or reload:
            self.con_mod = ability_mod_calc(self.model.constitution)
        return self.con_mod

    def intelligence_mod(self, reload=False):
        if self.int_mod is None or reload:
            self.int_mod = ability_mod_calc(self.model.intelligence)
        return self.int_mod

    def wisdom_mod(self, reload=False):
        if self.wis_mod is None or reload:
            self.wis_mod = ability_mod_calc(self.model.wisdom)
        return self.wis_mod

    def charisma_mod(self, reload=False):
        if self.cha_mod is None or reload:
            self.cha_mod = ability_mod_calc(self.model.charisma)
        return self.cha_mod

    def feats_on(self):
        for feat in self.model.feats:
            pass