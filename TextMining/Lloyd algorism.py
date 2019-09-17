import random
import kmean_ver_KWK_1 as kmean
import numpy

test_matrix = numpy.array([[random.random() for i in range(10)]for row in range(500)])

temp_result = kmean.ScableKmenas(test_matrix, g_l=3, g_k=15, g_first_center=5)
result = temp_result.Final_Result()
print(result)