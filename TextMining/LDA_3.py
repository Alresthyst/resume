# aa.py

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import lda
import kmean_ver_KWK
import us_sample as us
import pyclustering.cluster.xmeans as XMEAN

ALL_LOCATION = r"""D:\Back up\old_days\특허유니버시아드\노이즈제거\신동헌\us test2.xlsx"""
PURE_LOCATION = r"""D:\Back up\old_days\특허유니버시아드\노이즈제거\신동헌7\us_pure.xlsx"""

ALL_MULTIPLE_VALUE = 0.1
ALL_TOPIC_NUMBER = 70
DOC_TOPIC_NUMBER = 4
WORD_NUMBER = 20
PASS_TIMES = 30

SHEET_NUMBER = 0
IDX = 0

XMEAN_LAVUE = 110
KMEAN_L_VALUE = 5
KMEAN_K_VALUE = 20
KMEAN_FIRST_CENTER_NUMBER = 5
KMEAN_MULTIPLIER = 1
KMEAN_PROCESS_COUNT = 10

PATENT_TERMS = ['vehicl', 'control', 'steer', 'wheel', 'system',
                'inform', 'navig', 'guid', 'sensor', 'posit', 'devic'
                , 'includ', 'provid', 'data', 'imag', 'detect', 'signal',
                'receiv', 'determin', 'unit', 'method', 'road', 'use'
                , 'oper', 'one', 'drive', 'first', 'gener', 'base', 'least'
                , 'may', 'can', 'apparatu', 'driver', 'rout', 'angl',
                 'map', 'move', 'travel', 'time', 'second', '1', 'said', 'mean', 'compris', 'wherein',
                'plural', 'locat', 'park', 'display', 'object', 'store', 'traffic', '청구항', 'said']

PATENT_TERMS2 = [
    'compris', 'detect', 'first', 'second', 'mean', 'one', 'said',
    'unit', 'least',  'sensor', 'angel', 'determin', 'base'
]

PATENT_TERMS_CAS_SAMPLE = ['청구항', 'vehicl', 'first', 'second']
PATENT_TERMS_NUMBER = []
for i in range(50):
    PATENT_TERMS_CAS_SAMPLE.append(str(i))
    PATENT_TERMS.append(str(i))
    PATENT_TERMS2.append(str(i))
    PATENT_TERMS_NUMBER.append(str(i))

for_extracting_excel_documents = lda.LDA_KWK('non-meaning_string',
                                             given_pass_num=PASS_TIMES, given_topic_num=ALL_TOPIC_NUMBER,
                                             given_words_num=WORD_NUMBER)
Corpus_Excel = lda.Generate_with_Excel_CORPUS(for_extracting_excel_documents,
                                              excel_location=ALL_LOCATION, idx=IDX, sheet_num=SHEET_NUMBER)
LDACLASS_Corpus_Excel = lda.LDA_KWK(Corpus_Excel, given_pass_num=PASS_TIMES, given_topic_num=ALL_TOPIC_NUMBER,
                                    given_words_num=WORD_NUMBER, given_patent_term=PATENT_TERMS2,
                                    given_all_flag=ALL_MULTIPLE_VALUE)
print("Generating All Doc LDA Processing")
LDACLASS_Corpus_Excel.Generate_LDA()
LDACLASS_Corpus_Excel.Split_Topics_with_Terms()
print("Done")


Class_for_extract_individual_document = lda.LDA_KWK('non-meaning-string', given_pass_num=PASS_TIMES,
                                                    given_topic_num=DOC_TOPIC_NUMBER, given_words_num=WORD_NUMBER)
GWE_Given_Excel = lda.Generate_with_Excel(Class_for_extract_individual_document, excel_location=ALL_LOCATION,
                                          sheet_num=SHEET_NUMBER, idx=IDX, given_patent_term=PATENT_TERMS2,
                                          given_all_flag=ALL_MULTIPLE_VALUE)
lda.Processing_Entire_Class(GWE_Given_Excel)


matrix = lda.Calculate_Cosine_Similarity(LDACLASS_Corpus_Excel, GWE_Given_Excel)

init_center_class = kmean_ver_KWK.ScableKmenas(matrix, g_l=KMEAN_L_VALUE, g_k=KMEAN_K_VALUE,
                                        g_first_center=KMEAN_FIRST_CENTER_NUMBER,
                                        g_l_multipler=KMEAN_MULTIPLIER)

init_center = init_center_class.PosibilityChoosing()


x_mean = XMEAN.xmeans(data=matrix, initial_centers=init_center, kmax=XMEAN_LAVUE)
x_mean.process()
cluster = x_mean.get_clusters()

print(len(cluster))
# f = open("C:\Alrescha\Research\FILE_LO\새파일2.txt", 'w')
for cl in cluster:
    print(cl)
#     for number in cl:
#         data = "%f,%f\n" % (cluster.index(cl), number)
#         f.write(data)
# f.close()





import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D


plt.close('all')  # close all latent plotting windows
fig1 = plt.figure()  # Make a plotting figure

pcs = PCA(n_components=2)
result = pcs.fit(matrix).transform(matrix)


t = [i for i in range(len(cluster))]
count = 0
for cl in cluster:
    x = []
    y = []
    for number in cl:
        x.append(result[number][0])
        y.append(result[number][1])
    pltData = [x, y]
    plt.scatter(pltData[0], pltData[1], s=3)
    count += 1


plt.show()  # show the plot

# for i in range(KMEAN_PROCESS_COUNT):
#
#     kmean = kmean_ver_KWK.ScableKmenas(matrix, g_l=KMEAN_L_VALUE, g_k=KMEAN_K_VALUE,
#                                        g_first_center=KMEAN_FIRST_CENTER_NUMBER,
#                                        g_l_multipler=KMEAN_MULTIPLIER)
#
#     print("\n\nStart Clustering\n K value : ", kmean.k, "/ L value : ", kmean.l, "/ Multipler : ",
#           kmean.multipler, "/ Number of first Center : ", len(kmean.init_center),
#           "/ All Topic number : ", LDACLASS_Corpus_Excel.topic_num, "/ Number of terms in All : ",
#           LDACLASS_Corpus_Excel.words_num, "/ Term Pass count : ", LDACLASS_Corpus_Excel.pass_num,
#           " / Individual Topic Number : ", DOC_TOPIC_NUMBER, " / Individual Terms number : ",
#           WORD_NUMBER, " / All multipler value : ", ALL_MULTIPLE_VALUE, "\n\n")
#
#     resultt = kmean.Final_Result()
#
#     temp = list(resultt[1])
#     result_array = [];
#
#     for center_number in range(kmean.k):
#         result_center_array = []
#         for doc_index in range(len(temp)):
#             if (temp[doc_index] == center_number):
#                 result_center_array.append(doc_index + 1)
#         result_array.append(result_center_array)
#         print("Center Number : ", center_number, "Doc list : ", result_array[center_number])
#     print("\n\nCounting Number : ", i + 1, "\n\n\n\n")
