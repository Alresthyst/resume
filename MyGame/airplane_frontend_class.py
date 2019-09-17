import copy

import numpy
import pygame

import General_variables as G_val
import Generate_GA as ga
import airplane_frontend_variables as a_val
import airplane_front_making_behaviors as ab
import airplane_moving_val as m_val
import time
from copy import deepcopy


class AirplaneGame:

    def __init__(self):

        pygame.init()

        # self.font = pygame.font.SysFont("arial", 25)

        self.game = pygame.display.set_mode((a_val.GAME_WIDTH, a_val.GAME_HEIGHT))
        
        self.airplane_action_counter = dict()
        self.airplane_action_counter['player'] = time.time()
        self.airplane_action_counter['mod_player'] = list()
        self.airplane_action_counter['enemy'] = time.time()
        self.airplane_action_counter['mod_enemy'] = list()
        self.airplane_action_counter['started'] = 0
        self.airplane_action_counter['behavior_done_player'] = False
        self.airplane_action_counter['behavior_done_enemy'] = False

        self.airplane = pygame.image.load(a_val.AIRPLANE_IMAGE_PATH)
        self.background_1 = pygame.image.load(a_val.BACKGROUND_IMAGE_PATH)
        self.background_1_x = 0
        self.background_2 = self.background_1.copy()
        self.background_2_x = 0

        self.airplane_flag_up = 0
        self.airplane_flag_down = 0
        self.airplane_flag_left = 0
        self.airplane_flag_right = 0

        self.airplane_temp_keys_storage = []

        self.normal_attack = pygame.image.load(a_val.NORMAL_ATTACK_IMAGE_PATH)
        self.normal_skill_ui = pygame.image.load(a_val.NORMAL_ATTACK_UI_PATH)
        self.normal_pos = []
        self.normal_flag = []

        self.multishot = pygame.image.load(a_val.MULTISHOT_IMAGE_PATH)
        self.multishot_skill_ui = pygame.image.load(a_val.MULTISHOT_SKILL_UI_PATH)
        self.multi_pos = []
        self.multi_pos_left = []
        self.multi_pos_right = []
        self.multi_flag = []
        self.multishot_ammo = a_val.MULTISHOT_INIT_AMMO
        self.multishot_ammo_refresh = int(1000 * a_val.MULTISHOT_AMMO_REFRESH_TIME)
        self.multishot_event = a_val.EVENT_MULTISHOT
        self.multishot_ammo_pos = [a_val.SKILL_UI_GAP + a_val.NORMAL_UI_WIDTH + a_val.MULTISHOT_AMMO_TEXT_POS_GAP[0]
                                   + a_val.MULTISHOT_SKILL_UI_WIDTH,
                                   a_val.SKILL_UI_INIT_HEIGHT_MODIFIER + a_val.BACKGROUND_HEIGHT +
                                   a_val.MULTISHOT_AMMO_TEXT_POS_GAP[1] + a_val.MULTISHOT_SKILL_UI_HEIGHT]

        self.spread_shot = pygame.image.load(a_val.MULTISHOT_IMAGE_PATH)
        self.spread_shot_skill_ui = pygame.image.load(a_val.MULTISHOT_SKILL_UI_PATH)
        self.spread_pos = []
        self.spread_pos_left_1 = []
        self.spread_pos_left_2 = []
        self.spread_pos_right_1 = []
        self.spread_pos_right_2 = []

        self.charged_shot = pygame.image.load(a_val.CHARGE_BEAM_SHOT_IMAGE_PATH)
        self.charged_shot_ui = pygame.image.load(a_val.CHARGE_BEAM_SHOT_SKILL_UI_PATH)
        # in progressing.... not updated
        self.charged_shot_ui = self.grayscale(self.charged_shot_ui)
        self.charge_pos = []
        self.charge_timer = list()
        self.charge_counter = 0

        self.shield = pygame.image.load(a_val.SHIELD_IMAGE_PATH)
        self.shield_ui = pygame.image.load(a_val.SHIELD_SKILL_UI_PATH)
        # in progressing.... not updated
        self.shield_ui = self.grayscale(self.shield_ui)
        self.shield_flag = []
        self.shield_pos = []

        self.teleport = pygame.image.load(a_val.TELEPORT_IMAGE_PATH)
        self.teleport_event = pygame.event.Event(a_val.EVENT_TELEPORT, dict=None)
        self.teleport_event_id = a_val.EVENT_TELEPORT
        self.teleport_time = int(1000 * a_val.TELEPORT_TIME)
        self.flag_teleport = 0

        self.bomb_shot = pygame.image.load(a_val.BOMB_SHOT_IMAGE_PATH)
        # self.bomb_shot = pygame.transform.scale(self.bomb_shot, (350, 50))
        self.bomb_shot_ui = pygame.image.load(a_val.BOMB_SHOT_SKILL_UI_PATH)
        self.bomb_shot_pos = list()
        self.bomb_shot_timer = a_val.BOMB_SHOT_TIMER
        self.bomb_shot_timer_counter = list()
        self.enemy_bomb_shot_timer_counter = list()

        self.player_bullets = [self.normal_pos, self.multi_pos, self.multi_pos_left, self.multi_pos_right,
                               self.bomb_shot_pos, self.spread_pos]

        self.health_size = copy.deepcopy(a_val.HEALTH_SIZE)
        self.health_color = a_val.GREEN

        self.skill_ui_array = [self.normal_skill_ui, self.multishot_skill_ui, self.charged_shot_ui,
                               self.shield_ui, self.teleport, self.bomb_shot_ui, self.spread_shot_skill_ui]

        self.clock = pygame.time.Clock()
        self.game_status = True

        self.x_change = 0
        self.y_change = 0

        self.enemy_x_change = 0
        self.enemy_y_change = 0

        self.player_pos = a_val.AIRPLANE_INIT_POS[:]

        self.enemy = pygame.image.load(a_val.TEMP_ENEMY_PATH)
        self.enemy_pos = a_val.TEMP_ENEMY_INIT_POS[:]

        self.enemy_normal = pygame.image.load(a_val.TEMP_ENEMY_NORMAL_PATH)
        self.enemy_multi = pygame.image.load(a_val.ENEMY_MULTISHOT_PATH)

        self.enemy_normal_pos = []
        self.enemy_multi_pos = []
        self.enemy_multi_pos_left = []
        self.enemy_multi_pos_right = []
        self.enemy_bomb_shot_pos = list()

        self.enemy_spread_shot = pygame.image.load(a_val.MULTISHOT_IMAGE_PATH)
        self.enemy_spread_shot_skill_ui = pygame.image.load(a_val.MULTISHOT_SKILL_UI_PATH)
        self.enemy_spread_pos = []
        self.enemy_spread_pos_left_1 = []
        self.enemy_spread_pos_left_2 = []
        self.enemy_spread_pos_right_1 = []
        self.enemy_spread_pos_right_2 = []

        self.enemy_charge_pos = list()
        self.enemy_charge = pygame.image.load(a_val.CHARGE_BEAM_SHOT_IMAGE_PATH)
        self.enemy_charge_timer = list()
        self.enemy_charge_counter = 0

        self.enemy_bullets = [self.enemy_normal_pos, self.enemy_multi_pos,
                              self.enemy_multi_pos_left, self.enemy_multi_pos_right, self.enemy_bomb_shot_pos,
                              self.enemy_spread_pos, self.enemy_charge_pos]

        self.event_temp_enemy = pygame.event.Event(a_val.EVENT_TEMP_ENEMY, {'mode': 1})
        self.event_temp_enemy_id = a_val.EVENT_TEMP_ENEMY

        self.event_enemy = a_val.ENEMY_EVENT_MODES
        self.event_enemy_flag = 0
        # self.enemy_behaviors_container = a_val.ENEMY_BEHAVIOR

        self.enemy_behaviors_clock = pygame.time.Clock()
        self.enemy_behaviors_time = 0
        self.enemy_behaviors_time_flag = 0
        self.enemy_behavior_mode = 0

        self.moving_dir_airplane = 0
        self.moving_dir_enemy = 0

        self.player_normal_count = 0
        self.player_multi_count = 0
        self.enemy_normal_count = 0
        self.enemy_multi_count = 0

        self.outer_flag = True
        self.sequence_counter = 0

        self.state_player_before = []
        self.state_player_after = []
        self.state_player_bullets = []
        self.state_player_bullets_number = []

        self.state_enemy_before = []
        self.state_enemy_after = []
        self.state_enemy_bullets = []
        self.state_enemy_bullets_number = []

        self.saved_data_player = []
        self.saved_data_enemy = []
        self.saved_data_all = []

        self.player_hits = 0
        self.enemy_hits = 0

        self.game_defeated_plane = ''

        self.behavior_counter = 0
        self.pattern_counter = 0

        self.save_path_counter = 0

        self.behaviors_player = dict()
        self.behaviors_enemy = dict()
        self.creating_behaviors()

        self.init_games()

    def enemy_events_control(self, mode):
        """
        :param mode: beginning 1 ~
        :return: None
        """
        pygame.event.post(self.event_enemy[mode - 1])

    def init_games(self):

        pygame.display.set_caption(a_val.GAME_CAPTION)
        self.game.fill(a_val.WHITE)

        self.run_games()

    def run_games(self):

        while self.outer_flag:
            while self.game_status:
                for event in pygame.event.get():
                    self.pygame_event_handler(event)

                self.unit_position_set()
                self.bullet_scan_all()

                self.set_skill_ui()
                self.units_drawing()
                # print("Player HP : ", a_val.GAME_HEALTH - self.player_hits,
                #       "Enemy HP : ", a_val.GAME_HEALTH - self.enemy_hits)
                pygame.display.update()
                self.clock.tick(a_val.GAME_FPS)
                self.temp_algorithm_testing()
            pygame.quit()
            quit()
            break

    def set_skill_ui(self):
        self.game.fill(a_val.WHITE)
        init_height = a_val.BACKGROUND_HEIGHT + a_val.SKILL_UI_INIT_HEIGHT_MODIFIER
        init_width = a_val.SKILL_UI_INIT_WIDTH_START_POINT

        width = init_width
        temp_size_array = a_val.SIZE_ARRAY[1:-1]

        for idx, item in enumerate(temp_size_array):
            self.draw_object(self.skill_ui_array[idx], [width, init_height])
            width += item[1] + a_val.SKILL_UI_GAP
        # 이 부분 수정해서 깔끔하게 정리 해야 됨
        # font = self.font
        # text = font.render(str(self.multishot_ammo), False, (0, 0, 0))
        # self.game.blit(text, self.multishot_ammo_pos)
        return 0

    def pygame_event_handler(self, event):

        if event.type == pygame.QUIT:
            self.game_status = False

        elif event.type == pygame.KEYDOWN:
            self.pygame_key_down_handler()

        elif event.type == pygame.KEYUP:
            self.pygame_key_up_handler(event)

        elif event.type == self.teleport_event_id:
            self.teleport_event_handler()

        elif event.type == self.multishot_event:
            self.multishot_event_handler()

        elif event.type == self.event_temp_enemy_id:
            pygame.time.set_timer(self.event_temp_enemy_id, 0)

    def pygame_key_down_handler(self):

        temp_key = pygame.key.get_pressed()
        # print('key down temp:', temp_key[273:277])
        # print('key down self', self.airplane_temp_keys_storage)
        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_LEFT]]:
            self.x_change = -a_val.AIRPLANE_MOVEMENT_MODIFIER
        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_RIGHT]]:
            self.x_change = a_val.AIRPLANE_MOVEMENT_MODIFIER

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_UP]]:
            self.y_change = -a_val.AIRPLANE_MOVEMENT_MODIFIER
        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_DOWN]]:
            self.y_change = a_val.AIRPLANE_MOVEMENT_MODIFIER

        if self.airplane_temp_keys_storage[2:4] == (0, 1) and temp_key[275:277] == (1, 1):
            self.x_change = a_val.AIRPLANE_MOVEMENT_MODIFIER
        if self.airplane_temp_keys_storage[2:4] == (1, 0) and temp_key[275:277] == (1, 1):
            self.x_change = -a_val.AIRPLANE_MOVEMENT_MODIFIER

        if self.airplane_temp_keys_storage[0:2] == (0, 1) and temp_key[273:275] == (1, 1):
            self.y_change = -a_val.AIRPLANE_MOVEMENT_MODIFIER
        if self.airplane_temp_keys_storage[0:2] == (1, 0) and temp_key[273:275] == (1, 1):
            self.y_change = a_val.AIRPLANE_MOVEMENT_MODIFIER
        self.airplane_temp_keys_storage = temp_key[273:277]

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_A]] and self.flag_teleport == 0:
            self.player_pos[0] -= a_val.TELEPORT_LENGTH
            self.flag_teleport = 1
            self.skill_ui_array[a_val.IDX_TELEPORT] = self.grayscale(self.teleport)
            pygame.time.set_timer(self.teleport_event_id, self.teleport_time)

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_D]] and self.flag_teleport == 0:
            self.player_pos[0] += a_val.TELEPORT_LENGTH
            self.flag_teleport = 1
            self.skill_ui_array[a_val.IDX_TELEPORT] = self.grayscale(self.teleport)
            pygame.time.set_timer(self.teleport_event_id, self.teleport_time)

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_SPACE]]:
            self.generate_bullet('player', 'normal')

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_LSHIFT]]:  # and self.multishot_ammo > 0:
            self.generate_bullet('player', 'multi')
            # pygame.time.set_timer(self.multishot_event, self.multishot_ammo_refresh)

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_R]]:
            if not self.enemy_pos:
                self.enemy_pos = [100, 100]

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_NUM0]]:
            self.event_enemy_flag = 0
            self.enemy_behavior_mode = 0

        if temp_key[a_val.AIRPLANE_CONTROL_KEYS[a_val.KEY_NUM1]]:
            self.event_enemy_flag = 1

    def pygame_key_up_handler(self, event):

        temp_key = pygame.key.get_pressed()
        if event.key in a_val.AIRPLANE_CONTROL_KEYS[0:4]:
            self.x_change = 0
            self.y_change = 0

        # if temp_key[275:277] == (0, 1) and self.airplane_temp_keys_storage[2:4] == (1, 1):
        #     self.x_change = -val.AIRPLANE_MOVEMENT_MODIFIER
        #
        # if temp_key[275:277] == (1, 0) and self.airplane_temp_keys_storage[2:4] == (1, 1):
        #     self.x_change = val.AIRPLANE_MOVEMENT_MODIFIER
        #
        # if temp_key[273:275] == (0, 1) and self.airplane_temp_keys_storage[0:2] == (1, 1):
        #     self.y_change = val.AIRPLANE_MOVEMENT_MODIFIER
        #
        # if temp_key[273:275] == (1, 0) and self.airplane_temp_keys_storage[0:2] == (1, 1):
        #     self.y_change = -val.AIRPLANE_MOVEMENT_MODIFIER

    def airplane_moving(self, mode, area_length):
        target_pos = []
        anti_target_pos = []

        if mode == 0:
            target_pos = self.player_pos[:]
            anti_target_pos = self.enemy_pos[:]
        elif mode == 1:
            target_pos = self.enemy_pos[:]
            anti_target_pos = self.player_pos[:]
        else:
            print("you have to type mode.")
            print("Mode 0 : target is player")
            print("Mode 1 : target is A.I")

        distance_x = target_pos[0] - anti_target_pos[0]
        distance_y = target_pos[1] - anti_target_pos[1]

        temp = a_val.moving_function(distance_x, distance_y, area_length)

        x = ['left', 'right']
        y = ['up', 'down']

        x_probability = temp[0]
        x_opposite_probability = 1 - temp[0]

        y_probability = temp[1]
        y_opposite_probability = 1 - temp[1]

        x_result = numpy.random.choice(x, p=[x_probability, x_opposite_probability])
        y_result = numpy.random.choice(y, p=[y_probability, y_opposite_probability])

        if x_result == 'left' and mode == 0:
            self.x_change = -5
        elif x_result == 'right' and mode == 0:
            self.x_change = 5

        if x_result == 'left' and mode == 1:
            self.enemy_x_change = -5
        elif x_result == 'right' and mode == 1:
            self.enemy_x_change = 5

        if y_result == 'up' and mode == 0:
            self.y_change = -5
        elif y_result == 'down' and mode == 0:
            self.y_change = 5

        if y_result == 'up' and mode == 1:
            self.enemy_y_change = -5
        elif y_result == 'down' and mode == 1:
            self.enemy_y_change = 5

    def bullet_counting(self):
        self.player_normal_count += 1
        self.player_multi_count += 1
        self.enemy_normal_count += 1
        self.enemy_multi_count += 1

    def creating_behaviors(self):

        self.behaviors_player['GA learner'] = dict()
        self.behaviors_player['GA tester'] = dict()
        self.behaviors_enemy['GA learner'] = dict()
        self.behaviors_enemy['GA tester'] = dict()

        if G_val.BEHAVIOR_CREATION_MODE == 'Normal':
            ab_controller = ab.CreatingBehaviors()
            self.behaviors_player = ab_controller.behaviors_player
            self.behaviors_enemy = ab_controller.behaviors_enemy
        if G_val.BEHAVIOR_CREATION_MODE == 'Init':
            self.behaviors_player = m_val.pattern_learner
            self.behaviors_enemy = m_val.pattern_tester
