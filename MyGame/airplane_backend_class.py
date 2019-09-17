import airplane_backend_variables as val
import airplane_frontend_variables as main_val
import General_variables as G_val
import copy
import math
import numpy
import os


# 연동 시작 전에 GA_val 쪽에서 pattern counter 바꿔주는거 잊지 말기 !
# + Generate GA쪽 코드도 수정 해야댐 !
class GeneticAlgorithmClass:
    def __init__(self):
        print("Generation : ", G_val.GENE_COUNTER[0])
        front = val.RESULT_FILE_LOCATION_FRONT
        back = val.RESULT_FILE_LOCATION_BACK
        loc = front + str(G_val.GENE_COUNTER[0] + 1) + back
        loc += val.RESULT_PATTERN_NAME
        self.sequence_result_location_basic = loc

        self.code_path = val.CODE_PATH_FRONT + str(G_val.GENE_COUNTER[0] + 1) + val.CODE_PATH_BACK
        self.sub_name = val.SUB_CODE_NAME

        self.dummy_using_dict = dict()

        self.sequence_result_player = {}
        self.sequence_result_enemy = {}

        self.health_difference_player = dict()
        self.health_difference_enemy = dict()

        self.duration_player = []
        self.duration_enemy = []

        self.eval_storage_player = dict()
        self.eval_storage_enemy = dict()

        self.parents_player = dict()
        self.parents_enemy = dict()

        self.children_player = dict()
        self.children_enemy = dict()

    def generating(self):

        self.init_variables()
        self.read_sequence_result()  # This function should run earlier than any others!!

        self.making_health_difference()
        self.all_eval()

        self.extract_parents()
        self.create_children()

        self.children_to_code()

        self.writing_code()

        G_val.GENE_COUNTER[0] += 1

    def init_variables(self):
        counter_pattern = val.PATTERN_COUNTER[0]
        counter_sequence = val.PATTERN_ITER_NUMBER

        for pattern_num in range(counter_pattern):
            self.eval_storage_player['pattern' + str(pattern_num + 1)] = dict()
            self.eval_storage_enemy['pattern' + str(pattern_num + 1)] = dict()
            self.dummy_using_dict['pattern' + str(pattern_num + 1)] = dict()
            for num_sequence in range(counter_sequence):
                self.eval_storage_player['pattern' + str(pattern_num + 1)]['sequence' + str(num_sequence + 1)] = dict()
                self.eval_storage_enemy['pattern' + str(pattern_num + 1)]['sequence' + str(num_sequence + 1)] = dict()
                self.dummy_using_dict['pattern' + str(pattern_num + 1)]['sequence' + str(num_sequence + 1)] = dict()

    def read_sequence_result(self):
        counter_pattern = 0
        counter_sequence = 0

        for pattern in range(val.PATTERN_COUNTER[0]):
            self.sequence_result_player['pattern' + str(pattern + 1)] = {}
            self.sequence_result_enemy['pattern' + str(pattern + 1)] = {}
            for sequence in range(val.PATTERN_ITER_NUMBER):
                self.sequence_result_player['pattern' + str(pattern + 1)]['sequence' + str(sequence + 1)] = {}
                self.sequence_result_player['pattern' + str(pattern + 1)]['sequence' + str(sequence + 1)][
                    'values'] = []
                self.sequence_result_enemy['pattern' + str(pattern + 1)]['sequence' + str(sequence + 1)] = {}
                self.sequence_result_enemy['pattern' + str(pattern + 1)]['sequence' + str(sequence + 1)][
                    'values'] = []

        while counter_pattern < val.PATTERN_COUNTER[0]:

            path_player = self.sequence_result_location_basic + str(counter_pattern + 1) + val.RESULT_FILE_NAME \
                          + 'player' + str(counter_sequence + 1) + '.txt'
            path_enemy = self.sequence_result_location_basic + str(counter_pattern + 1) +\
                         val.RESULT_FILE_NAME + 'enemy' + str(counter_sequence + 1) + '.txt'

            file_controller_player = open(path_player, 'r')
            file_controller_enemy = open(path_enemy, 'r')

            while counter_sequence < val.PATTERN_ITER_NUMBER:
                line_player = file_controller_player.readline()
                line_enemy = file_controller_enemy.readline()
                if not line_player:
                    break

                if line_player[0] and line_enemy[0] == 's':
                    loser = line_player.split(":")[1].rstrip()
                    self.sequence_result_enemy['pattern' + str(counter_pattern + 1)][
                        'sequence' + str(counter_sequence + 1)]['loser'] = loser
                    self.sequence_result_player['pattern' + str(counter_pattern + 1)][
                        'sequence' + str(counter_sequence + 1)]['loser'] = loser
                    counter_sequence += 1

                    if counter_sequence >= val.PATTERN_ITER_NUMBER:
                        counter_sequence = 0
                        counter_pattern += 1
                        break

                elif line_player[0] != 's' and line_enemy[0] != 's' and line_player[0] != 'p' and line_enemy[0] != 'p':

                    newline_p = line_player.split(",")
                    newline_p[9] = int(newline_p[9].rstrip())
                    newline_p[0:4] = [int(i) for i in newline_p[0:4]]

                    newline_e = line_enemy.split(",")
                    newline_e[9] = int(newline_e[9].rstrip())
                    newline_e[0:4] = [int(i) for i in newline_e[0:4]]

                    self.sequence_result_player['pattern' + str(counter_pattern + 1)][
                        'sequence' + str(counter_sequence + 1)]['values'].append(newline_p)
                    self.sequence_result_enemy['pattern' + str(counter_pattern + 1)][
                        'sequence' + str(counter_sequence + 1)]['values'].append(newline_e)

    def making_health_difference(self):

        temp_player = copy.deepcopy(self.sequence_result_player)
        temp_enemy = copy.deepcopy(self.sequence_result_enemy)

        result_player_temp = []
        result_enemy_temp = []
        for pattern in temp_player.keys():

            self.health_difference_player[pattern] = dict()
            self.health_difference_enemy[pattern] = dict()

            for seq in temp_player[pattern].keys():

                self.health_difference_player[pattern][seq] = dict()
                self.health_difference_enemy[pattern][seq] = dict()

                for item_idx in range(len(temp_player[pattern][seq]['values'])):

                    result_player_temp.append(-temp_player[pattern][seq]['values'][item_idx][val.HEALTH_INDEX] +
                                              temp_enemy[pattern][seq]['values'][item_idx][val.HEALTH_INDEX])
                    result_enemy_temp.append(temp_player[pattern][seq]['values'][item_idx][val.HEALTH_INDEX] -
                                             temp_enemy[pattern][seq]['values'][item_idx][val.HEALTH_INDEX])

                self.health_difference_player[pattern][seq]['values'] = result_player_temp
                self.health_difference_enemy[pattern][seq]['values'] = result_enemy_temp

                self.health_difference_player[pattern][seq]['max'] = max(result_player_temp)
                self.health_difference_player[pattern][seq]['min'] = min(result_player_temp)
                self.health_difference_enemy[pattern][seq]['max'] = max(result_enemy_temp)
                self.health_difference_enemy[pattern][seq]['min'] = min(result_enemy_temp)

                result_player_temp = []
                result_enemy_temp = []

    def all_eval(self):
        self.eval_alpha()
        self.eval_beta()
        self.eval_gamma()

        self.eval_all()

    def eval_alpha(self):
        """
        이 함수는 유전 알고리즘에서 내가 자체적으로 만든 계산식에 있는 alpha값을 계산하는 것이 목적.
        alpha는 각 패턴에 속해있는 모든 시퀀스들의 체력 차이를 기반으로 계산.
        alpha = sigmoid의 변형된 함수.
        :return:
        """

        for pattern in self.dummy_using_dict:

            for seq in self.dummy_using_dict[pattern]:
                player_x = self.health_difference_player[pattern][seq]['max']
                enemy_x = self.health_difference_enemy[pattern][seq]['max']
                self.eval_storage_player[pattern][seq]['alpha'] = self.function_alpha(player_x)
                self.eval_storage_enemy[pattern][seq]['alpha'] = self.function_alpha(enemy_x)

    @staticmethod
    def function_alpha(input_x):
        e_x = math.exp(input_x * val.EVAL_ALPHA_MODIFIER_X)
        return round(e_x / (e_x + val.EVAL_ALPHA_MODIFIER_Y), 5)

    def eval_beta(self):
        """
        :return:
        """

        difference_spectrum = [x for x in range(-main_val.GAME_HEALTH, main_val.GAME_HEALTH + 1)]

        for pattern in self.dummy_using_dict:
            for seq in self.dummy_using_dict[pattern]:
                temp_sum_player = 0
                temp_sum_enemy = 0
                for i in difference_spectrum:
                    temp_sum_player += ((self.health_difference_player[pattern][seq]['values'].count(i)) /
                                        len(self.health_difference_player[pattern][seq]['values']) *
                                        self.function_alpha(i))
                    temp_sum_enemy += ((self.health_difference_enemy[pattern][seq]['values'].count(i)) /
                                       len(self.health_difference_enemy[pattern][seq]['values']) *
                                       self.function_alpha(i))

                self.eval_storage_player[pattern][seq]['beta'] = round(temp_sum_player, 5)
                self.eval_storage_enemy[pattern][seq]['beta'] = round(temp_sum_enemy, 5)

    def eval_gamma(self):

        for pattern in self.dummy_using_dict:

            temp_pattern_length_player = list()
            temp_pattern_length_enemy = list()

            for seq in self.dummy_using_dict[pattern]:

                temp_pattern_length_player.append(len(self.health_difference_player[pattern][seq]['values']))
                temp_pattern_length_enemy.append(len(self.health_difference_enemy[pattern][seq]['values']))

            for sequence in self.dummy_using_dict[pattern]:

                self.eval_storage_player[pattern][sequence]['gamma'] = self.function_gamma(
                    len(self.health_difference_player[pattern][sequence]['values']),
                    max(temp_pattern_length_player)
                )

                self.eval_storage_enemy[pattern][sequence]['gamma'] = self.function_gamma(
                    len(self.health_difference_enemy[pattern][sequence]['values']),
                    max(temp_pattern_length_enemy)
                )

    @staticmethod
    def function_gamma(input_x, x_max):
        return round(x_max / input_x, 5)

    def eval_all(self):

        for pattern in self.dummy_using_dict:
            for seq in self.dummy_using_dict[pattern]:
                player_a = self.eval_storage_player[pattern][seq]['alpha']
                player_b = self.eval_storage_player[pattern][seq]['beta']
                player_g = self.eval_storage_player[pattern][seq]['gamma']

                enemy_a = self.eval_storage_enemy[pattern][seq]['alpha']
                enemy_b = self.eval_storage_enemy[pattern][seq]['beta']
                enemy_g = self.eval_storage_enemy[pattern][seq]['gamma']

                self.eval_storage_player[pattern][seq]['all'] = self.function_all(player_a, player_b, player_g)
                self.eval_storage_enemy[pattern][seq]['all'] = self.function_all(enemy_a, enemy_b, enemy_g)

    @staticmethod
    def function_all(alpha, beta, gamma):

        return round((alpha + gamma) * beta, 5)

    def extract_parents(self):

        temp_storage_player = copy.deepcopy(self.eval_storage_player)
        temp_storage_enemy = copy.deepcopy(self.eval_storage_enemy)

        temp_player = copy.deepcopy(self.sequence_result_player)
        temp_enemy = copy.deepcopy(self.sequence_result_enemy)

        self.parents_player = self.extract_parents_main_func(val.PARENTS_MODE, val.PARENTS_NUMBER, temp_storage_player,
                                                             temp_player)
        self.parents_enemy = self.extract_parents_main_func(val.PARENTS_MODE, val.PARENTS_NUMBER, temp_storage_enemy,
                                                            temp_enemy)

    def extract_parents_main_func(self, mode, number, sample_eval, sample_result):

        if mode == 'default':
            temp_result = dict()

            for pattern in self.dummy_using_dict:
                temp_result[pattern] = dict()

                temp_seq = list()
                temp_choices = list()

                for seq in self.dummy_using_dict[pattern]:
                    temp_seq.append(sample_eval[pattern][seq]['all'])

                sum_seq = sum(temp_seq)
                semi_seq = [item / sum_seq for item in temp_seq]
                # semi_seq = [1 / len(temp_seq) for i in range(len(temp_seq))]
                seq_spectrum = [i for i in range(len(semi_seq))]

                while len(temp_choices) < number:

                    temp_choices = numpy.random.choice(seq_spectrum, size=number, p=semi_seq)
                    temp_choices = list(set(temp_choices))

                for spec_num in temp_choices:
                    temp_result[pattern]['parent' + str(spec_num + 1)] = sample_result[pattern][
                        'sequence' + str(spec_num + 1)]

            return temp_result

    def create_children(self):
        parents_player = copy.deepcopy(self.parents_player)
        parents_enemy = copy.deepcopy(self.parents_enemy)

        self.children_player = self.create_children_main_func(val.PLAYER_CHILDREN_MODE, parents_player)
        self.children_enemy = self.create_children_main_func(val.CHILDREN_MODE, parents_enemy)

    def create_children_main_func(self, mode, parent, child_num=val.CHILDREN_NUMBER):
        if child_num < val.CHILDREN_NUMBER_ORIGIN:
            child_num = val.CHILDREN_NUMBER_ORIGIN
            # print("input # of children is smaller than iteration number")

        result_children = dict()

        if mode == 'GA Generator 1':

            for pattern in self.dummy_using_dict:

                result_children[pattern] = dict()

                for ith in range(val.CHILDREN_NUMBER_ORIGIN):
                    result_children[pattern]['child' + str(ith + 1)] = dict()
                    result_children[pattern]['child' + str(ith + 1)]['values'] = list()

                    division_number = val.PLAYER_CHILDREN_MODE_DIVISION_NUMBER
                    parent_name = list(parent[pattern].keys())
                    length = 0
                    if len(parent[pattern][parent_name[0]]['values']) != parent[pattern][parent_name[1]]['values']:
                        length = min(len(parent[pattern][parent_name[0]]['values']), len(parent[pattern][parent_name[1]]['values']))

                    temp_index = [i for i in range(length)]
                    division_index = numpy.random.choice(temp_index, division_number, replace=False)
                    division_index = list(set(division_index))

                    for div_count in range(len(division_index) - 1):
                        result_children[pattern]['child' + str(ith + 1)]['values'] \
                            += parent[pattern][parent_name[div_count % 2]]['values'][division_index[div_count]:
                                                                                     division_index[div_count + 1]]
                # front_child = numpy.random.choice(list(parent[pattern].keys()), size=child_num)
                # back_child = numpy.random.choice(list(parent[pattern].keys()), size=child_num)
                #
                # front_children = front_child.tolist()
                # back_children = back_child.tolist()
                #
                # for index in range(child_num):
                #     front_length = int(len(parent[pattern][front_children[index]]['values'])/2)
                #     back_length = int(len(parent[pattern][back_children[index]]['values'])/2)
                #
                #     result_children[pattern]['child' + str(index + 1)] = dict()
                #     result_children[pattern]['child' + str(index + 1)]['values'] = list()
                #     result_children[pattern]['child' + str(index + 1)]['values'] \
                #         = parent[pattern][front_children[index]]['values'][0:front_length] \
                #           + parent[pattern][back_children[index]]['values'][back_length:]

            return result_children

        elif mode == 'default':
            for pattern in self.dummy_using_dict:

                result_children[pattern] = dict()

                front_child = numpy.random.choice(list(parent[pattern].keys()), size=child_num)
                back_child = numpy.random.choice(list(parent[pattern].keys()), size=child_num)

                front_children = front_child.tolist()
                back_children = back_child.tolist()

                for index in range(child_num):
                    front_length = int(len(parent[pattern][front_children[index]]['values'])/2)
                    back_length = int(len(parent[pattern][back_children[index]]['values'])/2)

                    result_children[pattern]['child' + str(index + 1)] = dict()
                    result_children[pattern]['child' + str(index + 1)]['values'] = list()
                    result_children[pattern]['child' + str(index + 1)]['values'] \
                        = parent[pattern][front_children[index]]['values'][0:front_length] \
                          + parent[pattern][back_children[index]]['values'][back_length:]

            return result_children

    def children_to_code_body(self, given_child):

        for pattern in self.dummy_using_dict:
            for child in given_child[pattern]:
                given_child[pattern][child]['code'] = list()
                before_data = given_child[pattern][child]['values'][0]
                for data in given_child[pattern][child]['values']:
                    given_child[pattern][child]['code'].append(self.children_to_code_basic(before_data, data))


    @staticmethod
    def children_to_code_basic(before_data, after_data):
        result = "st"
        if after_data[4] == 'normal':
            result += G_val.SPILT_CHAR
            result += 'normal'

        if after_data[5] == 'multi':
            result += G_val.SPILT_CHAR
            result += 'multi'

        if after_data[6] == 'spread':
            result += G_val.SPILT_CHAR
            result += 'spread'

        if after_data[7] == 'bomb':
            result += G_val.SPILT_CHAR
            result += 'bomb'

        if after_data[8] == 'charge':
            result += G_val.SPILT_CHAR
            result += 'charge'

        if after_data[0:4] == [1, 0, 0, 0]:
            result += G_val.SPILT_CHAR
            result += 'up'

        if after_data[0:4] == [0, 1, 0, 0]:
            result += G_val.SPILT_CHAR
            result += 'down'

        if after_data[0:4] == [0, 0, 1, 0]:
            result += G_val.SPILT_CHAR
            result += 'left'

        if after_data[0:4] == [0, 0, 0, 1]:
            result += G_val.SPILT_CHAR
            result += 'right'

        if after_data[0:4] == [1, 0, 1, 0]:
            result += G_val.SPILT_CHAR
            result += 'up&left'

        if after_data[0:4] == [1, 0, 0, 1]:
            result += G_val.SPILT_CHAR
            result += 'up&right'

        if after_data[0:4] == [0, 1, 1, 0]:
            result += G_val.SPILT_CHAR
            result += 'down&left'

        if after_data[0:4] == [0, 1, 0, 1]:
            result += G_val.SPILT_CHAR
            result += 'down&right'

        if after_data[0:4] == [0, 0, 0, 0]:
            result += G_val.SPILT_CHAR
            result += 'stop'
            # if before_data[0:4] == [1, 0, 0, 0]:
            #
            #     result += G_val.SPILT_CHAR
            #     result += 'up'
            #
            # if before_data[0:4] == [0, 1, 0, 0]:
            #
            #     result += G_val.SPILT_CHAR
            #     result += 'down'
            #
            # if before_data[0:4] == [0, 0, 1, 0]:
            #
            #     result += G_val.SPILT_CHAR
            #     result += 'left'
            #
            # if before_data[0:4] == [0, 0, 0, 1]:
            #
            #     result += G_val.SPILT_CHAR
            #     result += 'right'
            #
            # if before_data[0:4] == [1, 0, 1, 0]:
            #     result += G_val.SPILT_CHAR
            #     result += 'up&left'
            #
            # if before_data[0:4] == [1, 0, 0, 1]:
            #     result += G_val.SPILT_CHAR
            #     result += 'up&right'
            #
            # if before_data[0:4] == [0, 1, 1, 0]:
            #     result += G_val.SPILT_CHAR
            #     result += 'down&left'
            #
            # if before_data[0:4] == [0, 1, 0, 1]:
            #     result += G_val.SPILT_CHAR
            #     result += 'down&right'
        return result

    def children_to_code(self):
        self.children_to_code_body(self.children_player)
        self.children_to_code_body(self.children_enemy)

        self.tester_code()

    def tester_code(self):
        for pattern in self.dummy_using_dict:
            self.sequence_result_enemy[pattern]['code'] = list()
            before_data = self.sequence_result_enemy[pattern]['sequence1']['values'][0]
            for data in self.sequence_result_enemy[pattern]['sequence1']['values']:
                self.sequence_result_enemy[pattern]['code'].append(self.children_to_code_basic(before_data, data))

    def writing_code(self):

        if G_val.ENEMY_GAME_MODE == 'GA tester':
            for pattern in range(len(self.dummy_using_dict.keys())):
                pat = 'pattern' + str(pattern + 1)
                for txt in self.sequence_result_enemy[pat]['code']:
                    self.writing_text('enemy', txt, pattern)

        if G_val.PLAYER_GAME_MODE == 'GA learner':
            for pattern in range(len(self.dummy_using_dict.keys())):
                pat = 'pattern' + str(pattern + 1)
                for child in range(len(self.children_player[pat].keys())):
                    chd = 'child' + str(child + 1)
                    for txt in self.children_player[pat][chd]['code']:
                        self.writing_text('player', txt, pattern, child)

    def writing_text(self, airplane_type, text, number_pattern, number_child=0):
        if airplane_type == 'player':
            path_type = "\Player"
            if G_val.PLAYER_GAME_MODE == 'GA learner':
                path = self.code_path + path_type + '\pattern' + str(number_pattern + 1)
                if not os.path.exists(path):
                    os.makedirs(path)
                temp_child = self.sub_name + str(number_child + 1)

                path += temp_child

                file = open(path + '.txt', 'a')
                if text is None:
                    file.write('Noneee' + "\n")
                else:
                    file.write(text + "\n")

                file.close()

        if airplane_type == 'enemy':
            path_type = "\Enemy"
            if G_val.ENEMY_GAME_MODE == 'GA tester':
                path = self.code_path + path_type
                if not os.path.exists(path):
                    os.makedirs(path)
                path += '\pattern' + str(number_pattern + 1) + '.txt'
                log = open(path, 'a')
                if text is None:
                    log.write("none" + "\n")
                else:
                    log.write(text + "\n")
                log.close()

    def printing_sequence_data(self):
        """
        just printing results.... meaningless in general.
        """
        print()
        # print(self.sequence_result_loser)
        # print(len(self.sequence_result_enemy.keys()))
        # print(self.sequence_result_enemy['pattern2'].keys())
        # for item in self.sequence_result_enemy['pattern1']['sequence1']:
        #     print(item)
        # for pattern in self.sequence_result_enemy:
        #     for seq in self.sequence_result_enemy[pattern]:
        #         print(self.sequence_result_enemy[pattern][seq])
        # for pattern in self.health_difference_enemy:
        #     for seq in self.health_difference_enemy[pattern]:
        #         print(self.health_difference_player[pattern][seq]['max'])
        # for pattern in self.dummy_using_dict:
        #     for seq in self.dummy_using_dict[pattern]:
        #         print("Player All : ", self.eval_storage_player[pattern][seq]['all'])
        #         print("EnemyAll : ", self.eval_storage_enemy[pattern][seq]['all'])
        #         print(self.sequence_result_player[pattern][seq]['loser'])
        #         print("\n")
        #
        # for pattern in self.dummy_using_dict:
        #     print('player', pattern, self.parents_player[pattern].keys())
        #     print('enemy', pattern, self.parents_enemy[pattern].keys())
        # for pattern in self.dummy_using_dict:
        #     for item in self.children_player[pattern]:
        #         print(pattern, "//", item, "//", self.children_player[pattern][item])
        # print(self.children_player['pattern1']['child4'])
        #
        # for pattern in self.children_enemy:
        #     for child in self.children_enemy[pattern]:
        #         print(child, self.children_enemy[pattern][child]['code'].count(''))
        #
        pat = 'pattern2'
        chd = 'child1'
        # for item in self.children_enemy[pat][chd]['code']:
        #     print(item)
        pass
