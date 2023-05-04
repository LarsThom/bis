# last modified: 2023-05-03
# game version 7.2.1b

# maximizing crit while minimizing overflow of accuracy and alacrity

import sys
import json
from docplex.mp.model import Model

list_critical = ['critical', 'crit', 'c']
list_alacrity = ['alacrity', 'alac', 'a']

# read accuracy, alacrity and implants
GOAL_ACCURACY = int(input("Enter Accuracy: "))
GOAL_ALACRITY = int(input("Enter Alacrity: "))

print("Implants: either 'critical'(also 'crit', 'c') or 'alacrity'(also 'alac', 'a')")
implant1 = input("Enter Implant 1: ").lower()
implant2 = input("Enter Implant 2: ").lower()

print("Possible Earpieces: either 'critical', 'alacrity' or 'accuracy'. Can be blank.")
earpiece = input("Enter desired Earpiece: ").lower()

# define model
m = Model(name='SWTOR 7.2.1b')

# set variables
EnhancementsAccuracy = m.integer_var(name='accuracy-enhancement', lb=0)
EnhancementsAlacrity = m.integer_var(name='alacrity-enhancement', lb=0)
EnhancementsCritical = m.integer_var(name='critical-enhancement', lb=0)

AugmentsAccuracy = m.integer_var(name='accuracy-augment', lb=0)
AugmentsAlacrity = m.integer_var(name='alacrity-augment', lb=0)
AugmentsCritical = m.integer_var(name='critical-augment', lb=0)

EarpiecesAccuracy = m.binary_var(name='accuracy-earpiece')
EarpiecesAlacrity = m.binary_var(name='alacrity-earpiece')
EarpiecesCritical = m.binary_var(name='critical-earpiece')

Implants1Alacrity = m.binary_var(name='alacrity-implant-1')
Implants1Critical = m.binary_var(name='critical-implant-1')
Implants2Alacrity = m.binary_var(name='alacrity-implant-2')
Implants2Critical = m.binary_var(name='critical-implant-2')

StimsAccuracy = m.binary_var(name='accuracy-stim')

CrystalsCritical = m.integer_var(name='critical-crystal')

# set implant configuration
if implant1 in list_alacrity:
    if implant2 in list_alacrity:
        implants = "aa"
    elif implant2 in list_critical:
        implants = "ac"
elif implant1 in list_critical:
    if implant2 in list_alacrity:
        implants = "ac"
    elif implant2 in list_critical:
        implants = "cc"
else:
    sys.exit('ERROR: ILLEGAL IMPLANTS')

# CONSTRAINT VALUES PATCH 7.2.1b:
# stim          biochem700:   264
# crystal       purple 136:   41
# enhancement   purple 336:   589
# earpiece      purple 336:   589
# implant       gold 334:     577
# augment       gold 77:      130

# read datafile and set correct values
data = json.loads(open('data.json').read())

VAL_ENHANCEMENT = data['Gear'][0]['Enhancement']
VAL_AUGMENT = data['Gear'][0]['Augment']
VAL_EARPIECE = data['Gear'][0]['Earpiece']
VAL_IMPLANT = data['Gear'][0]['Implant']
VAL_CRYSTAL = data['Gear'][0]['Crystal']
VAL_STIM = data['Gear'][0]['Stim']

# set constraints
setAccuracy = m.sum([
    VAL_ENHANCEMENT * EnhancementsAccuracy,
    VAL_AUGMENT * AugmentsAccuracy,
    VAL_EARPIECE * EarpiecesAccuracy,
    VAL_STIM * StimsAccuracy
])
setAlacrity = m.sum([
    VAL_ENHANCEMENT * EnhancementsAlacrity,
    VAL_AUGMENT * AugmentsAlacrity,
    VAL_EARPIECE * EarpiecesAlacrity,
    VAL_IMPLANT * Implants1Alacrity,
    VAL_IMPLANT * Implants2Alacrity
])
setCritical = m.sum([
    VAL_ENHANCEMENT * EnhancementsCritical,
    VAL_AUGMENT * AugmentsCritical,
    VAL_EARPIECE * EarpiecesCritical,
    VAL_IMPLANT * Implants1Critical,
    VAL_IMPLANT * Implants2Critical,
    VAL_CRYSTAL * CrystalsCritical
])