# # -------------------------------------Set learner--------------------------------------------------------------------
#         if player_mode == 'GA learner':
#             for pattern_num in range(a_val.TESTER_PATTERN_NUMBERS):
#                 self.behaviors_player[player_mode]['pattern' + str(pattern_num + 1)] = dict()
#                 for num_iter in range(a_val.PATTERN_ITER_NUMBER):
#                     self.behaviors_player[player_mode]['pattern' + str(pattern_num + 1)]['sequence' + str(
#                         num_iter + 1)] = m_val.LEARNER_INIT_PATTERN[num_iter]
#
#         if enemy_mode == 'GA learner':
#             for pattern_num in range(a_val.TESTER_PATTERN_NUMBERS):
#                 self.behaviors_enemy[enemy_mode]['pattern' + str(pattern_num + 1)] = dict()
#                 for num_iter in range(a_val.PATTERN_ITER_NUMBER):
#                     self.behaviors_enemy[enemy_mode]['pattern' + str(pattern_num + 1)]['sequence' + str(
#                         num_iter + 1)] = m_val.LEARNER_INIT_PATTERN[num_iter]
# # --------------------------------------------------------------------------------------------------------------------
#
#
# # -------------------------------------Set tester---------------------------------------------------------------------
#         if player_mode == 'GA tester':
#             for pattern_num in range(a_val.TESTER_PATTERN_NUMBERS):
#                 self.behaviors_player[player_mode]['pattern' + str(pattern_num + 1)] = m_val.TESTER_PATTERN[pattern_num]
#
#         if enemy_mode == 'GA tester':
#             for pattern_num in range(a_val.TESTER_PATTERN_NUMBERS):
#                 self.behaviors_enemy[enemy_mode]['pattern' + str(pattern_num + 1)] = m_val.TESTER_PATTERN[pattern_num]
# # --------------------------------------------------------------------------------------------------------------------
# #         for pat in self.behaviors_enemy['GA tester']:
# #             print(pat

    def airplane_behavior(self, pos, mode, type):
        # print("airplane behavior", mode, type)
        if mode == '' or None:
            pass

        if mode == 'stop':
            pass

        if mode == 'up':
            pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'down':
            pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'left':
            pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'right':
            pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'up&right':
            pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER
            pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'down&right':
            pos[0] += a_val.AIRPLANE_MOVEMENT_MODIFIER
            pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'up&left':

            pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER
            pos[1] -= a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'down&left':
            pos[0] -= a_val.AIRPLANE_MOVEMENT_MODIFIER
            pos[1] += a_val.AIRPLANE_MOVEMENT_MODIFIER

        elif mode == 'normal':
            self.generate_bullet(type, 'normal')

        elif mode == 'multi':
            self.generate_bullet(type, 'multi')

        elif mode == 'bomb':
            self.generate_bullet(type, 'bomb')

        elif mode == 'spread':
            self.generate_bullet(type, mode)

        elif mode == 'charge':
            self.generate_bullet(type, "charge")

    def player_behavior(self, mode):

        modes = mode.split(G_val.SPILT_CHAR)

        if self.airplane_action_counter['started'] == 0:
            self.airplane_action_counter['started'] = 1
            self.airplane_action_counter['mod_player'] = modes
            for mod in modes:
                self.airplane_behavior(self.player_pos, mod, 'player')

        elif time.time() - self.airplane_action_counter['player'] < a_val.ACTION_COUNTER_TIME:
            for mod in self.airplane_action_counter['mod_player']:
                self.airplane_behavior(self.player_pos, mod, 'player')

        elif time.time() - self.airplane_action_counter['player'] >= a_val.ACTION_COUNTER_TIME:
            self.airplane_action_counter['player'] = time.time()
            self.airplane_action_counter['mod_player'] = modes
            for mod in modes:
                self.airplane_behavior(self.player_pos, mod, 'player')

    def enemy_behaviors(self, mode):

        modes = mode.split(G_val.SPILT_CHAR)

        if self.airplane_action_counter['started'] == 0:
            self.airplane_action_counter['started'] = 1
            self.airplane_action_counter['mod_enemy'] = modes
            for mod in modes:
                self.airplane_behavior(self.enemy_pos, mod, 'enemy')

        elif time.time() - self.airplane_action_counter['enemy'] < a_val.ACTION_COUNTER_TIME:
            for mod in self.airplane_action_counter['mod_enemy']:
                self.airplane_behavior(self.enemy_pos, mod, 'enemy')

        elif time.time() - self.airplane_action_counter['enemy'] >= a_val.ACTION_COUNTER_TIME:
            self.airplane_action_counter['enemy'] = time.time()
            self.airplane_action_counter['mod_enemy'] = modes
            for mod in modes:
                self.airplane_behavior(self.enemy_pos, mod, 'enemy')

    def all_airplane_controller(self):

        mode_p = G_val.PLAYER_GAME_MODE
        mode_e = G_val.ENEMY_GAME_MODE
        counter_pattern = a_val.SAVE_PATTERN_COUNTER[0]
        counter_seq = a_val.SAVE_COUNTER[0]

        pattern = 'pattern' + str(counter_pattern + 1)
        seq = 'sequence' + str(counter_seq + 1)
        # print("all_airplane_controller", self.behaviors_player[mode_p][pattern][seq]['moving'][-1])
        if self.behavior_counter < len(self.behaviors_player[mode_p][pattern][seq]['moving']) and \
                mode_p == 'GA learner':
            self.player_behavior(self.behaviors_player[mode_p][pattern][seq]['moving'][self.behavior_counter])

        if self.behavior_counter < len(self.behaviors_enemy[mode_e][pattern]['moving']) and \
                mode_e == 'GA tester':
            self.enemy_behaviors(self.behaviors_enemy[mode_e][pattern]['moving'][self.behavior_counter])

        self.behavior_counter += 1

        if self.behavior_counter > len(self.behaviors_player[mode_p][pattern][seq]['moving']):
            if self.enemy_bullets == [[] for i in range(len(self.enemy_bullets))] and \
                    self.player_bullets == [[] for i in range(len(self.player_bullets))]:
                self.game_defeated_plane = "None"
                self.finishing_sequence()

    def airplane_moving_trigger(self):

        self.airplane_moving_closing(self.player_pos[:], self.enemy_pos, a_val.AREA_LENGTH)
        self.airplane_moving_closing(self.enemy_pos, self.player_pos, a_val.AREA_LENGTH)

        # self.airplane_moving_evade(self.player_pos[:], a_val.AIRPLANE_WIDTH, self.enemy_normal_pos,
        #                            a_val.NORMAL_ATTACK_WIDTH, 'player')
        # self.airplane_moving_evade(self.player_pos[:], a_val.AIRPLANE_WIDTH, self.enemy_multi_pos,
        #                            a_val.MULTISHOT_WIDTH, 'player')
        # self.airplane_moving_evade(self.player_pos[:], a_val.AIRPLANE_WIDTH, self.enemy_multi_pos_left,
        #                            a_val.MULTISHOT_WIDTH, 'player')
        # self.airplane_moving_evade(self.player_pos[:], a_val.AIRPLANE_WIDTH, self.enemy_multi_pos_right,
        #                            a_val.MULTISHOT_WIDTH, 'player')
        #
        # self.airplane_moving_evade(self.enemy_pos, a_val.AIRPLANE_WIDTH, self.normal_pos,
        #                            a_val.NORMAL_ATTACK_WIDTH, 'enemy')
        # self.airplane_moving_evade(self.enemy_pos, a_val.AIRPLANE_WIDTH, self.multi_pos,
        #                            a_val.MULTISHOT_WIDTH, 'enemy')
        # self.airplane_moving_evade(self.enemy_pos, a_val.AIRPLANE_WIDTH, self.multi_pos_left,
        #                            a_val.MULTISHOT_WIDTH, 'enemy')
        # self.airplane_moving_evade(self.enemy_pos, a_val.AIRPLANE_WIDTH, self.multi_pos_right,
        #                            a_val.MULTISHOT_WIDTH, 'enemy')

        self.all_airplane_controller()
        # self.airplane_moving_attack()

    @staticmethod
    def airplane_moving_closing(player_pos, target_pos, area_length):
        dis_x = player_pos[0] - target_pos[0]
        dis_y = player_pos[1] - target_pos[1]

        if dis_x > area_length/2:
            player_pos[0] -= 5
        elif dis_x < -area_length/2:
            player_pos[0] += 5

        if dis_y > area_length/2:
            player_pos[1] -= 5
        elif dis_y < -area_length/2:
            player_pos[1] += 5

    @staticmethod
    def airplane_moving_evade(player_pos, player_width, bullet_pos, bullet_width, player_type):
        temp_moving_dir = 0
        for bpos in bullet_pos:
            temp_x = [bpos[0], bpos[0] + bullet_width, player_pos[0], player_pos[0] + player_width]
            if max(temp_x) - min(temp_x) <= bullet_width + player_width and bpos[1] < player_pos[1] and \
                    player_type == 'player':
                temp_moving_input = a_val.MOVING_EVADE_INPUT
                temp_moving_dir = numpy.random.choice(temp_moving_input, p=[0.5, 0.5])
                player_pos[0] += temp_moving_dir
            elif max(temp_x) - min(temp_x) <= bullet_width + player_width and bpos[1] > player_pos[1] and \
                    player_type == 'enemy':
                temp_moving_input = a_val.MOVING_EVADE_INPUT
                temp_moving_dir = numpy.random.choice(temp_moving_input, p=[0.5, 0.5])
                player_pos[0] += temp_moving_dir

        return temp_moving_dir

    def generate_bullet(self, player_type, bullet_type):
        if player_type == "player":
            if bullet_type == 'normal':
                self.normal_pos.append(
                    [self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.NORMAL_ATTACK_WIDTH / 2,
                     self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2])
                self.normal_flag = []

            if bullet_type == 'multi':
                self.multi_pos.append([self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.MULTISHOT_WIDTH / 2,
                                       self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2])
                self.multi_pos_left.append([self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.MULTISHOT_WIDTH / 2
                                            - a_val.MULTISHOT_WIDTH - a_val.MULTISHOT_GAP_MODIFIER,
                                            self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2])
                self.multi_pos_right.append([self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.MULTISHOT_WIDTH / 2
                                             + a_val.MULTISHOT_WIDTH + a_val.MULTISHOT_GAP_MODIFIER,
                                             self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2])
                self.multi_flag = []

            if bullet_type == 'bomb':
                self.bomb_shot_pos.append([(self.player_pos[0] + (a_val.AIRPLANE_WIDTH / 2)) - a_val.BOMB_SHOT_WIDTH / 2
                                          , (self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2) -
                                           (a_val.BOMB_SHOT_HEIGHT / 2)])
                self.bomb_shot_timer_counter.append(0)

            if bullet_type == 'spread':
                pos = [self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.MULTISHOT_WIDTH / 2,
                       self.player_pos[1] - a_val.AIRPLANE_HEIGHT / 2]
                self.spread_pos.append(pos)
                self.spread_pos_left_1.append([pos[0] - a_val.MULTISHOT_WIDTH - a_val.MULTISHOT_GAP_MODIFIER, pos[1]])
                self.spread_pos_left_2.append([pos[0] - 2*a_val.MULTISHOT_WIDTH - 2*a_val.MULTISHOT_GAP_MODIFIER,
                                               pos[1]])
                self.spread_pos_right_1.append([pos[0] + a_val.MULTISHOT_WIDTH + a_val.MULTISHOT_GAP_MODIFIER, pos[1]])
                self.spread_pos_right_2.append([pos[0] + 2 * a_val.MULTISHOT_WIDTH + 2 * a_val.MULTISHOT_GAP_MODIFIER,
                                               pos[1]])
            if bullet_type == 'charge':
                if self.charge_counter < a_val.CHARGE_BEAM_COUNTER:
                    self.charge_counter += 1
                else:
                    pos = [self.player_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.CHARGE_BEAM_SHOT_WIDTH / 2,
                           self.player_pos[1]]
                    self.charge_counter = 0
                    self.charge_pos.append(pos)
                    self.charge_timer.append(0)

        #     temp enemy's temporary bullets
        if player_type == 'enemy':
            if bullet_type == 'normal':
                self.enemy_normal_pos.append(
                    [self.enemy_pos[0] + a_val.TEMP_ENEMY_WIDTH / 2 - a_val.TEMP_ENEMY_NORMAL_WIDTH / 2,
                     self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT / 2])

            if bullet_type == 'multi':
                self.enemy_multi_pos.append([self.enemy_pos[0] + a_val.TEMP_ENEMY_WIDTH / 2 -
                                             a_val.MULTISHOT_WIDTH / 2,
                                             self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT / 2])
                self.enemy_multi_pos_left.append([self.enemy_pos[0] + a_val.TEMP_ENEMY_WIDTH / 2 -
                                                  a_val.MULTISHOT_WIDTH / 2 - a_val.MULTISHOT_WIDTH -
                                                  a_val.MULTISHOT_GAP_MODIFIER, self.enemy_pos[1] +
                                                  a_val.AIRPLANE_HEIGHT / 2])
                self.enemy_multi_pos_right.append([self.enemy_pos[0] + a_val.TEMP_ENEMY_WIDTH / 2 -
                                                   a_val.MULTISHOT_WIDTH / 2 + a_val.MULTISHOT_WIDTH +
                                                   a_val.MULTISHOT_GAP_MODIFIER,
                                                   self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT / 2])
            if bullet_type == 'bomb':
                self.enemy_bomb_shot_pos.append([self.enemy_pos[0] + a_val.AIRPLANE_WIDTH / 2
                                                - a_val.BOMB_SHOT_WIDTH / 2,
                                                 self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT / 2])
                self.enemy_bomb_shot_timer_counter.append(0)

            if bullet_type == 'spread':
                pos = [self.enemy_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.MULTISHOT_WIDTH / 2,
                       self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT]
                self.enemy_spread_pos.append(pos)
                self.enemy_spread_pos_left_1.append([pos[0] - a_val.MULTISHOT_WIDTH - a_val.MULTISHOT_GAP_MODIFIER,
                                                     pos[1]])
                self.enemy_spread_pos_left_2.append([pos[0] - 2*a_val.MULTISHOT_WIDTH - 2*a_val.MULTISHOT_GAP_MODIFIER,
                                                    pos[1]])
                self.enemy_spread_pos_right_1.append([pos[0] + a_val.MULTISHOT_WIDTH + a_val.MULTISHOT_GAP_MODIFIER,
                                                      pos[1]])
                self.enemy_spread_pos_right_2.append([pos[0] + 2 * a_val.MULTISHOT_WIDTH + 2 * a_val.MULTISHOT_GAP_MODIFIER,
                                                     pos[1]])

            if bullet_type == 'charge':
                if self.enemy_charge_counter < a_val.CHARGE_BEAM_COUNTER:
                    self.enemy_charge_counter += 1
                else:
                    pos = [self.enemy_pos[0] + a_val.AIRPLANE_WIDTH / 2 - a_val.CHARGE_BEAM_SHOT_WIDTH / 2,
                           self.enemy_pos[1] + a_val.AIRPLANE_HEIGHT]
                    self.enemy_charge_counter = 0
                    self.enemy_charge_pos.append(pos)
                    self.enemy_charge_timer.append(0)

    def airplane_moving_attack(self):  # not using

        self.bullet_counting()

        if self.player_normal_count >= a_val.BULLET_COUNT_TIME_PLAYER_NORMAL:
            self.generate_bullet('player', 'normal')
            self.player_normal_count = 0

        if self.player_multi_count >= a_val.BULLET_COUNT_TIME_PLAYER_MULTI:
            self.generate_bullet('player', 'multi')
            self.player_multi_count = 0

        if self.enemy_normal_count >= a_val.BULLET_COUNT_TIME_ENEMY_NORMAL:
            self.generate_bullet('enemy', 'normal')
            self.enemy_normal_count = 0

        if self.enemy_multi_count >= a_val.BULLET_COUNT_TIME_ENEMY_MULTI:
            self.generate_bullet('enemy', 'multi')
            self.enemy_multi_count = 0

    def unit_position_set(self):

        # self.airplane_action_counter['player'] += 1
        # self.airplane_action_counter['enemy'] += 1

        self.bullet_position_set()

        if G_val.PLAYING_MODE == 'EVE':
            self.airplane_moving_trigger()

        self.player_pos[0] += self.x_change
        self.player_pos[1] += self.y_change

        if self.player_pos[0] < 0:
            self.player_pos[0] = 0
        if self.player_pos[0] > a_val.BACKGROUND_WIDTH - a_val.AIRPLANE_WIDTH:
            self.player_pos[0] = a_val.BACKGROUND_WIDTH - a_val.AIRPLANE_WIDTH

        if self.player_pos[1] > a_val.BACKGROUND_HEIGHT - a_val.AIRPLANE_HEIGHT:
            self.player_pos[1] = a_val.BACKGROUND_HEIGHT - a_val.AIRPLANE_HEIGHT
        if self.player_pos[1] < a_val.BACKGROUND_HEIGHT/2:
            self.player_pos[1] = a_val.BACKGROUND_HEIGHT / 2

        self.enemy_pos[0] += self.enemy_x_change
        self.enemy_pos[1] += self.enemy_y_change

        if self.enemy_pos[0] < 0:
            self.enemy_pos[0] = 0
        if self.enemy_pos[0] > a_val.BACKGROUND_WIDTH - a_val.AIRPLANE_WIDTH:
            self.enemy_pos[0] = a_val.BACKGROUND_WIDTH - a_val.AIRPLANE_WIDTH

        if self.enemy_pos[1] < 0:
            self.enemy_pos[1] = 0
        if self.enemy_pos[1] > a_val.BACKGROUND_HEIGHT/2 - a_val.AIRPLANE_HEIGHT:
            self.enemy_pos[1] = ((a_val.BACKGROUND_HEIGHT / 2) - a_val.AIRPLANE_HEIGHT)

    def bullet_position_set(self):
        # print("bullet_position_set", self.charge_timer, self.enemy_charge_timer,
        # self.charge_counter, self.enemy_charge_counter)

        if self.normal_pos:
            for pos in self.normal_pos:
                pos[1] -= a_val.BULLET_SPEED

        if self.multi_pos:
            for pos in self.multi_pos:
                pos[1] -= a_val.BULLET_SPEED
        if self.multi_pos_left:
            for pos in self.multi_pos_left:
                pos[1] -= a_val.BULLET_SPEED
        if self.multi_pos_right:
            for pos in self.multi_pos_right:
                pos[1] -= a_val.BULLET_SPEED

        if self.spread_pos:
            for pos in self.spread_pos:
                pos[1] -= a_val.BULLET_SPEED
        if self.spread_pos_left_1:
            for pos in self.spread_pos_left_1:
                pos[0] += (1/1.7)*a_val.BULLET_SPEED
                pos[1] -= a_val.BULLET_SPEED
        if self.spread_pos_left_2:
            for pos in self.spread_pos_left_2:
                pos[0] += 1.7*a_val.BULLET_SPEED
                pos[1] -= a_val.BULLET_SPEED
        if self.spread_pos_right_1:
            for pos in self.spread_pos_right_1:
                pos[0] -= (1/1.7)*a_val.BULLET_SPEED
                pos[1] -= a_val.BULLET_SPEED
        if self.spread_pos_right_2:
            for pos in self.spread_pos_right_2:
                pos[0] -= 1.7*a_val.BULLET_SPEED
                pos[1] -= a_val.BULLET_SPEED

        if self.charge_timer:
            for counter_idx in range(len(self.charge_timer)):
                self.charge_timer[counter_idx] += 1
                if self.charge_timer[counter_idx] == a_val.CHARGE_BEAM_TIMER:
                    del self.charge_timer[counter_idx]
                    del self.charge_pos[counter_idx]

        if self.enemy_normal_pos:
            for pos in self.enemy_normal_pos:
                pos[1] += a_val.BULLET_SPEED

        if self.enemy_multi_pos:
            for pos in self.enemy_multi_pos:
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_multi_pos_left:
            for pos in self.enemy_multi_pos_left:
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_multi_pos_right:
            for pos in self.enemy_multi_pos_right:
                pos[1] += a_val.BULLET_SPEED
        
        if self.enemy_spread_pos:
            for pos in self.enemy_spread_pos:
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_spread_pos_left_1:
            for pos in self.enemy_spread_pos_left_1:
                pos[0] += (1/1.7)*a_val.BULLET_SPEED
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_spread_pos_left_2:
            for pos in self.enemy_spread_pos_left_2:
                pos[0] += 1.7*a_val.BULLET_SPEED
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_spread_pos_right_1:
            for pos in self.enemy_spread_pos_right_1:
                pos[0] -= (1/1.7)*a_val.BULLET_SPEED
                pos[1] += a_val.BULLET_SPEED
        if self.enemy_spread_pos_right_2:
            for pos in self.enemy_spread_pos_right_2:
                pos[0] -= 1.7*a_val.BULLET_SPEED
                pos[1] += a_val.BULLET_SPEED
                
        if self.bomb_shot_timer_counter:
            for counter_idx in range(len(self.bomb_shot_timer_counter)):
                self.bomb_shot_timer_counter[counter_idx] += 1
                if self.bomb_shot_timer_counter[counter_idx] == a_val.BOMB_SHOT_TIMER:
                    del self.bomb_shot_timer_counter[counter_idx]
                    del self.bomb_shot_pos[counter_idx]
                    
        if self.enemy_bomb_shot_timer_counter:
            for counter_idx in range(len(self.enemy_bomb_shot_timer_counter)):
                self.enemy_bomb_shot_timer_counter[counter_idx] += 1
                if self.enemy_bomb_shot_timer_counter[counter_idx] == a_val.BOMB_SHOT_TIMER:
                    del self.enemy_bomb_shot_timer_counter[counter_idx]
                    del self.enemy_bomb_shot_pos[counter_idx]

        if self.enemy_charge_timer:
            for counter_idx in range(len(self.enemy_charge_timer)):
                self.enemy_charge_timer[counter_idx] += 1
                if self.enemy_charge_timer[counter_idx] == a_val.CHARGE_BEAM_TIMER:
                    del self.enemy_charge_timer[counter_idx]
                    del self.enemy_charge_pos[counter_idx]

    def multishot_draw(self):
        if self.multi_pos:
            for pos in self.multi_pos:
                self.draw_object(self.multishot, pos)
        if self.multi_pos_left:
            for pos in self.multi_pos_left:
                self.draw_object(self.multishot, pos)
        if self.multi_pos_right:
            for pos in self.multi_pos_right:
                self.draw_object(self.multishot, pos)
    
    def spread_draw(self):
        if self.spread_pos:
            for pos in self.spread_pos:
                self.draw_object(self.multishot, pos)
        if self.spread_pos_left_1:
            for pos in self.spread_pos_left_1:
                self.draw_object(self.multishot, pos)
        if self.spread_pos_left_2:
            for pos in self.spread_pos_left_2:
                self.draw_object(self.multishot, pos)
        if self.spread_pos_right_1:
            for pos in self.spread_pos_right_1:
                self.draw_object(self.multishot, pos)
        if self.spread_pos_right_2:
            for pos in self.spread_pos_right_2:
                self.draw_object(self.multishot, pos)
                
    def charge_shot_draw(self):
        if self.charge_pos:
            for pos in self.charge_pos:
                width = int(a_val.CHARGE_BEAM_SHOT_WIDTH)
                height = deepcopy(pos[1])
                height = int(height)
                self.charged_shot = pygame.transform.scale(self.charged_shot, (width, height))
                self.draw_object(self.charged_shot, (pos[0], 0))
        pass

    def bombshot_draw(self):

        if self.bomb_shot_pos:
            for pos in self.bomb_shot_pos:
                self.draw_object(self.bomb_shot, pos)

    def enemy_drawing(self):

        if self.enemy_normal_pos:
            for pos in self.enemy_normal_pos:
                self.draw_object(self.enemy_normal, pos)

        if self.enemy_multi_pos:
            for pos in self.enemy_multi_pos:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_multi_pos_left:
            for pos in self.enemy_multi_pos_left:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_multi_pos_right:
            for pos in self.enemy_multi_pos_right:
                self.draw_object(self.enemy_multi, pos)

        if self.enemy_bomb_shot_pos:
            for pos in self.enemy_bomb_shot_pos:
                self.draw_object(self.bomb_shot, pos)
                
        if self.enemy_spread_pos:
            for pos in self.enemy_spread_pos:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_spread_pos_left_1:
            for pos in self.enemy_spread_pos_left_1:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_spread_pos_left_2:
            for pos in self.enemy_spread_pos_left_2:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_spread_pos_right_1:
            for pos in self.enemy_spread_pos_right_1:
                self.draw_object(self.enemy_multi, pos)
        if self.enemy_spread_pos_right_2:
            for pos in self.enemy_spread_pos_right_2:
                self.draw_object(self.enemy_multi, pos)

        if self.enemy_charge_pos:
            for pos in self.enemy_charge_pos:
                width = int(a_val.CHARGE_BEAM_SHOT_WIDTH)
                height = int(a_val.BACKGROUND_HEIGHT - pos[1])
                self.charged_shot = pygame.transform.scale(self.charged_shot, (width, height))
                self.draw_object(self.charged_shot, pos)

    def bullet_hit_scan(self, bullet_pos, bullet_size, target_pos, target_size, target_code):
        if bullet_pos and target_pos:
            for pos in bullet_pos:
                temp_x = [pos[0], pos[0] + bullet_size[0], target_pos[0], target_pos[0] + target_size[0]]
                temp_y = [pos[1], pos[1] + bullet_size[1], target_pos[1], target_pos[1] + target_size[1]]
                if max(temp_x) - min(temp_x) <= bullet_size[0] + target_size[0] and max(temp_y) - min(temp_y) \
                        <= bullet_size[1] + target_size[1]:
                    if target_code in (21, 22, 31, 32):
                        pass
                    else:
                        bullet_pos.remove(pos)
                    self.crashed(target_code)
                elif (pos[0] > a_val.BACKGROUND_WIDTH or pos[0] < 0) and pos is not None \
                        and target_code not in(21, 22, 31, 32):
                    bullet_pos.remove(pos)

    def all_bullet_scan_out_window(self):

        temp_pos = [0, - a_val.BACKGROUND_HEIGHT]
        temp_size = [a_val.BACKGROUND_WIDTH, a_val.BACKGROUND_HEIGHT]

        normal_size = [a_val.NORMAL_ATTACK_WIDTH, a_val.NORMAL_ATTACK_HEIGHT]
        multishot_size = [a_val.MULTISHOT_WIDTH, a_val.MULTISHOT_HEIGHT]
        charged_size = [a_val.CHARGE_BEAM_SHOT_WIDTH, a_val.CHARGE_BEAM_SHOT_HEIGHT]

        self.bullet_hit_scan(self.normal_pos, normal_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.multi_pos, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.multi_pos_left, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.multi_pos_right, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)

        self.bullet_hit_scan(self.spread_pos, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.spread_pos_left_1, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.spread_pos_left_2, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.spread_pos_right_1, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.spread_pos_right_2, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)

        temp_pos = [0, a_val.BACKGROUND_HEIGHT]
        temp_size = [a_val.BACKGROUND_WIDTH, a_val.BACKGROUND_HEIGHT]
        normal_size = [a_val.TEMP_ENEMY_NORMAL_WIDTH, a_val.TEMP_ENEMY_NORMAL_HEIGHT]

        self.bullet_hit_scan(self.enemy_normal_pos, normal_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_multi_pos, normal_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_multi_pos_right, normal_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_multi_pos_left, normal_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        
        self.bullet_hit_scan(self.enemy_spread_pos, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_spread_pos_left_1, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_spread_pos_left_2, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_spread_pos_right_1, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)
        self.bullet_hit_scan(self.enemy_spread_pos_right_2, multishot_size, temp_pos, temp_size, a_val.CODE_DUMMY)

    def bullet_scan_all(self):

        self.all_bullet_scan_out_window()

        self.bullet_hit_temp_enemy()

        self.bullet_hit_me()

    def bullet_hit_scan_normalshot(self, target_pos, target_size, target_code):
        normal_size = [a_val.NORMAL_ATTACK_WIDTH, a_val.NORMAL_ATTACK_HEIGHT]
        if self.normal_pos and target_pos:
            self.bullet_hit_scan(self.normal_pos, normal_size, target_pos, target_size, target_code)

    def bullet_hit_scan_multishot(self, target_pos, target_size, target_code):
        multishot_size = [a_val.MULTISHOT_WIDTH, a_val.MULTISHOT_HEIGHT]
        self.bullet_hit_scan(self.multi_pos, multishot_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.multi_pos_left, multishot_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.multi_pos_right, multishot_size, target_pos, target_size, target_code)

    def bullet_hit_scan_shield(self, bullet_pos, target_pos, target_size, target_code):
        pass

    def bullet_hit_scan_spread(self, target_pos, target_size, target_code):
        bullet_size = [a_val.MULTISHOT_WIDTH, a_val.MULTISHOT_HEIGHT]
        self.bullet_hit_scan(self.spread_pos, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.spread_pos_left_1, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.spread_pos_left_2, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.spread_pos_right_1, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.spread_pos_right_2, bullet_size, target_pos, target_size, target_code)

    def bullet_hit_scan_bomb(self, target_pos, target_size, target_code):
        size = [a_val.BOMB_SHOT_WIDTH, a_val.BOMB_SHOT_HEIGHT]
        self.bullet_hit_scan(self.bomb_shot_pos, size, target_pos, target_size, target_code)

    def bullet_hit_scan_charge_shot(self, target_pos, target_size, target_code):
        size = self.charged_shot.get_size()
        self.bullet_hit_scan(self.charge_pos, size, target_pos, target_size, target_code)

    def bullet_hit_temp_enemy(self):
        temp_enemy_size = [a_val.TEMP_ENEMY_WIDTH, a_val.TEMP_ENEMY_HEIGHT]
        if self.enemy_pos:
            self.bullet_hit_scan_normalshot(self.enemy_pos, temp_enemy_size, a_val.CODE_TEMP_ENEMY)
            self.bullet_hit_scan_multishot(self.enemy_pos, temp_enemy_size, a_val.CODE_TEMP_ENEMY)
            self.bullet_hit_scan_spread(self.enemy_pos, temp_enemy_size, a_val.CODE_TEMP_ENEMY)
            self.bullet_hit_scan_bomb(self.enemy_pos, temp_enemy_size, a_val.CODE_TEMP_ENEMY_BOMB)
            self.bullet_hit_scan_charge_shot(self.enemy_pos, temp_enemy_size, a_val.CODE_TEMP_ENEMY_CHARGE)

    def bullet_hit_scan_normalshot_me(self, target_pos, target_size, target_code):
        normal_size = [a_val.TEMP_ENEMY_NORMAL_WIDTH, a_val.TEMP_ENEMY_NORMAL_HEIGHT]
        if self.enemy_normal_pos and target_pos:
            self.bullet_hit_scan(self.enemy_normal_pos, normal_size, target_pos, target_size, target_code)

    def bullet_hit_scan_multishot_me(self, target_pos, target_size, target_code):
        multishot_size = [a_val.ENEMY_MULTISHOT_WIDTH, a_val.ENEMY_MULTISHOT_HEIGHT]

        if self.enemy_multi_pos:
            self.bullet_hit_scan(self.enemy_multi_pos, multishot_size, target_pos, target_size, target_code)
        if self.enemy_multi_pos_left:
            self.bullet_hit_scan(self.enemy_multi_pos_left, multishot_size, target_pos, target_size, target_code)
        if self.enemy_multi_pos_right:
            self.bullet_hit_scan(self.enemy_multi_pos_right, multishot_size, target_pos, target_size, target_code)

    def bullet_hit_scan_spread_me(self, target_pos, target_size, target_code):
        bullet_size = [a_val.MULTISHOT_WIDTH, a_val.MULTISHOT_HEIGHT]
        self.bullet_hit_scan(self.enemy_spread_pos, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.enemy_spread_pos_left_1, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.enemy_spread_pos_left_2, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.enemy_spread_pos_right_1, bullet_size, target_pos, target_size, target_code)
        self.bullet_hit_scan(self.enemy_spread_pos_right_2, bullet_size, target_pos, target_size, target_code)

    def bullet_hit_scan_bomb_me(self, target_pos, target_size, target_code):
        size = [a_val.BOMB_SHOT_WIDTH, a_val.BOMB_SHOT_HEIGHT]
        self.bullet_hit_scan(self.enemy_bomb_shot_pos, size, target_pos, target_size, target_code)

    def bullet_hit_scan_charge_shot_me(self, target_pos, target_size, target_code):
        size = self.charged_shot.get_size()
        self.bullet_hit_scan(self.enemy_charge_pos, size, target_pos, target_size, target_code)

    def bullet_hit_me(self):
        temp_me_size = [a_val.AIRPLANE_WIDTH, a_val.AIRPLANE_HEIGHT]
        if self.player_pos:
            self.bullet_hit_scan_normalshot_me(self.player_pos, temp_me_size, a_val.CODE_HIT_ME)
            self.bullet_hit_scan_multishot_me(self.player_pos, temp_me_size, a_val.CODE_HIT_ME)
            self.bullet_hit_scan_spread_me(self.player_pos, temp_me_size, a_val.CODE_HIT_ME)
            self.bullet_hit_scan_bomb_me(self.player_pos, temp_me_size, a_val.CODE_HIT_ME_BOMB)
            self.bullet_hit_scan_charge_shot_me(self.player_pos, temp_me_size, a_val.CODE_HIT_ME_CHARGE)

    def crashed(self, target_code):
        if target_code == 1:
            for pos in self.shield_pos:
                self.shield_pos.remove(pos)

        elif target_code == 2:
            self.enemy_hits += 1
            if self.enemy_hits == a_val.GAME_HEALTH:
                print("Enemy dead", self.enemy_hits)
                self.game_defeated_plane = "Enemy"
                self.finishing_sequence()

        elif target_code == 21:
            self.enemy_hits += 3
            if self.enemy_hits == a_val.GAME_HEALTH:
                print("Enemy dead", self.enemy_hits)
                self.game_defeated_plane = "Enemy"
                self.finishing_sequence()

        elif target_code == 22:
            self.enemy_hits += 5
            if self.enemy_hits == a_val.GAME_HEALTH:
                print("Enemy dead", self.enemy_hits)
                self.game_defeated_plane = "Enemy"
                self.finishing_sequence()

        elif target_code == 3:
            self.player_hits += 1
            if self.player_hits == a_val.GAME_HEALTH:
                print("player dead", self.player_hits)
                self.game_defeated_plane = "Player"
                self.finishing_sequence()

        elif target_code == 31:
            self.player_hits += 3
            if self.player_hits == a_val.GAME_HEALTH:
                print("player dead", self.player_hits)
                self.game_defeated_plane = "Player"
                self.finishing_sequence()

        elif target_code == 32:
            self.player_hits += 5
            if self.player_hits == a_val.GAME_HEALTH:
                print("player dead", self.player_hits)
                self.game_defeated_plane = "Player"
                self.finishing_sequence()

    def teleport_event_handler(self):
        self.flag_teleport = 0
        self.skill_ui_array[a_val.IDX_TELEPORT] = pygame.image.load(a_val.TELEPORT_IMAGE_PATH)

    def multishot_event_handler(self):
        if self.multishot_ammo < 20:
            self.multishot_ammo += 1

    @staticmethod
    def grayscale(img):
        # https://stackoverflow.com/questions/10261440/how-can-i-make-a-greyscale-copy-of-a-surface-in-pygame
        arr = pygame.surfarray.array3d(img)
        # luminosity filter
        avgs = [[(r * 0.3 + g * 0.3 + b * 0.3) for (r, g, b) in col] for col in arr]
        arr = numpy.array([[[avg, avg, avg] for avg in col] for col in avgs])
        return pygame.surfarray.make_surface(arr)

    def draw_object(self, obj, pos):
        self.game.blit(obj, (pos[0], pos[1]))

    def units_drawing(self):

        self.draw_object(self.background_1, (0, 0))
        self.draw_object(self.airplane, self.player_pos)

        if self.enemy_pos:
            self.draw_object(self.enemy, self.enemy_pos)

        if self.normal_pos:
            for pos in self.normal_pos:
                self.draw_object(self.normal_attack, pos)

        self.multishot_draw()
        self.bombshot_draw()
        self.spread_draw()
        self.charge_shot_draw()

        # 이 부분 수정해서 깔끔하게 정리 해야 됨
        # font = self.font
        # text = font.render("Health : ", False, a_val.BLACK)
        # self.game.blit(text, (a_val.HEALTH_POS[0] - a_val.HEALTH_TEXT_GAP[0], a_val.HEALTH_POS[1] - a_val.HEALTH_TEXT_GAP[1]))

        temp_rect = pygame.Rect(a_val.HEALTH_POS[0], a_val.HEALTH_POS[1], self.health_size[0], self.health_size[1])
        pygame.draw.rect(self.game, self.health_color, temp_rect)

        self.enemy_drawing()

    def init_states(self):
        if not self.state_player_before:
            self.update_state_bullets()
            self.state_player_before = [self.player_pos[:], self.state_player_bullets[:],
                                        self.state_player_bullets_number[:]]
            self.state_enemy_before = [self.enemy_pos[:], self.state_enemy_bullets[:],
                                       self.state_enemy_bullets_number[:]]

    def update_state_bullets(self):

        self.state_player_bullets = [self.normal_pos[:], self.multi_pos[:], self.multi_pos_left[:],
                                     self.multi_pos_right[:]]
        self.state_player_bullets_number = [len(self.normal_pos[:]), len(self.multi_pos[:]),
                                            len(self.spread_pos), len(self.bomb_shot_pos),
                                            len(self.charge_pos), self.charge_counter]
        self.none_to_string(self.state_player_bullets)
        self.none_to_string(self.state_player_bullets_number)

        self.state_enemy_bullets = [self.enemy_normal_pos[:], self.enemy_multi_pos[:],
                                    ]
        self.state_enemy_bullets_number = [len(self.enemy_normal_pos[:]), len(self.enemy_multi_pos[:]),
                                           len(self.enemy_spread_pos), len(self.enemy_bomb_shot_pos),
                                           len(self.enemy_charge_pos), self.enemy_charge_counter]
        self.none_to_string(self.state_enemy_bullets)
        self.none_to_string(self.state_enemy_bullets_number)

    def save_states(self):
        self.update_state_bullets()
        if self.state_player_after:
            self.state_player_before = self.state_player_after[:]
            self.state_player_after = [self.player_pos[:], self.state_player_bullets[:],
                                       self.state_player_bullets_number[:]]

            self.state_enemy_before = self.state_enemy_after[:]
            self.state_enemy_after = [self.enemy_pos[:], self.state_enemy_bullets[:],
                                      self.state_enemy_bullets_number[:]]

        elif not self.state_player_after:
            self.state_player_after = [self.player_pos[:], self.state_player_bullets[:],
                                       self.state_player_bullets_number[:]]
            self.state_enemy_after = [self.enemy_pos[:], self.state_enemy_bullets[:],
                                      self.state_enemy_bullets_number[:]]

    def checking_movements(self, airplane_mode):
        player_result = ['0' for i in range(4)]   # [up, down, left, right]
        enemy_result = ['0' for i in range(4)]
        if airplane_mode == 'player' and self.state_player_after:
            temp_storage_pos = a_val.vector_minus(self.state_player_after[0], self.state_player_before[0])
            if temp_storage_pos[0] < 0:
                player_result[2] = '1'
            if temp_storage_pos[0] > 0:
                player_result[3] = '1'
            if temp_storage_pos[1] < 0:
                player_result[0] = '1'
            if temp_storage_pos[1] > 0:
                player_result[1] = '1'
            return player_result

        elif airplane_mode == 'enemy' and self.state_enemy_after:
            temp_storage_pos = a_val.vector_minus(self.state_enemy_after[0], self.state_enemy_before[0])
            if temp_storage_pos[0] < 0:
                enemy_result[2] = '1'
            if temp_storage_pos[0] > 0:
                enemy_result[3] = '1'
            if temp_storage_pos[1] < 0:
                enemy_result[0] = '1'
            if temp_storage_pos[1] > 0:
                enemy_result[1] = '1'
            return enemy_result

    def checking_attacks(self, airplane_mode, bullet_type):
        if airplane_mode == 'player' and self.state_player_after:
            before = self.state_player_before
            after = self.state_player_after

            if bullet_type == 'normal':
                temp_storage_attacks = self.checking_attacks_basic(before, after, a_val.NORMAL_INDEX)
                if temp_storage_attacks > 0:
                    return 'normal'
                else:
                    return "Nothing"

            elif bullet_type == 'multi':
                temp_storage_attacks = self.checking_attacks_basic(before, after, a_val.MULTISHOT_INDEX)
                if temp_storage_attacks > 0:
                    return 'multi'
                else:
                    return "Nothing"
                
            elif bullet_type == 'spread':
                temp_storage_attacks = self.checking_attacks_basic(before, after, a_val.SPREAD_INDEX)
                if temp_storage_attacks > 0:
                    return 'spread'
                else:
                    return "Nothing"

            elif bullet_type == 'bomb':
                temp_storage_attacks = self.checking_attacks_basic(before, after, a_val.BOMB_INDEX)
                if temp_storage_attacks > 0:
                    return 'bomb'
                else:
                    return "Nothing"

            elif bullet_type == 'charge':
                charge = self.checking_attacks_basic(before, after, a_val.CHARGE_INDEX)
                if charge > 0:
                    return 'charge'

                else:
                    return "Nothing"

        elif airplane_mode == 'enemy' and self.state_enemy_after:
            before_enemy = self.state_enemy_before
            after_enemy = self.state_enemy_after

            if bullet_type == 'normal':
                temp_storage_attacks = self.checking_attacks_basic(before_enemy, after_enemy, a_val.NORMAL_INDEX)
                if temp_storage_attacks > 0:
                    return 'normal'
                else:
                    return "Nothing"

            elif bullet_type == 'multi':
                temp_storage_attacks = self.checking_attacks_basic(before_enemy, after_enemy, a_val.MULTISHOT_INDEX)
                if temp_storage_attacks > 0:
                    return 'multi'
                else:
                    return "Nothing"

            elif bullet_type == 'spread':
                temp_storage_attacks = self.checking_attacks_basic(before_enemy, after_enemy, a_val.SPREAD_INDEX)
                if temp_storage_attacks > 0:
                    return 'spread'
                else:
                    return "Nothing"

            elif bullet_type == 'bomb':
                temp_storage_attacks = self.checking_attacks_basic(before_enemy, after_enemy, a_val.BOMB_INDEX)
                if temp_storage_attacks > 0:
                    return 'bomb'
                else:
                    return "Nothing"

            elif bullet_type == 'charge':
                charge = self.checking_attacks_basic(before_enemy, after_enemy, a_val.CHARGE_INDEX)
                if charge > 0:
                    return 'charge'
                
                else:
                    return "Nothing"

    @staticmethod
    def checking_attacks_basic(airplane_state_before, airplane_stare_after, bullet_type_index):
        if airplane_state_before[2][bullet_type_index] is 'None':
            before_number = 0
        else:
            before_number = airplane_state_before[2][bullet_type_index]

        if airplane_stare_after[2][bullet_type_index] is "None":
            after_number = 0
        else:
            after_number = airplane_stare_after[2][bullet_type_index]

        return after_number - before_number

    def temp_algorithm_testing(self):
        self.init_states()
        self.save_states()
        self.saving_data()
        # print("Saved data : ", self.saved_data_player, self.saved_data_enemy)
        self.saved_data_player = []
        self.saved_data_enemy = []

    def saving_data(self):
        self.saved_data_player.append([self.checking_movements('player'),
                                       [self.checking_attacks('player', 'normal'),
                                        self.checking_attacks('player', 'multi'),
                                       self.checking_attacks('player', 'spread'),
                                       self.checking_attacks('player', 'bomb'),
                                       self.checking_attacks('player', 'charge')],
                                       self.player_hits])
        self.saved_data_enemy.append([self.checking_movements('enemy'),
                                      [self.checking_attacks('enemy', 'normal'),
                                       self.checking_attacks('enemy', 'multi'),
                                       self.checking_attacks('enemy', 'spread'),
                                       self.checking_attacks('enemy', 'bomb'),
                                       self.checking_attacks('enemy', 'charge')],
                                      self.enemy_hits])
        self.saved_data_all.append([self.saved_data_player, self.saved_data_enemy])

    def writing_data(self):

        mode_p = G_val.PLAYER_GAME_MODE
        mode_e = G_val.ENEMY_GAME_MODE
        counter_pattern = a_val.SAVE_PATTERN_COUNTER[0]
        counter_seq = a_val.SAVE_COUNTER[0]

        pattern = 'pattern' + str(counter_pattern + 1)
        seq = 'sequence' + str(counter_seq)

        loc = a_val.TEXT_LOCATION_FRONT + str(G_val.GENE_COUNTER[0] + 1) + a_val.TEXT_LOCATION_BACK + a_val.SAVE_PATH[
            a_val.SAVE_PATH_COUNTER[0]]
        a_val.create_path(loc)

        p = 'player' + str(a_val.SAVE_COUNTER[0])
        e = 'enemy' + str(a_val.SAVE_COUNTER[0])
        for data in self.saved_data_all:
            text_dir = ",".join(data[0][0][0])
            text_bul = ",".join(data[0][0][1])
            text = text_dir + "," + text_bul + "," + str(data[0][0][2]) + "\n"
            a_val.saving_text(text, p, location=loc)

            text_dir2 = ",".join(data[1][0][0])
            text_bul2 = ",".join(data[1][0][1])
            text2 = text_dir2 + "," + text_bul2 + "," + str(data[1][0][2]) + "\n"
            a_val.saving_text(text2, e, location=loc)

        last_text = "sequence_end // defeated : " + self.game_defeated_plane + "\n"
        a_val.saving_text(last_text, p, location=loc)
        a_val.saving_text(last_text, e, location=loc)

        if mode_p == 'GA learner':
            description_p = "pattern description : " + self.behaviors_player[mode_p][pattern][seq]['description']
            a_val.saving_text(description_p, p, location=loc)

        if mode_e == 'GA tester':
            description_e = "pattern description : " + self.behaviors_enemy[mode_e][pattern]['description']
            a_val.saving_text(description_e, e, location=loc)

    def finishing_sequence(self):
        self.saving_data()

        a_val.SAVE_COUNTER[0] += 1
        if a_val.SAVE_COUNTER[0] >= a_val.PATTERN_ITER_NUMBER:
            if a_val.SAVE_PATTERN_COUNTER[0] < a_val.TESTER_PATTERN_NUMBERS:

                self.game_status = False
                pygame.quit()
                self.writing_data()
                a_val.SAVE_COUNTER[0] = 0
                a_val.SAVE_PATH_COUNTER[0] += 1
                a_val.SAVE_PATTERN_COUNTER[0] += 1
                if a_val.SAVE_PATTERN_COUNTER[0] == a_val.TESTER_PATTERN_NUMBERS:

                    self.game_status = False
                    pygame.quit()
                    if a_val.Running_mode == 'gaming':
                        ga.play.__init__()
                        ga.play.generating()
                        # GA와 연동이 필요함! 일단은 무턱대고 종료하는 알고리즘!
                        # quit()  : 일단 막아둠.
                        a_val.SAVE_PATTERN_COUNTER[0] = 0
                        a_val.SAVE_PATH_COUNTER[0] = 0
                        if G_val.GENE_COUNTER[0] == G_val.NUMBER_OF_GENERATION:
                            quit()
                        else:
                            self.__init__()
                else:

                    self.__init__()

        elif a_val.SAVE_COUNTER[0] < a_val.PATTERN_ITER_NUMBER:

            self.game_status = False
            pygame.quit()
            self.writing_data()
            self.__init__()

    @staticmethod
    def none_to_string(given_list):
        for idx in range(len(given_list)):
            if not given_list[idx]:
                given_list[idx] = 'None'
