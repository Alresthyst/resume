import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import lda
import kmean_ver_KWK
import us_sample as us
import pyclustering.cluster.xmeans as XMEAN

ALL_LOCATION = r"""D:\Back up\old_days\특허유니버시아드\노이즈제거\신동헌\us test2.xlsx"""
PURE_LOCATION = r"""D:\Back up\old_days\특허유니버시아드\노이즈제거\신동헌7\us_pure.xlsx"""

ALL_MULTIPLE_VALUE = 0.00001
DOC_MULTIPLE_VALUE = 0.0001
ALL_TOPIC_NUMBER = 1
DOC_TOPIC_NUMBER = 2
WORD_NUMBER = 20
ALL_WORD_NUMBER = 500
PASS_TIMES = 1


SHEET_NUMBER = 0
IDX = 0

XMEAN_LAVUE = 80
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
    'unit', 'least',  'sensor', 'angel', 'determin', 'base',



    'vehicl', 'wheel'
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
                                             given_words_num=ALL_WORD_NUMBER)
Corpus_Excel = lda.Generate_with_Excel_CORPUS(for_extracting_excel_documents,
                                              excel_location=ALL_LOCATION, idx=IDX, sheet_num=SHEET_NUMBER)
LDACLASS_Corpus_Excel = lda.LDA_KWK(Corpus_Excel, given_pass_num=PASS_TIMES, given_topic_num=ALL_TOPIC_NUMBER,
                                    given_words_num=ALL_WORD_NUMBER, given_patent_term=PATENT_TERMS2,
                                    given_all_flag=ALL_MULTIPLE_VALUE)
print("Generating All Doc LDA Processing")
LDACLASS_Corpus_Excel.Generate_LDA()
LDACLASS_Corpus_Excel.Split_Topics_with_Terms()
print("Done")


Class_for_extract_individual_document = lda.LDA_KWK('non-meaning-string', given_pass_num=PASS_TIMES,
                                                    given_topic_num=DOC_TOPIC_NUMBER, given_words_num=WORD_NUMBER)
DOCCLASS_Given_Excel = lda.Generate_with_Excel(Class_for_extract_individual_document, excel_location=ALL_LOCATION,
                                          sheet_num=SHEET_NUMBER, idx=IDX, given_patent_term=PATENT_TERMS2,
                                          given_all_flag=DOC_MULTIPLE_VALUE)
lda.Processing_Entire_Class(DOCCLASS_Given_Excel)

lda.Term_From_LDA_TO_Documents(LDACLASS_Corpus_Excel, DOCCLASS_Given_Excel)

