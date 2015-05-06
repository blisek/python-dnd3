import collections

# shouldn't be changed
SP_SYSTEM_NAME = 'system_name'
SP_NAME = 'name'
SP_DESCRIPTION = 'desc'
SP_KEY_ABILITY = 'key_ability'
SP_SYNERGY = 'synergy'
SP_SYNERGIES = 'synergies'
SP_MIN_RANK = 'min_rank'
SP_TEST_BONUS = 'test_bonus'
SP_RESTRICTED = 'restricted'

Skill = collections.namedtuple('Skill', [SP_SYSTEM_NAME, SP_NAME, SP_DESCRIPTION, SP_KEY_ABILITY, SP_RESTRICTED,
                                         SP_SYNERGIES])
Synergy = collections.namedtuple('Synergy', [SP_NAME, SP_MIN_RANK, SP_TEST_BONUS])

