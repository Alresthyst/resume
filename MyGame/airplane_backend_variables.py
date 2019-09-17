import airplane_frontend_variables
import General_variables as G_val


Running_mode = G_val.RUNNING_MODE
"""
development

gaming
"""

PATTERN_COUNTER = airplane_frontend_variables.SAVE_PATTERN_COUNTER
PATTERN_ITER_NUMBER = airplane_frontend_variables.PATTERN_ITER_NUMBER
GENE_COUNTER = G_val.GENE_COUNTER

RESULT_FILE_LOCATION_FRONT = r'''D:\Research\Gaming\making game\DATA\Generation '''
# RESULT_FILE_LOCATION_FRONT = r'''C:\Users\Ryrie\Dropbox\RESEARCH\making game\DATA\Generation '''


RESULT_FILE_LOCATION_BACK = r"""th\Airplane_Result"""

CODE_PATH_FRONT = r'''D:\Research\Gaming\making game\DATA\Generation '''
# CODE_PATH_FRONT = r'''C:\Users\Ryrie\Dropbox\RESEARCH\making game\DATA\Generation '''
CODE_PATH_BACK = r"""th\GA_Result"""
SUB_CODE_NAME = '\Child_'


RESULT_FILE_LOCATION = r'''D:\Documents\Graduate School\Research\Gaming\making game\Results'''
RESULT_PATTERN_NAME = '\pattern'
RESULT_FILE_NAME = '\Result_'


HEALTH_INDEX = 9

EVAL_ALPHA_MODIFIER_X = 0.5
EVAL_ALPHA_MODIFIER_Y = 5

PARENTS_NUMBER = 2
PARENTS_MODE = 'default'
"""
default : 실험용
"""

CHILDREN_MODE = 'default'
PLAYER_CHILDREN_MODE = 'GA Generator 1'
PLAYER_CHILDREN_MODE_DIVISION_NUMBER = 7

CHILDREN_NUMBER_ORIGIN = airplane_frontend_variables.PATTERN_ITER_NUMBER
CHILDREN_NUMBER = airplane_frontend_variables.PATTERN_ITER_NUMBER

