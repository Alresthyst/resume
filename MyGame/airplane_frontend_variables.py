from PIL import Image as Img
import pygame
from scipy.stats import norm
import os
import General_variables as G_val


Running_mode = G_val.RUNNING_MODE
"""
'gaming' : GA 와 연동
'development : GA 개발용
"""

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

GAME_WIDTH = 1280
GAME_HEIGHT = 720 + 150

GAME_FPS = 60

GAME_CAPTION = 'HAHAHA :)'

SIZE_ARRAY = []

SAVE_PATH_COUNTER = [0]
SAVE_PATTERN_COUNTER = [0]
SAVE_COUNTER = [0]
PATTERN_ITER_NUMBER = 7
TESTER_PATTERN_NUMBERS = 0
GENE_COUNTER = G_val.GENE_COUNTER

ACTION_COUNTER_TIME = 0.3
#
if Running_mode == 'development':
    SAVE_PATTERN_COUNTER = [TESTER_PATTERN_NUMBERS]


TEXT_LOCATION = r'''D:\Documents\Graduate School\Research\Gaming\making game\Results'''
TEXT_LOCATION_FRONT = r'''D:\Research\Gaming\making game\DATA\Generation '''
# TEXT_LOCATION_FRONT = r'''C:\Users\Ryrie\Dropbox\RESEARCH\making game\DATA\Generation '''
TEXT_LOCATION_BACK = r"""th\Airplane_Result"""

SAVE_FILE_NAME = '\Result_'

SAVE_PATH = ['\pattern' + str(i + 1) for i in range(50)]


SKILL_UI_INIT_HEIGHT_MODIFIER = 20
SKILL_UI_INIT_WIDTH_START_POINT = 50
SKILL_UI_GAP = 30

GAME_HEALTH = 100

AIRPLANE_IMAGE_PATH = 'image/airplane.jpg'
AIRPLANE_WIDTH, AIRPLANE_HEIGHT = Img.open(AIRPLANE_IMAGE_PATH).size
AIRPLANE_INIT_HEIGHT_MODIFIER = 200
AIRPLANE_MOVEMENT_MODIFIER = 10
AIRPLANE_INIT_POS = [450, 450]
SIZE_ARRAY.append(['Airplane', AIRPLANE_WIDTH, AIRPLANE_HEIGHT])

TEMP_ENEMY_PATH = 'image/temp_enemy.jpg'
TEMP_ENEMY_WIDTH, TEMP_ENEMY_HEIGHT = Img.open(TEMP_ENEMY_PATH).size
EVENT_TEMP_ENEMY = pygame.USEREVENT + 3
TEMP_ENEMY_INIT_POS = [500, 150]


AREA_LENGTH = 3600
MOVING_EVADE_INPUT = [AIRPLANE_MOVEMENT_MODIFIER, -AIRPLANE_MOVEMENT_MODIFIER]
BULLET_COUNT_TIME = 30
BULLET_COUNT_TIME_PLAYER_NORMAL = 10
BULLET_COUNT_TIME_PLAYER_MULTI = 20
BULLET_COUNT_TIME_ENEMY_NORMAL = 30
BULLET_COUNT_TIME_ENEMY_MULTI = 60

BULLET_SPEED = 15
BULLET_OUT_WINDOW_CONTROL_MODIFIER = 80

NORMAL_INDEX = 0
MULTISHOT_INDEX = 1
SPREAD_INDEX = 2
BOMB_INDEX = 3
CHARGE_INDEX = 5


NORMAL_ATTACK_IMAGE_PATH = 'image/bullet.jpg'
NORMAL_ATTACK_UI_PATH = 'image/bullet_ui.jpg'
NORMAL_ATTACK_WIDTH, NORMAL_ATTACK_HEIGHT = Img.open(NORMAL_ATTACK_IMAGE_PATH).size
NORMAL_UI_WIDTH, NORMAL_UI_HEIGHT = Img.open(NORMAL_ATTACK_UI_PATH).size
SIZE_ARRAY.append(['Normal', NORMAL_UI_WIDTH, NORMAL_UI_HEIGHT])
IDX_NORMAL = 0