CONSTRAINT_ACCURACY = m.add_constraint(
    setAccuracy >= GOAL_ACCURACY, ctname='accuracy-constraint')

CONSTRAINT_ALACRITY = m.add_constraint(
    setAlacrity >= GOAL_ALACRITY, ctname='alacrity-constraint')

CONSTRAINT_CRITICAL = m.add_constraint(
    setCritical >= 0, ctname='critical-constraint')

CONSTRAINT_ENHANCEMENTS = m.add_constraint(m.sum(
    [EnhancementsAccuracy, EnhancementsAlacrity, EnhancementsCritical]) == 7, ctname='enhancement-constraint')

CONSTRAINT_AUGMENTS = m.add_constraint(m.sum(
    [AugmentsAccuracy, AugmentsAlacrity, AugmentsCritical]) == 14, ctname='augment-constraint')

if earpiece == "alacrity":
    CONSTRAINT_EARPIECE = m.add_constraint(
        m.sum([EarpiecesAlacrity]) == 1, ctname='earpiece-constraint')
    CONSTRAINT_EARPIECE_REV = m.add_constraint(m.sum(
        [EarpiecesAccuracy, EarpiecesCritical]) == 0, ctname='earpiece-constraint-rev')
elif earpiece == "accuracy":
    CONSTRAINT_EARPIECE = m.add_constraint(
        m.sum([EarpiecesAccuracy]) == 1, ctname='earpiece-constraint')
    CONSTRAINT_EARPIECE_REV = m.add_constraint(m.sum(
        [EarpiecesAlacrity, EarpiecesCritical]) == 0, ctname='earpiece-constraint-rev')
elif earpiece == "critical":
    CONSTRAINT_EARPIECE = m.add_constraint(
        m.sum([EarpiecesCritical]) == 1, ctname='earpiece-constraint')
    CONSTRAINT_EARPIECE = m.add_constraint(m.sum(
        [EarpiecesAlacrity, EarpiecesAccuracy]) == 0, ctname='earpiece-constraint-rev')
elif earpiece == "":
    CONSTRAINT_EARPIECE = m.add_constraint(m.sum(
        [EarpiecesCritical, EarpiecesAccuracy, EarpiecesAlacrity]) == 1, ctname='earpiece-constraint')
else:
    sys.exit("ERROR: ILLEGAL EARPIECE")

CONSTRAINT_CRYSTAL = m.add_constraint(
    m.sum([CrystalsCritical]) == 2, ctname='earpiece-constraint')

if implants == "ac":
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Critical]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Critical, Implants2Alacrity]) == 0, ctname='implant-constraint-rev')
elif implants == "cc":
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Critical, Implants2Critical]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Alacrity]) == 0, ctname='implant-constraint-rev')
elif implants == "aa":
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Alacrity]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Critical, Implants2Critical]) == 0, ctname='implant-constraint-rev')

# set goal:
m.set_objective('max',
                VAL_ENHANCEMENT * EnhancementsCritical +
                VAL_AUGMENT * AugmentsCritical +
                VAL_EARPIECE * EarpiecesCritical +
                VAL_IMPLANT * Implants1Critical +
                VAL_IMPLANT * Implants2Critical +
                VAL_CRYSTAL * CrystalsCritical
                )

# solve and display
print("\n")
m.solve().display()
print("\nSolution values:")
print("Accuracy: ", setAccuracy.solution_value)
print("Alacrity: ", setAlacrity.solution_value)
print("Critical: ", setCritical.solution_value)
