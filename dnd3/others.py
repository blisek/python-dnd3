__author__ = 'bartek'
import collections

L_SYSTEM_NAME = 'system_name'
L_NAME = 'name'
L_DESCRIPTION = 'desc'

Language = collections.namedtuple('Language', [L_SYSTEM_NAME, L_NAME, L_DESCRIPTION])

L_COMMON = 'common'
L_DWARVEN = 'dwarven'
L_ELVEN = 'elven'

STANDARD_LANGUAGES = [
    Language(L_COMMON, 'wspólny', ''),
    Language(L_DWARVEN, 'krasnoludzki', ''),
    Language(L_ELVEN, 'elfi', '')
]

S_SYSTEM_NAME = 'system_name'
S_NAME = 'name'
S_ATTACK_AC_MOD = 'att_ac_mod'
S_SPECIAL_ATTACK_MODIFIER = 'spec_att_mod'
S_HIDE_MODIFIER = 'hide_modifier'

Size = collections.namedtuple('Size', [S_SYSTEM_NAME, S_NAME, S_ATTACK_AC_MOD,
                                       S_SPECIAL_ATTACK_MODIFIER, S_HIDE_MODIFIER])

S_MEDIUM = 'medium'

SIZES = [
    Size('fine', 'filigranowy', 8, -16, 16),
    Size('diminutive', 'drobny', 4, -12, 12),
    Size('tiny', 'malutki', 2, -8, 8),
    Size('small', 'mały', 1, -4, 4),
    Size(S_MEDIUM, 'średni', 0, 0, 0),
    Size('large', 'duży', -1, 4, -4),
    Size('huge', 'olbrzymi', -2, 8, -8),
    Size('gargantuan', 'gigantyczny', -4, 12, -12),
    Size('colossal', 'kolosalny', -8, 16, -16)
]