__author__ = 'bartek'


# A - alignment
A_LG = 'lawful_good'
A_LN = 'lawful_neutral'
A_LE = 'lawful_evil'
A_NG = 'neutral_good'
A_N = 'neutral'
A_NE = 'neutral_evil'
A_CG = 'chaotic_good'
A_CN = 'chaotic_neutral'
A_CE = 'chaotic_evil'

ALIGNMENT_FLAGS = {
    A_LG: 1,
    A_LN: 2,
    A_LE: 4,
    A_NG: 8,
    A_N: 16,
    A_NE: 32,
    A_CG: 64,
    A_CN: 128,
    A_CE: 256
}

A_ALL_CHAOTIC = ALIGNMENT_FLAGS[A_CE] | ALIGNMENT_FLAGS[A_CN] | ALIGNMENT_FLAGS[A_CG]
A_ALL_NEUTRAL = ALIGNMENT_FLAGS[A_N] | ALIGNMENT_FLAGS[A_NE] | ALIGNMENT_FLAGS[A_NG]
A_ALL_LAWFUL = ALIGNMENT_FLAGS[A_LE] | ALIGNMENT_FLAGS[A_LN] | ALIGNMENT_FLAGS[A_LG]
A_ALL_ALIGNMENTS = A_ALL_CHAOTIC | A_ALL_NEUTRAL | A_ALL_LAWFUL

# T - time
T_ROUND = 'round'
T_TOUR = 'tour'
T_HOUR = 'hour'

# F - feats
F_ALLTIME = 1
F_FIGHT = 2
F_LIMITED_DURATION = 32768

# E - keys in extra return arguments
E_NEW_FEATS = 'new_feats'  # zbiór
E_NEW_SPECA = 'new_speca'  # zbiór
E_FEATS_NUM = 'feats_num'  # liczba
E_SKILLS_NUM = 'skills_num'  # liczba
E_LANGUAGES = 'languages'  # zbiór
E_LANGUAGES_NUM = 'languages_num'  # liczba
