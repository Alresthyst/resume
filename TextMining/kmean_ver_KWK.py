import sklearn.cluster.k_means_ as kmean
import sklearn.utils.extmath as extmath
import numpy as np
import random as r
import math
import numpy.random as ran
import numpy

# test_matrix = np.array([[r.random() for i in range(10)]for row in range(500)])

class ScableKmenas:
    def __init__(self, g_matrix, g_l, g_k, g_first_center, g_l_multipler):
        '''

        :param g_matrix: Term Matrix 입니당

        :param g_l: Scalable K mean++ 에서 사용하는 l 값 입니다. initializing 시에 각 횟수 마다 뽑을 Center 후보들의 갯수를 의미합니당

        :param g_k: 최종 Center의 갯수를 의미합니당!

        :param g_first_center: 초기 Center의 갯수를 지정합니다!

        :param g_l_multipler: 초기 Center 갯수에서 얼마나 많은 최종 Center들을 뽑을 것인지를 결정 하는 값입니다. 이 값이 일정 수준을 넘어 가면
                               계산량은 적어지지만, 잘못 하면 Center의 갯수가 k개 보다 작아져서 K mean 실행이 불가 하며
                               상대적으로 작은 값을 뽑으면 보다 좋은 Center 를 얻을 수 있으나, 계산량이 늘어나서 시간이 오래 걸리게 됩니다. !ㅅ!
                               예시 : k = 350, l = 0.5
                               중간 결과 : 696개의 Center 선택
                               K(350)까지 줄이는데 걸린 시간 : 대략 10분 30초
        '''
        self.matrix = g_matrix
        self.l = g_l
        self.k = g_k
        self.multipler = g_l_multipler;
        self.norm = kmean.row_norms(self.matrix, True)
        self.fc = g_first_center
        self.init_center, self.init_center_index = self.PickFirstCenter()
        self.process_center = self.init_center
        self.process_center_index = self.init_center_index
        self.center_distance = 0


    def PickFirstCenter(self):
        temp_matrix = self.matrix.tolist()
        temp = [temp_matrix.pop(r.randint(0, len(temp_matrix) - 1)) for pos in range(self.fc)]
        return temp, [self.matrix.tolist().index(temp[index]) for index in range(len(temp))]

    def SquaredDistance(self, center=None):
        if (center != None):
            temp_center = center
        else:
            temp_center = self.process_center

        temp_result = list(kmean.pairwise_distances_argmin_min(self.matrix, temp_center))  # reshape(1, -1) = 데이터가 1개 일때 이렇게 바꿔주래..
        temp_result[1] = temp_result[1]**2
        temp_result.append(sum(temp_result[1]))
        return temp_result

    def PosibilityChoosing_Process(self):
        temp_distance = self.SquaredDistance(center=self.process_center)
        temp_self_matrix = list(self.matrix)

        temp_matrix = (self.l * temp_distance[1] / temp_distance[2])
        temp_matrix = temp_matrix/sum(temp_matrix)

        temp_result = [numpy.random.choice(numpy.arange(0, len(temp_self_matrix)), p=temp_matrix) for count in range(self.l)]

        for count in range(len(temp_result)):
            self.process_center_index.append(temp_result[count])
        self.process_center_index = list(set(self.process_center_index))

        self.process_center = [self.matrix[i] for i in self.process_center_index]
        return 0

    def PosibilityChoosing(self):
        # round(math.log(self.SquaredDistance(center=self.init_center)[2]))
        for i in range(round(self.k/(self.multipler*self.l))):
            self.PosibilityChoosing_Process()
        print("Finishing Posibility Choosing :", len(self.process_center))
        return self.process_center

    def Calculate_Distance_Processed_Center(self):
        temp_center = self.process_center
        temp_stroage = []
        for pos in range(len(temp_center)):
            temp_under_storage = []
            for count in range(len(temp_center)):
                temp_under_storage.append(numpy.linalg.norm(temp_center[pos] - temp_center[count]))
            temp_stroage.append(temp_under_storage)
        return temp_stroage

    def Storage_Index_Distance_Processed_Center(self):
        temp_CDPC = list(self.Calculate_Distance_Processed_Center())
        temp_storage = []
        for pos in range(len(temp_CDPC)):
            temp_CDPC[pos][pos] = max(temp_CDPC[pos])
            # printing middle level of algorithm
            # print("min value is :", min(temp_CDPC[pos]), "position is : ", pos)
            temp_storage.append([pos, temp_CDPC[pos].index(min(temp_CDPC[pos])), min(temp_CDPC[pos])])
        return temp_storage

    def Reduce_Processed_Center_to_K_Cluster(self):
        k = self.k
        temp_distance = []
        temp_set = []

        while(k < len(self.process_center)):
            print(len(self.process_center))
            temp_SIDPC = self.Storage_Index_Distance_Processed_Center()
            for i in range(len(temp_SIDPC)):
                temp_distance.append(temp_SIDPC[i][2])
            # Check Result temp_distance
            # print(min(temp_distance))
            # print("minus:", len(self.process_center) - len(temp_set))
            temp_min = min(temp_distance)
            for count in range(len(temp_SIDPC)):
                if (temp_SIDPC[count][2] == temp_min):
                    temp_distance =[]
                    del self.process_center[temp_SIDPC[count][1]]
                    break





    def Scablekmeans_ProcessingCenter(self):
        print("Starting Choosing")
        self.PosibilityChoosing()
        print("Reducing Start")
        self.Reduce_Processed_Center_to_K_Cluster()
        print("Reducing Done\n\n");
        return 0

    def Final_Result(self):
        self.Scablekmeans_ProcessingCenter()
        try:
            return kmean.k_means(self.matrix, self.k, init=numpy.array(self.process_center), n_init=1)
        except:
            print("최종 계산된 Center의 갯수가 K 보다 작습니다...", "\n K 값 : ", self.k, " /  Center 갯수 : ", len(self.process_center))


    # def Find_Distance_For_Complete_Centers(self):
    #     if (len(self.process_center_index) <= self.fc):
    #         self.PosibilityChoosing()
    #     else:
    #         pass
    #     main_centers = self.process_center
    #     temp = [[0 for i in range(len(self.process_center_index))] for row in range(len(self.process_center_index))]
    #     for pos in range(len(self.process_center_index)):
    #         for count in range(len(self.process_center_index)):
    #             if (pos == count):
    #                 pass
    #             else:
    #                 temp[pos][count] = numpy.linalg.norm(main_centers[pos] - main_centers[count])
    #
    #     temp2 = [0 for i in range(len(self.process_center_index))]
    #     self.center_distance = [0 for i in range(len(self.process_center_index))]
    #     for pos in range(len(self.process_center_index)):
    #         temp_cal = temp
    #         temp_cal[pos].remove(0)
    #         temp2[pos] = min(temp_cal[pos])
    #         self.center_distance[pos] = temp_cal[pos].index(min(temp_cal[pos]))
    #     return temp2
    #
    #
    # def WeightingCenters(self):
    #     print(self.Find_Distance_For_Complete_Centers())
    #     temp_center_distance_index = self.center_distance
    #     temp_center_distance = self.Find_Distance_For_Complete_Centers()
    #     print(len(temp_center_distance), len(list(set(temp_center_distance))))
    #     count = 0
    #     temp_storage_groups = []
    #     for pos in range(len(temp_center_distance_index)):
    #         temp_groups = []
    #         if(temp_center_distance[pos] == temp_center_distance[count]):
    #             temp_groups.append(temp_center_distance_index[pos])
    #         temp_groups.append(temp_center_distance_index[count])
    #         count += 1
    #         temp_storage_groups.append(temp_groups)
    #     print(temp_storage_groups)
    #     # temp_dis, temp_index = self.Find_Distance_For_Complete_Centers(), list(self.center_distance)
    #     # temp_dis2 = temp_dis
    #     # temp_dis2.sort()
    #     # temp_del = [0 for i in range(0, len(temp_dis2)-self.k, 1)]
    #     # count = 0
    #     # for index in range(0, len(temp_dis2) - self.k, 1):
    #     #     if (temp_dis2[len(temp_dis2) - self.k] >= temp_dis[index]):
    #     #         temp_del[count] = temp_index[index]
    #     #         count += 1
    #     # for count in sorted(temp_del, reverse=True):
    #     #     del self.process_center_index[count]
    #     #     del self.process_center[count]
    #     # return temp_del





# test_kmean = ScableKmenas(test_matrix, g_l=3, g_k=15, g_first_center=4)
# result = test_kmean.Final_Result()




# # print(len(test_kmean.process_center))
# print(result)
# print(len(test_kmean.process_center), len(result[0]))
# print(test_kmean.Find_Distance_For_Complete_Centers())
# print(test_kmean.WeightingCenters())
# print(len(test_kmean.process_center_index), test_kmean.PosibilityChoosing())

# print(test_kmean.PosibilityChoosing())
# print(test_kmean.init_center)
# print(round(math.log(test_kmean.SquaredDistance()[2], 10)))
# print(kmean.pairwise_distances_argmin_min(test_matrix, test_kmean.PickFirstCenter()))
#
# test_center = kmean._init_centroids(test_matrix, 3, init= 'k-means++')
# test_norm = kmean.row_norms(test_matrix, True)
#
# result = kmean._labels_inertia(X=test_matrix, x_squared_norms=test_norm, centers=test_center)
#
# print(result[1]**2)
# print(test_center)




