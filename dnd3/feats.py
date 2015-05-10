__author__ = 'bartek'
import dnd3.flags
import dnd3.controllers
import dnd3.models


class Feat:
    def __init__(self, system_name: str, passive: bool):
        self.sys_name = system_name
        self.passive = passive

    def get_flags(self) -> int:
        return 0

    def system_name(self) -> str:
        """ Zwraca nazwę systemową atutu
        :return: systemowa nazwa atutu
        """
        return self.sys_name

    def is_available_for(self, controller: dnd3.controllers.CreatureController) -> bool:
        """ Sprawdza czy postać spełnia wymagania atutu
        :param controller: kontroler postaci
        :return: True jeśli spełnia wymagania, inaczej False
        """
        raise NotImplementedError()

    def is_turned_on(self, controller: dnd3.controllers.CreatureController) -> bool:
        return self.sys_name in controller.model[dnd3.models.P_FEATS]

    def turn_on(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> bool:
        """ Aktywuje atut dla danej postaci
        :param controller: kontroler postaci
        :param args: dodatkowe argumenty
        :param kwargs: dodatkowe argumenty
        :return: True jeśli aktywowano atut, inaczej False
        """
        raise NotImplementedError()

    def turn_off(self, controller: dnd3.controllers.CreatureController, *args, **kwargs) -> bool:
        """ Dezaktywuje atut
        :param controller: kontroler postaci
        :param args: dodatkowe argumenty
        :param kwargs: dodatkowe argumenty
        :return: True jeśli aktywowano atut, inaczej False
        """
        raise NotImplementedError()

    def feat_description(self):
        """ Zwraca nazwę atutu
        :return: FeatDescription z tekstowym opisem atutu
        """
        raise NotImplementedError()

    def is_passive(self) -> bool:
        return self.passive

    def activate(self, controller: dnd3.controllers.CreatureController) -> None:
        pass

    def deactivate(self, controller: dnd3.controllers.CreatureController) -> None:
        pass


class FeatDescription:
    def __init__(self, name: str, description: str, requirements: str):
        self._name = name
        self._description = description
        self._requirements = requirements

    def name(self) -> str:
        return self._name

    def description(self) -> str:
        return self._description

    def requirements(self) -> str:
        return self._requirements


# Definicje atutów
class ExternFeat(Feat):
    def __init__(self, system_name: str, conditions: list, effects: list, triggers: list, description: FeatDescription):
        super().__init__(system_name, False)
        self.conditions = conditions
        self.effects = effects
        self.triggers = triggers
        self.description = description

    def get_flags(self) -> int:
        return dnd3.flags.F_ALLTIME

    def is_available_for(self, controller):
        return all(map(lambda x: x(controller), self.conditions))

    def turn_on(self, controller, *args, **kwargs):
        effects_prod = []
        for e in self.effects:
            tmp = e(controller)
            effects_prod.append(tmp)
            tmp.set()
        controller.feats_on[self.sys_name] = effects_prod

    def turn_off(self, controller, *args, **kwargs):
        if self.sys_name not in controller.feats_on:
            return None
        for e in controller.feats_on[self.sys_name]:
            e.unset()
        controller.feats_on[self.sys_name] = ()

    def feat_description(self):
        return self.description
