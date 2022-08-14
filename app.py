import sys
import json
from docplex.mp.model import Model
from docplex.mp.relax_linear import LinearRelaxer

# read accuracy, alacrity and implants

GOAL_ACCURACY = int(input("Enter Accuracy: "))
GOAL_ALACRITY = int(input("Enter Alacrity: "))
print("Implants: either critical(also crit, c) or alacrity(also alac, a")
IMPLANT1 = input("Enter Implant 1: ").lower()
IMPLANT2 = input("Enter Implant 2: ").lower()

# define model
m = Model(name='SWTOR 7.1')

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

list_critical = ['critical', 'crit', 'c']
list_alacrity = ['alacrity', 'alac', 'a']

if IMPLANT1 in list_alacrity:
    if IMPLANT2 in list_alacrity:
        Implants1Alacrity = 1
        Implants1Critical = 0
        Implants2Alacrity = 1
        Implants2Critical = 0
    elif IMPLANT2 in list_critical:
        Implants1Alacrity = 1
        Implants1Critical = 0
        Implants2Alacrity = 0
        Implants2Critical = 1
elif IMPLANT1 in list_critical:
    if IMPLANT2 in list_alacrity:
        Implants1Alacrity = 0
        Implants1Critical = 1
        Implants2Alacrity = 1
        Implants2Critical = 0
    elif IMPLANT2 in list_critical:
        Implants1Alacrity = 0
        Implants1Critical = 1
        Implants2Alacrity = 0
        Implants2Critical = 1
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



# set constraints
setAccuracy = m.sum([
    554*EnhancementsAccuracy,
    130*AugmentsAccuracy,
    554*EarpiecesAccuracy,
    264*StimsAccuracy
    ])
setAlacrity = m.sum([
    554*EnhancementsAlacrity,
    130*AugmentsAlacrity,
    554*EarpiecesAlacrity,
    577*Implants1Alacrity,
    577*Implants2Alacrity
    ])
setCritical = m.sum([
    554*EnhancementsCritical,
    130*AugmentsCritical,
    554*EarpiecesCritical,
    577*Implants1Critical,
    577*Implants2Critical,
    41*CrystalsCritical
    ])

CONSTRAINT_ACCURACY = m.add_constraint(setAccuracy >= GOAL_ACCURACY, ctname='accuracy-constraint')

CONSTRAINT_ALACRITY = m.add_constraint(setAlacrity >= GOAL_ALACRITY, ctname='alacrity-constraint')

CONSTRAINT_CRITICAL = m.add_constraint(setCritical >= 0, ctname='critical-constraint')

CONSTRAINT_ENHANCEMENTS = m.add_constraint(m.sum([EnhancementsAccuracy, EnhancementsAlacrity, EnhancementsCritical]) == 7, ctname='enhancement-constraint')

CONSTRAINT_AUGMENTS = m.add_constraint(m.sum([AugmentsAccuracy, AugmentsAlacrity, AugmentsCritical]) == 14, ctname='augment-constraint')

CONSTRAINT_EARPIECE = m.add_constraint(m.sum([EarpiecesAccuracy, EarpiecesAlacrity, EarpiecesCritical]) == 1, ctname='earpiece-constraint')

CONSTRAINT_CRYSTAL = m.add_constraint(m.sum([CrystalsCritical]) == 2, ctname='earpiece-constraint')


# goal:
m.set_multi_objective('min', [264*StimsAccuracy + 554*EnhancementsAccuracy + 130*AugmentsAccuracy + 554*EarpiecesAccuracy,
    554*EnhancementsAlacrity + 130*AugmentsAlacrity + 554*EarpiecesAlacrity + 577*Implants1Alacrity + 577*Implants2Alacrity,
    554*EnhancementsCritical + 130*AugmentsCritical + 554*EarpiecesCritical + 577*Implants1Critical + 577*Implants2Critical + 41*CrystalsCritical], weights = [1,1,0])
    
# solve and display
print("\n")
m.solve().display()
print("\nSolution values:")
print("Accuracy: ", setAccuracy.solution_value)
print("Alacrity: ", setAlacrity.solution_value)
print("Critical: ", setCritical.solution_value)