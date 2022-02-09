from database import *
from settings import *
 
def getTrophiesPages(language):
    trophies = {
        1: [
            [
                getText(language, 'trophy_1'),
                getText(language, 'trophy_1_1'),
                10 > getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard"),
            ],
            [
                getText(language, 'trophy_2'),
                getText(language, 'trophy_2_1'),
                50 > getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard"),
            ],
            [
                getText(language, 'trophy_3'),
                getText(language, 'trophy_3_1'),
                100 > getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard"),
            ],
        ],
        2: [
            [
                getText(language, 'trophy_4'),
                getText(language, 'trophy_4_1'),
                120 < getStat("time_easy") or 0 == getStat('time_easy'),
            ],
            [
                getText(language, 'trophy_5'),
                getText(language, 'trophy_5_1'),
                90 < getStat("time_easy") or 0 == getStat('time_easy'),
            ],
            [
                getText(language, 'trophy_6'),
                getText(language, 'trophy_6_1'),
                60 < getStat("time_easy") or 0 == getStat('time_easy'),
            ],
        ],
        3: [
            [
                getText(language, 'trophy_7'),
                getText(language, 'trophy_7_1'),
                600 < getStat("time_medium") or 0 == getStat('time_medium'),
            ],
            [
                getText(language, 'trophy_8'),
                getText(language, 'trophy_8_1'),
                450 < getStat("time_medium") or 0 == getStat('time_medium'),
            ],
            [
                getText(language, 'trophy_9'),
                getText(language, 'trophy_9_1'),
                300 < getStat("time_medium") or 0 == getStat('time_medium'),
            ],
        ],
        4: [
            [
                getText(language, 'trophy_10'),
                getText(language, 'trophy_10_1'),
                1800 < getStat("time_hard") or 0 == getStat('time_hard'),
            ],
            [
                getText(language, 'trophy_11'),
                getText(language, 'trophy_11_1'),
                1200 < getStat("time_hard") or 0 == getStat('time_hard'),
            ],
            [
                getText(language, 'trophy_12'),
                getText(language, 'trophy_12_1'),
                600 < getStat("time_hard") or 0 == getStat('time_hard'),
            ],
        ],
    }
    return trophies