MULTISHOT_IMAGE_PATH = 'image/bullet.jpg'
MULTISHOT_WIDTH, MULTISHOT_HEIGHT = Img.open(MULTISHOT_IMAGE_PATH).size
MULTISHOT_SKILL_UI_PATH = 'image/multi shot_skill_ui.jpg'
MULTISHOT_SKILL_UI_WIDTH, MULTISHOT_SKILL_UI_HEIGHT = Img.open(MULTISHOT_SKILL_UI_PATH).size
MULTISHOT_GAP_MODIFIER = 30
MULTISHOT_INIT_AMMO = 20
MULTISHOT_AMMO_TEXT_POS_GAP = [-10, 20]
MULTISHOT_AMMO_REFRESH_TIME = 2
EVENT_MULTISHOT = pygame.USEREVENT + 2
SIZE_ARRAY.append(['Multi', MULTISHOT_SKILL_UI_WIDTH, MULTISHOT_SKILL_UI_HEIGHT])
IDX_MULTISHOT = 1


CHARGE_BEAM_SHOT_IMAGE_PATH = 'image/charged shot_model.png'
CHARGE_BEAM_SHOT_WIDTH, CHARGE_BEAM_SHOT_HEIGHT = Img.open(CHARGE_BEAM_SHOT_IMAGE_PATH).size
CHARGE_BEAM_SHOT_SKILL_UI_PATH = 'image/charged shot_skill_ui.jpg'
CHARGE_BEAM_SHOT_UI_WIDTH, CHARGE_BEAM_SHOT_UI_HEIGHT = Img.open(CHARGE_BEAM_SHOT_SKILL_UI_PATH).size
SIZE_ARRAY.append(['Charged', CHARGE_BEAM_SHOT_UI_WIDTH, CHARGE_BEAM_SHOT_UI_HEIGHT])
CHARGE_BEAM_TIMER = 3
CHARGE_BEAM_COUNTER = 60
IDX_CHARGED = 2


SHIELD_IMAGE_PATH = 'image/shield.jpg'
SHIELD_WIDTH, SHIELD_HEIGHT = Img.open(SHIELD_IMAGE_PATH).size
SHIELD_SKILL_UI_PATH = 'image/shield_skill_ui.jpg'
SHIELD_SKILL_UI_WIDTH, SHIELD_SKILL_UI_HEIGHT = Img.open(SHIELD_SKILL_UI_PATH).size
SIZE_ARRAY.append(['Shield', SHIELD_SKILL_UI_WIDTH, SHIELD_SKILL_UI_HEIGHT])
IDX_SHIELD = 3


TELEPORT_IMAGE_PATH = 'image/teleport.jpg'
TELEPORT_WIDTH, TELEPORT_HEIGHT = Img.open(TELEPORT_IMAGE_PATH).size
SIZE_ARRAY.append(['Teleport', TELEPORT_WIDTH, TELEPORT_HEIGHT])
IDX_TELEPORT = 4
TELEPORT_LENGTH = 150
TELEPORT_TIME = 5.0
EVENT_TELEPORT = pygame.USEREVENT + 1


BOMB_SHOT_IMAGE_PATH = 'image/boom 1.png'
BOMB_SHOT_WIDTH, BOMB_SHOT_HEIGHT = Img.open(BOMB_SHOT_IMAGE_PATH).size
BOMB_SHOT_SKILL_UI_PATH = 'image/charged shot_skill_ui.jpg'
BOMB_SHOT_SKILL_UI_WIDTH, BOMB_SHOT_SKILL_UI_HEIGHT = Img.open(BOMB_SHOT_IMAGE_PATH).size
SIZE_ARRAY.append(['Bomb', BOMB_SHOT_WIDTH, BOMB_SHOT_HEIGHT])
IDX_BOMB = 5
BOMB_SHOT_TIMER = 6

TEMP_ENEMY_NORMAL_PATH = 'image/bullet_enemy.jpg'
TEMP_ENEMY_NORMAL_WIDTH, TEMP_ENEMY_NORMAL_HEIGHT = Img.open(TEMP_ENEMY_NORMAL_PATH).size
TEMP_ENEMY_MOVEMENT_MODIFIER = 10

ENEMY_MULTISHOT_PATH = 'image/bullet_enemy.jpg'
ENEMY_MULTISHOT_WIDTH, ENEMY_MULTISHOT_HEIGHT = Img.open(ENEMY_MULTISHOT_PATH).size


