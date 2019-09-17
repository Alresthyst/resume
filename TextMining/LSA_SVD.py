import numpy as np
import math

# 인터넷 예제 실습
in_matrix = [
    [1, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1]
]

# test_matrix = [
#     [1,1],
#     [1,1],
#     [1,1],
#     [1,1],
# ]
#
#
# # print(len(test_matrix))


in_np_matrix = np.array(in_matrix).astype(np.float64)

# print(in_np_matrix) # ok

U, s, V = np.linalg.svd(in_np_matrix, full_matrices=False)

after_s =[[0 for col in range(5)] for row in range(5)]


def make_s(before_matrix, after_matrix):
    count = 0
    for i in range(len(before_matrix)):

        if (count == i):
            after_matrix[count][i] = before_matrix[i]
        else:
            after_matrix[count][i] = 0
        count += 1
    return after_matrix


# print(U, "\n", make_s(s,after_s), "\n", V)
# a= U.dot(make_s(s, after_s))
# print(a.dot(V))


# print(make_s(s,after_s)) #ok


# final_matrix = LSA_SVD_r_RANK(in_np_matrix, 2,'n')

# print(final_matrix) # ok


def dotmat(matrix1, matrix2):
    t = 0
    for i in range(len(matrix1)):
        t = t + matrix1[i]*matrix2[i]
        # print(matrix1[i], matrix2[i])
    return t


def absbody(matrix):
    temp = 0
    for i in range(len(matrix)):
        temp = temp + (matrix[i] * matrix[i])
    return math.sqrt(temp)

def cosine_sim(mat1, mat2):
    return dotmat(mat1, mat2) / (absbody(mat1) * absbody(mat2))



def LSA_SVD_r_RANK(matrix, r, TypeChar):
    temp_matrix = np.array(matrix).astype(np.float64)
    tU, b_ts, tV = np.linalg.svd(temp_matrix, full_matrices=False)
    a_ts = [[0 for col in range(len(b_ts))] for row in range(len(b_ts))]
    ts = make_s(b_ts,a_ts)



    # print(tU, "\n", ts, "\n", tV)
    # ab = tU.dot(ts)
    # print(ab.dot(tV))

    fU = [[0 for col in range(r)] for row in range(len(tU))]
    fU = np.array(fU).astype(np.float64)
    fs = [[0 for col in range(r)] for row in range(r)]
    fs = np.array(fs).astype(np.float64)
    fV = [[0 for col in range(len(tV.T))] for row in range(r)]
    fV = np.array(fV).astype(np.float64)



    for i in range(r):
        for j in range(len(tU)):
            # print(j,i)
            fU[j][i] = tU[j][i]


    for i in range(r):
        for j in range(r):
            # print(j,i)
            fs[j][i] = ts[j][i]


    for i in range(len(tV.T)):
        for j in range(r):
            # print(j,i)
            fV[j][i] = tV[j][i]




    # print(fU, "\n\n", fs, "\n\n", fV, "\n\n done ") #ok

    if (TypeChar == 'm' or TypeChar == 'M'):
        return fU.dot(fs)
    elif (TypeChar == 'n' or TypeChar == 'N'):
        return (fs.dot(fV)).T
    else:
        temp_matrix2 = fU.dot(fs)
        result_matrix = temp_matrix2.dot(fV)
        return result_matrix





# print(final_matrix.T[0], final_matrix.T[1])
# print(dotmat(final_matrix.T[0], final_matrix.T[1]))
# print(absbody(final_matrix.T[0]))
# print(cosine_sim(final_matrix.T[0], final_matrix.T[2]))



