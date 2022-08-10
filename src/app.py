import sys
from docplex.mp.model import Model

# set accuracy and alacrity goals
GOAL_ACCURACY = 2694
GOAL_ALACRITY = 2100

# set implants: 'accuracy', 'alacrity' or 'critical'
IMPLANT1 = 'alacrity'
IMPLANT2 = 'critical'

# define model
m = Model(name='SWTOR 7.1 BiS calc')

# set variables
ENHANCEMENT_ACCU = m.integer_var(name='accuracy-enhancement', lb=0)
ENHANCEMENT_ALAC = m.integer_var(name='alacrity-enhancement', lb=0)
ENHANCEMENT_CRIT = m.integer_var(name='critical-enhancement', lb=0)

AUGMENT77_ACCU = m.integer_var(name='accuracy-augment-gold', lb=0)
AUGMENT77_ALAC = m.integer_var(name='alacrity-augment-gold', lb=0)
AUGMENT77_CRIT = m.integer_var(name='critical-augment-gold', lb=0)

EARPIECE_ACCU = m.binary_var(name='accuracy-earpiece')
EARPIECE_ALAC = m.binary_var(name='alacrity-earpiece')
EARPIECE_CRIT = m.binary_var(name='critical-earpiece')

IMPLANT1_ALAC = m.binary_var(name='alacrity-implant-1')
IMPLANT1_CRIT = m.binary_var(name='critical-implant-1')
IMPLANT2_ALAC = m.binary_var(name='alacrity-implant-2')
IMPLANT2_CRIT = m.binary_var(name='critical-implant-2')

STIM_ACCU = m.binary_var(name='accuracy-stim')

if IMPLANT1 == 'alacrity':
    if IMPLANT2 == 'alacrity':
        IMPLANT1_ALAC = 1
        IMPLANT1_CRIT = 0
        IMPLANT2_ALAC = 1
        IMPLANT2_CRIT = 0
    elif IMPLANT2 == 'critical':
        IMPLANT1_ALAC = 1
        IMPLANT1_CRIT = 0
        IMPLANT2_ALAC = 0
        IMPLANT2_CRIT = 1
elif IMPLANT1 == 'critical':
    if IMPLANT2 == 'alacrity':
        IMPLANT1_ALAC = 0
        IMPLANT1_CRIT = 1
        IMPLANT2_ALAC = 1
        IMPLANT2_CRIT = 0
    elif IMPLANT2 == 'critical':
        IMPLANT1_ALAC = 0
        IMPLANT1_CRIT = 1
        IMPLANT2_ALAC = 0
        IMPLANT2_CRIT = 1
else:
    sys.exit('ERROR: ILLEGAL IMPLANTS')
     

# set constraints
ACCURACY = m.add_constraint(m.sum([264*STIM_ACCU, 554*ENHANCEMENT_ACCU, 554*EARPIECE_ACCU,
            130*AUGMENT77_ACCU]) >= GOAL_ACCURACY, ctname='accuracy-constraint')

ALACRITY = m.add_constraint(m.sum([554*ENHANCEMENT_ALAC, 554*EARPIECE_ALAC, 130*AUGMENT77_ALAC,
            577*IMPLANT1_ALAC, 577*IMPLANT2_ALAC]) >= GOAL_ALACRITY, ctname='alacrity-constraint')

ENHANCEMENTS = m.add_constraint(m.sum([ENHANCEMENT_ACCU, ENHANCEMENT_ALAC]) <= 7, ctname='enhancement-constraint')

AUGMENTS = m.add_constraint(m.sum([ AUGMENT77_ALAC, AUGMENT77_ACCU, AUGMENT77_CRIT]) == 14, ctname='augment-constraint')

EARPIECE = m.add_constraint(m.sum([EARPIECE_ACCU, EARPIECE_ALAC, EARPIECE_CRIT]) == 1, ctname='earpiece-constraint')

m.set_multi_objective('min', [264*STIM_ACCU + 554*ENHANCEMENT_ACCU + 130*AUGMENT77_ACCU + 554*EARPIECE_ACCU,
            554*ENHANCEMENT_ALAC + 130*AUGMENT77_ALAC + 554*EARPIECE_ALAC + 577*IMPLANT1_ALAC + 577*IMPLANT2_ALAC])
# goals:
# goal accuracy
# m.minimize(264*STIM_ACCU + 554*ENHANCEMENT_ACCU + 108*AUGMENT74_ACCU + 130*AUGMENT77_ACCU + 554*EARPIECE_ACCU)
# # goal alacrity
# m.minimize(554*ENHANCEMENT_ALAC + 108*AUGMENT74_ALAC + 130*AUGMENT77_ALAC + 554*EARPIECE_ALAC)
# goal critical
# m.maximize(554*ENHANCEMENT_CRIT + 108*AUGMENT74_CRIT + 130*AUGMENT77_CRIT + 554*EARPIECE_CRIT)

# solve and display
m.solve().display()
# print(264*STIM_ACCU + 554*ENHANCEMENT_ACCU + 108*AUGMENT74_ACCU + 130*AUGMENT77_ACCU + 554*EARPIECE_ACCU)
# print(554*ENHANCEMENT_ALAC + 108*AUGMENT74_ALAC + 130*AUGMENT77_ALAC + 554*EARPIECE_ALAC)