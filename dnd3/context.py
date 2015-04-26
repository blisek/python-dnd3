__author__ = 'bartek'


class Context:
    def __init__(self):
        self.feats = []

    def add_feats(self, iterator):
        self.feats.extend(iterator)

    def get_feats(self):
        """ Zwraca iterator do listy atutów tego kontekstu w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return iter(self.feats)

    def get_feats_available_for_creature(self, controller):
        """ Zwraca iterator do listy atutów tego kontekstu, których wymagania spełnia kontroler, w nieokreślonym porządku
        :return: iterator do listy z atutami
        """
        return filter(lambda l: l.is_available_for(controller), self.feats)