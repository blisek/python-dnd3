__author__ = 'bartek'
import dnd3.models as models


P_FEATS_ON = 'feats_on'

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
        :type model: dnd3.models.CreatureModel
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

        self.fortitude = None
        self.reflex = None
        self.will = None

        # słownik atutów, które zostały aktywowane na tym modelu
        self.feats_on = dict()

    def strength_mod(self, reload=False):
        """ Zwraca modyfikator z siły
        :param reload: jeśli True modyfikator zostanie ponownie wyliczony
        :return: modyfikator z siły
        """
        if self.s_mod is None or reload:
            self.s_mod = ability_mod_calc(self.model[models.P_STR])
        return self.s_mod

    def dexterity_mod(self, reload=False):
        """ Zwraca modyfikator ze zręczności
        :param reload: jeśli True modyfikator zostanie ponownie wyliczony
        :return: modyfikator ze zręczności
        """
        if self.dex_mod is None or reload:
            self.dex_mod = ability_mod_calc(self.model[models.P_DEX])
        return self.dex_mod

    def constitution_mod(self, reload=False):
        if self.con_mod is None or reload:
            self.con_mod = ability_mod_calc(self.model[models.P_CON])
        return self.con_mod

    def intelligence_mod(self, reload=False):
        if self.int_mod is None or reload:
            self.int_mod = ability_mod_calc(self.model[models.P_INT])
        return self.int_mod

    def wisdom_mod(self, reload=False):
        if self.wis_mod is None or reload:
            self.wis_mod = ability_mod_calc(self.model[models.P_WIS])
        return self.wis_mod

    def charisma_mod(self, reload=False):
        if self.cha_mod is None or reload:
            self.cha_mod = ability_mod_calc(self.model[models.P_CHA])
        return self.cha_mod

    def get_feats_on(self):
        for feat in self.model.feats:
            pass

    def st_fortitude(self, reload=False):
        if self.fortitude is None or reload:
            self.fortitude = sum(map(lambda x: x[1], filter(lambda x: x[0].startswith(models.P_FORTITUDE), self.model.items())))
        return self.fortitude

    def st_reflex(self, reload=False):
        if self.reflex is None or reload:
            self.reflex = sum(map(lambda x: x[1], filter(lambda x: x[0].startswith(models.P_REFLEX), self.model.items())))
        return self.reflex

    def st_will(self, reload=False):
        if self.will is None or reload:
            self.will = sum(map(lambda x: x[1], filter(lambda x: x[0].startswith(models.P_WILL), self.model.items())))
        return self.will

    def ac_total(self, reload=False):