# https://workwallpaper.com/full-hd-1920x1080-wallpapers/
BACKGROUND_IMAGE_PATH = 'image/green-background-2_00450547_1280-720.jpg'
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = Img.open(BACKGROUND_IMAGE_PATH).size
SIZE_ARRAY.append(['Background', BACKGROUND_WIDTH, BACKGROUND_HEIGHT])

HEALTH_SIZE = [200, 25]
HEALTH_POS = [BACKGROUND_WIDTH - HEALTH_SIZE[0] - 15, BACKGROUND_HEIGHT + 30]
HEALTH_TEXT_GAP = [75, -3]

HEALTH_RECOVERY = 5
HEALTH_DAMAGE = 10


# Key mapping:
"""
up, down, left, right = airplane movement

a, d = airplane teleport direction

space = airplane normal attack

Left shift = airplane multi attack

f = airplane charged attack

1 = airplane shield 

r = regenerate temp enemy
"""
AIRPLANE_CONTROL_KEYS = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
                         pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.K_LSHIFT,
                         pygame.K_f, pygame.K_1,
                         pygame.K_r,
                         pygame.K_p, pygame.K_o]
KEY_UP = 0
KEY_DOWN = 1
KEY_LEFT = 2
KEY_RIGHT = 3
KEY_A = 4
KEY_D = 5
KEY_SPACE = 6
KEY_LSHIFT = 7
KEY_F = 8
KEY_1 = 9
KEY_R = 10
KEY_NUM0 = 11
KEY_NUM1 = 12

# TARGET CODE MAPPING :
"""
1 : shield
2 : temp enemy

"""
CODE_DUMMY = 0
CODE_SHIELD = 1
CODE_TEMP_ENEMY = 2
CODE_TEMP_ENEMY_BOMB = 21
CODE_TEMP_ENEMY_CHARGE = 22
CODE_HIT_ME = 3
CODE_HIT_ME_BOMB = 31
CODE_HIT_ME_CHARGE = 32


ENEMY_BEHAVIOR_TIME_INTERVAL = 70  # (ms)
ENEMY_EVENT_ID = pygame.USEREVENT + 5
"""
1 : UP
2 : DOWN
3 : LEFT
4 : RIGHT
5 : NORMAL 
6 : MULTISHOT
7 : TELEPORT( < )
8 : TELEPORT( > )
"""
ENEMY_EVENT_MODES = [pygame.event.Event(ENEMY_EVENT_ID, {'mode': 1, 'Key': pygame.K_UP}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 2, 'Key': pygame.K_DOWN}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 3, 'Key': pygame.K_LEFT}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 4, 'Key': pygame.K_RIGHT}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 5, 'Key': pygame.K_SPACE}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 6, 'Key': pygame.K_LSHIFT}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 7, 'Key': pygame.K_a}),
                     pygame.event.Event(ENEMY_EVENT_ID, {'mode': 8, 'Key': pygame.K_d})]

# for times in range(30):
#     ran_int = ran.randrange(1, 4)
#     for time in range(10):
#         ENEMY_BEHAVIOR.append(ran_int)
iter_num = 5
temp_5 = [5 for i in range(iter_num)]
temp_6 = [6 for i in range(iter_num)]
temp_7 = [7 for i in range(iter_num)]
temp_8 = [8 for i in range(iter_num)]
temp = temp_5 + temp_6 + temp_7 + temp_8


def moving_function(distance_x, distance_y, area_length):
    var = area_length/2
    STD_Z_x = distance_x / var
    STD_Z_y = distance_y / var
    print(distance_y)
    return [norm.cdf(STD_Z_x), norm.cdf(STD_Z_y)]


def saving_text(input_text, airplane_type, location):
    file_name = SAVE_FILE_NAME + airplane_type + ".txt"
    log = open(location + file_name, 'a')
    log.write(input_text)
    log.close()


def vector_minus(input_a, input_b):
    if len(input_a) != len(input_b):
        print("input matrix size is different")

    else:
        temp = []
        for idx in range(len(input_a)):
            temp.append(input_a[idx] - input_b[idx])

    return temp


def create_path(path):
    """
    https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
    https://stackoverflow.com/questions/23793987/python-write-file-to-directory-doesnt-exist
    """
    if not os.path.exists(path):
        os.makedirs(path)
