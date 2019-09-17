import airplane_frontend_variables as a_val


number_pattern = a_val.TESTER_PATTERN_NUMBERS
number_iter = a_val.PATTERN_ITER_NUMBER
# ------------------------- clock moving------------------------------------------------------------
iter_num = 5

temp = ['up', 'up&right', 'right', 'down&right', 'down', 'down', 'down&left', 'left', 'up&left', 'up']
temp_2 = []
for item in temp:
    for num in range(iter_num):
        temp_2.append(item)
clock_moving = dict()
clock_moving['moving'] = temp_2 + ['multi'] + temp_2 + ['normal'] + temp_2
clock_moving['description'] = 'just clock moving'
# --------------------------------------------------------------------------------------------------


# ------------------------- Zig moving -------------------------------------------------------------
temp3 = ['up&right', 'up&right', 'up&right', 'right', 'right', 'right']
temp_zig = list()
for i in range(10):
    temp_zig += temp3

    if i % 3 == 0:
        temp_zig += ['multi']

temp4 = ['down&left', 'down&left', 'down&left', 'left', 'left', 'left']
temp_zig_opposite = []

for i in range(10):
    temp_zig_opposite += temp4

    if i % 3 == 0:
        temp_zig_opposite += ['multi']

zig_moving = dict()
zig_moving['moving'] = temp_zig + temp_zig_opposite
zig_moving['description'] = 'just zig moving'

# --------------------------------------------------------------------------------------------------

TESTER_PATTERN = [clock_moving, zig_moving, clock_moving]
LEARNER_INIT_PATTERN = list()
for i in range(5):
    LEARNER_INIT_PATTERN.append(zig_moving)
for i in range(5):
    LEARNER_INIT_PATTERN.append(clock_moving)

pattern_tester = dict()
pattern_learner = dict()

pattern_learner['GA learner'] = dict()
pattern_learner['GA tester'] = dict()
pattern_tester['GA learner'] = dict()
pattern_tester['GA tester'] = dict()

for pat_num in range(number_pattern):
    pat = 'pattern' + str(pat_num + 1)
    pattern_tester['GA tester'][pat] = TESTER_PATTERN[pat_num]
    pattern_learner['GA learner'][pat] = dict()
    for it_num in range(number_iter):
        se = 'sequence' + str(it_num + 1)
        pattern_learner['GA learner'][pat][se] = LEARNER_INIT_PATTERN[it_num]
