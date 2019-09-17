import airplane_front_making_behaviors_variables as val
import General_variables as G_val


class CreatingBehaviors:

    def __init__(self):
        self.behaviors_player = dict()
        self.behaviors_enemy = dict()

        self.main_path = val.CHILD_PATH_FRONT + str(G_val.GENE_COUNTER[0]) + val.CHILD_PATH_BACK
        self.sub_name = val.SUB_FILE_NAME

        self.number_pattern = val.PATTERN_NUMBER
        self.number_iter = val.ITERATION_NUMBER

        self.init_behaviors()

        self.read_ga_result()

    def init_behaviors(self):
        self.behaviors_player['GA learner'] = dict()
        self.behaviors_player['GA tester'] = dict()
        self.behaviors_enemy['GA learner'] = dict()
        self.behaviors_enemy['GA tester'] = dict()

        mode_p = G_val.PLAYER_GAME_MODE
        mode_e = G_val.ENEMY_GAME_MODE
        self.behaviors_player[mode_p] = dict()
        self.behaviors_enemy[mode_e] = dict()

        for num_pat in range(self.number_pattern):

            if mode_p == 'GA learner':
                self.behaviors_player[mode_p]['pattern' + str(num_pat + 1)] = dict()
            if mode_e == 'GA learner':
                self.behaviors_enemy[mode_e]['pattern' + str(num_pat + 1)] = dict()

    def read_lines(self, airplane_type, pattern_number, child_number=1):
        mode_p = G_val.PLAYER_GAME_MODE
        if airplane_type == 'player':

            path_type = '\Player'

            if G_val.PLAYER_GAME_MODE == 'GA learner':
                path = self.main_path + path_type + "\pattern" + str(pattern_number + 1) + self.sub_name + str(
                    child_number + 1)
                path += ".txt"

                files = open(path, 'r')

                while True:
                    line = files.readline()

                    if not line:
                        break

                    else:
                        pat = 'pattern' + str(pattern_number + 1)
                        seq = 'sequence' + str(child_number + 1)
                        self.behaviors_player[mode_p][pat][seq]['moving'].append(line.rstrip())
                        self.behaviors_player[mode_p][pat][seq]['description'] = ""

        if airplane_type == 'enemy':
            mode_e = G_val.ENEMY_GAME_MODE
            path_type = '\Enemy'

            if G_val.ENEMY_GAME_MODE == 'GA tester':
                    path = self.main_path + path_type + "\pattern" + str(pattern_number + 1)
                    path += ".txt"
                    files = open(path, 'r')

                    while True:
                        line = files.readline()

                        if not line:
                            break

                        else:
                            self.behaviors_enemy[mode_e]['pattern' + str(pattern_number + 1)]['moving'].append(
                                line.rstrip())
                            self.behaviors_enemy[mode_e]['pattern' + str(pattern_number + 1)]['description'] = ""

    def read_ga_result(self):
        mode_p = G_val.PLAYER_GAME_MODE
        mode_e = G_val.ENEMY_GAME_MODE

        for num_pat in range(self.number_pattern):

            if mode_e == 'GA tester':
                self.behaviors_enemy[mode_e]['pattern' + str(num_pat + 1)] = dict()
                self.behaviors_enemy[mode_e]['pattern' + str(num_pat + 1)]['moving'] = list()
                self.read_lines('enemy', num_pat)

            if mode_p == 'GA learner':

                for num_it in range(self.number_iter):
                    self.behaviors_player[mode_p]['pattern' + str(num_pat + 1)]['sequence' + str(num_it + 1)] = dict()
                    self.behaviors_player[mode_p]['pattern' + str(num_pat + 1)]['sequence' + str(num_it + 1)]['moving'] = list()
                    self.read_lines('player', num_pat, num_it)
