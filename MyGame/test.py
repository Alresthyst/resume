import random
import math
from keras.layers import Dense, Activation
from keras import Sequential

#
# def vector_line_cal(b_pos, b_vector, t_pos):
#     determinant_vector = [b_pos[0] - t_pos[0], b_pos[1] - t_pos[1]]
#     len_det = math.sqrt(determinant_vector[0]**2 + determinant_vector[1]**2)
#
#     len_b = math.sqrt(b_vector[0]**2 + b_vector[1]**2)
#     mod_det = [determinant_vector[0]/len_det, determinant_vector[1]/len_det]
#     mod_b = [b_vector[0] / len_b, b_vector[1] / len_b]
#
#     if mod_det[0] != mod_b[0] and mod_det[1] != mod_b[1]:
#         return 0
#     else:
#         return 1
#
#
# temp_b = [[random.randrange(-500, 500), random.randrange(-500, 500)] for i in range(100)]
# temp_target_pos = [random.randrange(-500, 500), random.randrange(-500, 500)]
# temp_b_v = [[random.randrange(-10, 10), random.randrange(-10, 10)] for i in range(len(temp_b))]
#
# for idx in range(len(temp_b)):
#     print(vector_line_cal(temp_b[idx], temp_b_v[idx], temp_target_pos))

model = Sequential()
model.add(Dense(units=64, input_dim=20*20, activation='custom'))
