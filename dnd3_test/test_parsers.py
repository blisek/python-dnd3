__author__ = 'bartek'
import unittest
import dnd3.parsers as pars
import dnd3.models as mod
import dnd3.controllers as con


class ParsersTest(unittest.TestCase):
    def test_parse_feats(self):
        feats = pars.parse_feats('test_feats.xml')
        self.assertEqual(len(feats), 2)
        abilities, model, controller = self.get_controller1()
        pierwszy = feats['pierwszy']
        self.assertFalse(pierwszy.is_available_for(controller))
        model.skills['blefowanie'] = 5
        self.assertTrue(pierwszy.is_available_for(controller))
        feats['pierwszy'].turn_on(controller)
        self.assertEqual(model.constitution, 14)
        self.assertEqual(model.dexterity, 10)
        self.assertEqual(model.charisma, 18)
        feats['drugi'].turn_on(controller)
        self.assertEqual(model.charisma, 1)

    def test_parse_skills(self):
        skills = pars.parse_skills('test_skills.xml')
        self.assertEqual(len(skills), 2)
        abilities, model, controller = self.get_controller1()
        pierwsza = skills['skill_1']
        model.intelligence = 16
        self.assertEqual(pierwsza.key_ability(controller, True), 3)
        druga = skills['skill_2']
        self.assertEqual(druga.key_ability(controller, True), 1)
        self.assertEqual(druga.synergies[0].name, pierwsza.system_name)
        self.assertEqual(druga.synergies[0].min_rank, 5)
        self.assertEqual(druga.synergies[0].test_bonus, 2)

    def get_controller1(self):
        d = {mod.P_STR: 12, mod.P_DEX: 12, mod.P_CON: 12, mod.P_INT: 12,
             mod.P_WIS: 12, mod.P_CHA: 12}
        model = mod.Creature(**d)
        controller = con.CreatureController(model)
        return d, model, controller


if __name__ == "__main__":
    unittest.main()