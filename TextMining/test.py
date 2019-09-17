import random
import pyclustering.cluster.xmeans as xmean
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import random
from mpl_toolkits.mplot3d import Axes3D


a = [1, 2]
b = [1, 2, 3]
c = [2, 3, 4]
d = []

d += b[0:2]
d += c[0:2]


print(d)

e = [0, 0, 1, 2, 3]
print(e.remove(0))
print(e)

print(len(range(1,4)))

f = ['a', 'b']
g = ['c', 'd']
h = ['z','x', 'e', 'f', 'g', 'h', 'i']
h.sort()
print(h)
print(" ".join(f))

asdasd = [[random.random() for i in range(10)] for j in range(100)]

# for asd in asdasd:
#     print(asd)


tt = [
    [0,0,0,1],
    [0,0,0,2],
    [0,1,0,0],
    [0,0,1,0],
    [6,6,6,6],
    [6,6,6,7],
    [6,7,6,6],
    [3,3,3,3],
    [3,3,3,4],
]

pcs = PCA(n_components=2)
X = pcs.fit(tt).transform(tt)

plt.close('all')  # close all latent plotting windows
fig1 = plt.figure()  # Make a plotting figure

x=[]
y=[]
for item in X:
   x.append(item[0])
   y.append(item[1])

pltData = [x, y]
plt.scatter(pltData[0], pltData[1], s=5)


plt.show()  # show the plot



test_x = xmean.xmeans(data=tt, initial_centers=[tt[0], tt[1]], kmax=20)

test_x.process()

cluster = test_x.get_clusters()


for cl in cluster:
    print(cl)






import lda
import kmean_ver_KWK
import us_sample as us
import pyclustering.cluster.xmeans as XMEAN

ALL_LOCATION = r"""C:\Users\DB_LAB_1\Desktop\특허\특허전략유니버시아드\신동헌\us test.xlsx"""
PURE_LOCATION = r"""C:\Users\DB_LAB_1\Desktop\특허\특허전략유니버시아드\신동헌\us_pure.xlsx"""

ALL_MULTIPLE_VALUE = 0.2
ALL_TOPIC_NUMBER = 1
DOC_TOPIC_NUMBER = 7
WORD_NUMBER = 20
PASS_TIMES = 50

SHEET_NUMBER = 0
IDX = 0

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
    'compris', 'control', 'data', 'detect', 'first', 'second', 'imag', 'mean', 'one', 'said', 'system',
    'vehicl', 'wherein', 'unit', 'least', 'devic', 'sensor', 'angel', 'determin', 'base'
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
                                              excel_location=PURE_LOCATION, idx=IDX, sheet_num=SHEET_NUMBER)
LDACLASS_Corpus_Excel = lda.LDA_KWK(Corpus_Excel, given_pass_num=PASS_TIMES, given_topic_num=ALL_TOPIC_NUMBER,
                                    given_words_num=WORD_NUMBER, given_patent_term=PATENT_TERMS_NUMBER,
                                    given_all_flag=ALL_MULTIPLE_VALUE)
print("Generating All Doc LDA Processing")
LDACLASS_Corpus_Excel.Generate_LDA()
LDACLASS_Corpus_Excel.Split_Topics_with_Terms()
print("Done")

print(LDACLASS_Corpus_Excel.doc)
for i in LDACLASS_Corpus_Excel.result_lda:
    print(i[1])