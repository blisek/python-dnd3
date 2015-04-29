import collections

# shouldn't be changed
SP_NAME = 'name'
SP_DESCRIPTION = 'desc'
SP_KEY_ABILITY = 'key_ability'
SP_SYNERGY = 'synergy'
SP_SYNERGIES = 'synergies'
SP_MIN_RANK = 'min_rank'
SP_TEST_BONUS = 'test_bonus'

Skill = collections.namedtuple('Skill', [SP_NAME, SP_DESCRITPION, SP_KEY_ABILITY, SP_SYNERGIES])
Synergy = collections.namedtuple('Synergy', [SP_NAME, SP_MIN_RANK, SP_TEST_BONUS])

