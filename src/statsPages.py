from database import *
from settings import *
 
def getStatsPages(language):
    stats = {
        1: [
            getText(language, 'stat_1'),
            getText(language, 'stat_1_1'), str(getStat("wins_easy")),
            getText(language, 'stat_1_2'), str(getStat("wins_medium")),
            getText(language, 'stat_1_3'), str(getStat("wins_hard")),
            getText(language, 'stat_1_4'), str(getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard"))
        ],
        2: [
            getText(language, 'stat_2'),
            getText(language, 'stat_2_1'), getTime(getStat("time_easy")),
            getText(language, 'stat_2_2'), getTime(getStat("time_medium")),
            getText(language, 'stat_2_3'), getTime(getStat("time_hard")),
            getText(language, 'stat_2_4'), getTime(getStat("time_total")),
        ]
    }
    return stats