import shelve
import os

# INITIALIZE
STATS_DB = shelve.open(os.path.join("../data", "stats"))
OPTIONS_DB = shelve.open(os.path.join("../data", "options"))

# FUNCTIONS
# Options
def optionsValues(option, invert=False, new_value=None):
    option = str(option)
    try:
        value = OPTIONS_DB[option]
    except:  # No such option saved in database, so create new value
        if option == "0" or option == "1":
            value = 0.5
        else:
            value = True

    if invert:
        value = not value
        OPTIONS_DB[option] = value
    elif new_value is not None:
        value = new_value
        OPTIONS_DB[option] = value
    else:  # if value wasn't changed, returns it
        return value

# Stats
def getStat(stat):
    try:
        # If database already has high_score entry
        value = STATS_DB[stat]
    except:
        value = 0
    return value


def saveStat(stat, new_value, compare=0):
    if compare:
        # Replace stat with value if new value is higher
        if new_value > getStat(stat):
            STATS_DB[stat] = new_value
    else:
        # Add new value to old stat value
        STATS_DB[stat] = getStat(stat) + new_value

def closeDB():
    STATS_DB.close()
    OPTIONS_DB.close()