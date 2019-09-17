
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


import lda
import kmean_ver_KWK
import math
import pyclustering.cluster.xmeans as XMEAN
from textblob import TextBlob as tb


ALL_LOCATION = r"""C:\Users\DB_LAB_1\Desktop\특허\특허전략유니버시아드\신동헌\us test2.xlsx"""
PURE_LOCATION = r"""C:\Users\DB_LAB_1\Desktop\특허\특허전략유니버시아드\신동헌\us_pure.xlsx"""

ALL_MULTIPLE_VALUE = 0.001
ALL_TOPIC_NUMBER = 3
DOC_TOPIC_NUMBER = 7
WORD_NUMBER = 10
PASS_TIMES = 1

SHEET_NUMBER = 0
IDX = 0

XMEAN_LAVUE = 110
KMEAN_L_VALUE = 2
KMEAN_K_VALUE = 10
KMEAN_FIRST_CENTER_NUMBER = 5
KMEAN_MULTIPLIER = 1
KMEAN_PROCESS_COUNT = 10



PATENT_TERMS2 = [
    'compris', 'detect', 'first', 'second', 'mean', 'one', 'said',
    'unit', 'least',  'sensor', 'angel', 'determin', 'base',



    'vehicl', 'wheel'
]

PATENT_TERMS_CAS_SAMPLE = ['청구항', 'vehicl', 'first', 'second']
PATENT_TERMS_NUMBER = []
for i in range(50):
    PATENT_TERMS_CAS_SAMPLE.append(str(i))
    PATENT_TERMS2.append(str(i))
    PATENT_TERMS_NUMBER.append(str(i))



def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def Generate_with_Excel(ldaclass, excel_location, sheet_num, idx):
    '''

    필독 ! : 이 파일 테스트시 엑셀의 맨 첫번 째 행이 의미 없는 행이라서 첫 행을 빼고 가져옵니다. 수정하실려면
             indexing 변수를 변경해주세요!
             또한 안타깝게도 여백이 있는 것을 제거 하지는 못했으니 여백 제거도 신경써주세요!
    :param ldaclass: LDA_KWK class 입니다. 초기 값중에 하나인 given_doc은 아무 문자나 넣어도 되지만, 나머지 값들은 원하는 값으로 넣어주세요!!!
    :param excel_location: 변환 하고자 하는 엑셀의 위치 입니다. r{내용} 형식으로 넣어주시면 깔끔 !
    :param sheet_num: 가져온 엑셀의 시트 번호입니당
    :param idx: 엑셀 시트에서 가져올 열 변호 입니다!
    :return: 각 행의 문서들을 배이스로한 LDA_KWK 클래스 입니당
    '''
    indexing = 1 # 첫 행 막기 위함
    # 엑셀에서 파일 읽기 시작!
    print("Start extracting document from given excel - document")

    temp_doc = ldaclass.Extract_Excel(excel_location, sheet_num, idx)
    result = []
    for i in temp_doc:
        print("asd ", i)
        result.append(tb(i))

    print("End extracting document from given excel - document")

    return result

def t (GWE):
    result = []
    for items in GWE:
        result.append(tb(" ".join(items.texts[0])))
    return result


for_extracting_excel_documents = lda.LDA_KWK('non-meaning_string',
                                             given_pass_num=PASS_TIMES, given_topic_num=ALL_TOPIC_NUMBER,
                                             given_words_num=WORD_NUMBER)
GWE = lda.Generate_with_Excel(for_extracting_excel_documents,
                              excel_location=ALL_LOCATION, idx=IDX, sheet_num=SHEET_NUMBER,
                              given_patent_term=PATENT_TERMS2,
                              given_all_flag=ALL_MULTIPLE_VALUE)

lda.Processing_Entire_Class(GWE)

bloblist = t(GWE)

# print(bloblist)

temp = []

temp_stor = []

print("starting tf idf")
for i, blob in enumerate(bloblist):
    # print("Top words in document {}".format(i + 1))
    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    temp.append(sorted(scores.items(), key=lambda x: x[1], reverse=True))
    # for word, score in sorted_words[:30]:
    #     print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

# print(temp[3])
# print("\n\n\n\n", temp_stor[0])
#
print("End of  tf idf")
print("start gathering terms")
lda.tf_idf_terms_gather(GWE, temp)
print("end gathering terms")
#
# print(GWE[3].result_terms)
# print(GWE[3].result_weight)

result_matrix = lda.Create_Matrix(GWE)

# print("length of result_matrix :", len(result_matrix.T))
# print("length of GWE : ", len(GWE))
# print("length of col (rematrix)", len(result_matrix.T[1]))


init_center_class = kmean_ver_KWK.ScableKmenas(result_matrix, g_l=KMEAN_L_VALUE, g_k=KMEAN_K_VALUE,
                                        g_first_center=KMEAN_FIRST_CENTER_NUMBER,
                                        g_l_multipler=KMEAN_MULTIPLIER)

init_center = init_center_class.PosibilityChoosing()

print("Start X-Means")
x_mean = XMEAN.xmeans(data=result_matrix, initial_centers=init_center, kmax=XMEAN_LAVUE)
x_mean.process()
cluster = x_mean.get_clusters()

print("End X-Means")

print(len(cluster))

for cl in cluster:
    print(cl)


f = open("C:\Alrescha\Research\FILE_LO\새파일.txt", 'a')
f.write(','.join(str(x) for x in range(len(result_matrix.T))))
f.write("\n")

for itemss in result_matrix:
    print(len(itemss))
    strasd = ','.join(str(x) for x in itemss)
    f.write(strasd + "\n")
f.close()

f = open("C:\Alrescha\Research\FILE_LO\새파일3.txt", 'a')
strasd = ','.join(str(x) for x in lda.Gathering_Terms(GWE))
f.write(strasd + "\n")
f.close()

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt1
import random
from mpl_toolkits.mplot3d import Axes3D

#
# plt.close('all')  # close all latent plotting windows
# fig1 = plt.figure()  # Make a plotting figure
#
# pcs = PCA(n_components=2)
# result = pcs.fit(result).transform(result)
#
#
# t = [i for i in range(len(cluster))]
# count = 0
# for cl in cluster:
#     x = []
#     y = []
#     for number in cl:
#         x.append(result[number][0])
#         y.append(result[number][1])
#     pltData = [x, y]
#     plt.scatter(pltData[0], pltData[1], s=3)
#     count += 1
#
#
# plt.show()  # show the plot

plt1.close('all')  # close all latent plotting windows
fig1 = plt1.figure()  # Make a plotting figure
ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object

pcs = PCA(n_components=3)
result = pcs.fit(result_matrix).transform(result_matrix)


t = [i for i in range(len(cluster))]
count = 0
for cl in cluster:
    x = []
    y = []
    z = []
    for number in cl:
        x.append(result[number][0])
        y.append(result[number][1])
        z.append(result[number][2])
    plt1Data = [x, y, z]
    ax.scatter(plt1Data[0], plt1Data[1], plt1Data[2], s=3)
    count += 1


plt1.show()  # show the plot


