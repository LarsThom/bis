# last modified: 2023-05-03
# game version 7.2.1b
import sys
from docplex.mp.model import Model

list_critical = ['critical', 'crit', 'c']
list_alacrity = ['alacrity', 'alac', 'a']

# read accuracy, alacrity and implants
GOAL_ACCURACY = int(input("Enter Accuracy: "))
GOAL_ALACRITY = int(input("Enter Alacrity: "))

print("Implants: either 'critical'(also 'crit', 'c') or 'alacrity'(also 'alac', 'a')")
implant1 = input("Enter Implant 1: ").lower()
implant2 = input("Enter Implant 2: ").lower()
# if implant1 in list_critical:
#     Implants1Critical = 1
# elif implant1 in list_alacrity:
#     Implants1Alacrity = 1
# else:
#     sys.exit('ERROR: ILLEGAL IMPLANTS')
# if implant2 in list_critical:
#     Implants2Critical = 1
# elif implant2 in list_alacrity:
#     Implants2Alacrity = 1
# else:
#     sys.exit('ERROR: ILLEGAL IMPLANTS')

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


# read datafile and set correct values
# with open("./data.json", "r") as read_file:
#     data = json.load(read_file)

# accuracy_dict = {"Enhancements":0, "Augments":0, "Earpieces":0, "Stims":0}
# alacrity_dict = {"Enhancements":0, "Augments":0, "Earpieces":0, "Implants":0}
# critical_dict = {"Enhancements":0, "Augments":0, "Earpieces":0, "Implants":0, "Crystals":0}

# for x in accuracy_dict:
#     accuracy_dict[x] = data[x][0]['Accuracy']
# for x in alacrity_dict:
#     alacrity_dict[x] = data[x][0]['Alacrity']
# for x in critical_dict:
#     critical_dict[x] = data[x][0]['Critical']

# [accuracy_dict[x] = (data[x][0]['Accuracy']) for x in accuracy_dict]
# [alacrity_dict[x] = (data[x][0]['Alacrity']) for x in alacrity_dict]
# [critical_dict[x] = (data[x][0]['Critical']) for x in critical_dict]

# print(accuracy_dict)
# print(alacrity_dict)
# print(critical_dict)

# CONSTRAINT VALUES PATCH 7.2.1b:
# stim          biochem700:   264
# crystal       purple 136:   41
# enhancement   purple 336:   589
# earpiece      purple 336:   589
# implant       gold 334:     577
# augment       purple 74:    130
# augment       gold 77:      108

# set constraints
setAccuracy = m.sum([
    589*EnhancementsAccuracy,
    130*AugmentsAccuracy,
    589*EarpiecesAccuracy,
    264*StimsAccuracy
])
setAlacrity = m.sum([
    589*EnhancementsAlacrity,
    130*AugmentsAlacrity,
    # 589*EarpiecesAlacrity,
    577*Implants1Alacrity,
    577*Implants2Alacrity
])
setCritical = m.sum([
    589*EnhancementsCritical,
    130*AugmentsCritical,
    # 589*EarpiecesCritical,
    577*Implants1Critical,
    577*Implants2Critical,
    41*CrystalsCritical
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

CONSTRAINT_EARPIECE = m.add_constraint(m.sum(
    [EarpiecesAccuracy]) == 1, ctname='earpiece-constraint')
# [EarpiecesAccuracy, EarpiecesAlacrity, EarpiecesCritical]) == 1, ctname='earpiece-constraint')

# CONSTRAINT_IMPLANTS = m.add_constraint(m.sum(
#     [Implants1Alacrity, Implants1Critical, Implants2Alacrity, Implants2Critical]) == 2, ctname='implant-constraint')

CONSTRAINT_CRYSTAL = m.add_constraint(
    m.sum([CrystalsCritical]) == 2, ctname='earpiece-constraint')

if implants == "ac":
    print("ac")
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Critical]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Critical, Implants2Alacrity]) == 0, ctname='implant-constraint-rev')
elif implants == "cc":
    print("cc")
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Critical, Implants2Critical]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Alacrity]) == 0, ctname='implant-constraint-rev')
elif implants == "aa":
    print("aa")
    CONSTRAINT_IMPLANTS = m.add_constraint(
        m.sum([Implants1Alacrity, Implants2Alacrity]) == 2, ctname='implant-constraint')
    CONSTRAINT_IMPLANTS_REV = m.add_constraint(
        m.sum([Implants1Critical, Implants2Critical]) == 0, ctname='implant-constraint-rev')

# goal:
# m.set_multi_objective('min', [264*StimsAccuracy + 554*EnhancementsAccuracy + 130*AugmentsAccuracy + 554*EarpiecesAccuracy,
#     554*EnhancementsAlacrity + 130*AugmentsAlacrity + 554*EarpiecesAlacrity + 577*Implants1Alacrity + 577*Implants2Alacrity,
#     554*EnhancementsCritical + 130*AugmentsCritical + 554*EarpiecesCritical + 577*Implants1Critical + 577*Implants2Critical + 41*CrystalsCritical], weights = [1,1,0])

m.set_objective('max', 589*EnhancementsCritical + 130*AugmentsCritical +
                577*Implants1Critical + 577*Implants2Critical + 41*CrystalsCritical)
# m.set_objective('max', 589*EnhancementsCritical + 130*AugmentsCritical + 589 *
#                 EarpiecesCritical + 577*Implants1Critical + 577*Implants2Critical + 41*CrystalsCritical)

# solve and display
print("\n")
m.solve().display()
print("\nSolution values:")
print("Accuracy: ", setAccuracy.solution_value)
print("Alacrity: ", setAlacrity.solution_value)
print("Critical: ", setCritical.solution_value)
