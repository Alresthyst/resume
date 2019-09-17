# https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

from xlrd import open_workbook
import numpy
import LSA_SVD

class LDA_KWK:
    def __init__(self, given_doc, given_topic_num, given_words_num, given_pass_num, given_patent_term = None
                 , given_all_flag = None):
        self.doc = given_doc
        self.topic_num = given_topic_num
        self.words_num = given_words_num
        self.pass_num = given_pass_num
        self.tokenizer = RegexpTokenizer(r'\w+')
        # create English stop words list
        self.en_stop = get_stop_words('en')
        # Create p_stemmer of class PorterStemmer
        self.p_stemmer = PorterStemmer()
        # list for tokenized documents in loop
        self.texts = []
        self.stemmed_tokens = []
        self.stopped_tokens = []
        self.dictionary = dict
        self.corpus = []
        self.ldamodel = 0
        # Save result
        self.result_weight = []
        self.result_terms = []
        self.result_topic_number = []
        self.result_lda = []
        self.patent_term_flag = 0
        if (given_patent_term is not None):
            self.patent_term_flag = 1
            self.patent_term = given_patent_term
        self.all_flag = given_all_flag

    # loop through document list
    def CleanDoc(self):
        # clean and tokenize document string
        raw = self.doc.lower()
        tokens = self.tokenizer.tokenize(raw)

        # remove stop words from tokens
        self.stopped_tokens = [i for i in tokens if not i in self.en_stop]

        # stem tokens
        self.stemmed_tokens = [self.p_stemmer.stem(i) for i in self.stopped_tokens]

        # 특허용 코드 - 불필요한 단어 추가 제거
        if(self.patent_term_flag == 1):
            for terms in self.patent_term:
                if (self.stemmed_tokens.count(terms) == 0):
                    pass
                    # term이 진짜 있는지 없는지 볼려고 테스트 할때 쓴닷
                    # print("We dont have term : ", terms)
                else:
                    for term_count in range(self.stemmed_tokens.count(terms)):
                        self.stemmed_tokens.remove(terms)
        # add tokens to list
        self.texts.append(self.stemmed_tokens)

        # turn our tokenized documents into a id <-> term dictionary
        self.dictionary = corpora.Dictionary(self.texts)

        # convert tokenized documents into a document-term matrix
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]


        # 주의 ! 특허 전용!
        if (self.all_flag is not None):
            # print("Start deleting non-necessery term by frequency")
            temp_count = len(self.stemmed_tokens) * self.all_flag
            for cor in self.corpus[0]:
                if (cor[1] > temp_count):
                    # print(self.dictionary[cor[0]], cor[1])
                    self.corpus[0].remove(cor)

    # generate LDA model
    def Generate_LDA(self):
        self.CleanDoc()
        self.ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=self.topic_num, id2word=self.dictionary,
                                                        passes=self.pass_num)

    def SplitTopics(self):
        #return [ [v,k] for k, v in self.show_topic(topicno, topn)]
        #gensim.ldamodel => print_topic
        for topicnum in range(self.topic_num):
            temp_result = self.ldamodel.print_topic(topicno=topicnum, topn=self.words_num).split("+")
            for pos in range(len(temp_result)):
                self.result_weight.append(temp_result[pos][0])
                self.result_terms.append(temp_result[pos][1])
                self.result_topic_number.append(topicnum)
        return 0


    def Split_Topics_with_Terms(self):
        for topcnum in range(self.topic_num):
            self.result_topic_number.append(topcnum)
            temp_result = self.ldamodel.print_topic(topicno=topcnum, topn=self.words_num).split("+")
            for pos in range(len(temp_result)):
                self.result_weight.append(temp_result[pos][0])
                self.result_terms.append(temp_result[pos][1])
            self.result_lda.append([topcnum, self.result_terms, self.result_weight])
            self.result_weight = []
            self.result_terms = []
        # printing result
        # for i in range(len(self.result_lda)):
        #     print(self.result_lda[i], "\n")
        return 0

    def LDA_TotalProcess(self):
        self.Generate_LDA()
        self.Split_Topics_with_Terms()
        return 0

    def PrintResult(self):
        print(len(self.result_weight), self.result_weight, "\n", self.result_terms)

    def excel_converter(self, workbook, sheet_num, idx):
        document = workbook.sheet_by_index(sheet_num)

        # row length:
        num_rows = document.nrows

        row_val = []

        for val in range(num_rows):
            # append string to row_val
            # print(document.row_values(val)) -> 출력 결과 확인용!
            row_val.append(document.row_values(val)[idx])
        return row_val

    def Extract_Excel(self, given_location, given_sheet_num, given_idx):
        return self.excel_converter(open_workbook(given_location), given_sheet_num, given_idx)


def Generate_with_Excel(ldaclass, excel_location, sheet_num, idx, given_patent_term = None, given_all_flag = None):
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

    if (given_patent_term is not None):
        patent_term = given_patent_term
    else:
        patent_term = None

    if (given_all_flag is not None):
        all_flag = given_all_flag
    else:
        all_flag = None

    temp_doc = ldaclass.Extract_Excel(excel_location, sheet_num, idx)
    result = []
    for docnum in range(len(temp_doc)):
        result.append(LDA_KWK(given_doc=temp_doc[docnum],
                              given_topic_num=ldaclass.topic_num,
                              given_words_num=ldaclass.words_num,
                              given_pass_num=ldaclass.pass_num,
                              given_patent_term=patent_term,
                              given_all_flag=all_flag))

    #엑실 읽기 끝!
    print("End extracting document from given excel - document")

    return result

def Generate_with_Excel_CORPUS(ldaclass, excel_location, sheet_num, idx):
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
    print("Start extracting all document from given excel")


    temp_doc = ldaclass.Extract_Excel(excel_location, sheet_num, idx)
    result = ''
    for docnum in range(len(temp_doc)):
        # print(temp_doc[docnum])
        result += temp_doc[docnum]

    #엑실 읽기 끝!
    print("End extracting all document from given excel")
    return result


def Processing_Entire_Class(GWE):
    '''

    :param GWE: Generate_with_Excel 함수의 리턴 값 입니다!
    :return: LDA 프로세스를 마친 LDA_KWK 클래스들을 리턴 !
    '''
    print("Processing making LDA_KWK Class")
    for cls in GWE:
        cls.LDA_TotalProcess()
    print("Making LDA_KWK Class is done")
    return GWE

def Gathering_Terms(PEC):
    '''

    :param PEC: Processing_Entire_Class 리턴 값입니당 !ㅅ!
    :return: LDA로 나온 모든 Term(단어)들을 리턴 합니당 !ㅅ!
    '''
    temp = []
    for index in range(len(PEC)):
        temp += PEC[index].result_terms

    temp = list(set(temp))
    return temp


def tf_idf_terms_gather(GWE, result_set):
    temp = []

    for i ,items2 in enumerate(result_set):
        # print(i)
        GWE[i].result_terms = []
        GWE[i].result_weight = []
        for terms in items2:
            GWE[i].result_terms.append(terms[0])
            GWE[i].result_weight.append(terms[1])
    return 0


def Create_Matrix(PEC):
    '''

    :param PEC: Processing_Entire_Class 리턴 값입니당 !ㅅ!
    :return: LDA 기반의 n-차원 공간입니당!
    '''


    print("Start Creating term Matrix")

    terms = Gathering_Terms(PEC)

    print("Number of terms :", len(terms))

    result =[[0 for i in range(len(terms))] for j in range(len(PEC))]
    for docunum in range(len(PEC)):
        temp = [0 for i in range(len(terms))]
        for termnum in range(len(terms)):
            for count in range(len(PEC[docunum].result_terms)):
                if (PEC[docunum].result_terms[count] == terms[termnum]):
                    temp[termnum] = PEC[docunum].result_weight[count]
                result[docunum] = temp

    print("End Creating term Matrix")

    return numpy.array(result)


def Calculate_Cosine_Similarity(All_KWK_CLASS, DOC_KWK_CLASS):
    print("Start Making Cosine Sim matrix")
    all_result_lda = All_KWK_CLASS.result_lda
    All_topic_num = All_KWK_CLASS.topic_num
    Words_num = All_KWK_CLASS.words_num
    temp_cos_sim_result2 = []
    for i in range(len(all_result_lda)):
        all_result_lda[i][1].sort()
        print("All ","Topic Number : ", i, "Terms : ", all_result_lda[i][1])
    Cosine_similarity_result = []


    for KWK_CLASS_NUM in range(len(DOC_KWK_CLASS)):
        doc_result_lda = DOC_KWK_CLASS[KWK_CLASS_NUM].result_lda
        Doc_topic_num = DOC_KWK_CLASS[KWK_CLASS_NUM].topic_num

        print("Doc N: ", KWK_CLASS_NUM, "Doc : ", doc_result_lda)

        for all_topic_number in range(All_topic_num):
            temp_cos_sim_result = []
            for doc_topic_number in range(Doc_topic_num):
                terms1 = ",".join(all_result_lda[all_topic_number][1])
                terms2 = ",".join(doc_result_lda[doc_topic_number][1])

                terms = terms1 +","+ terms2
                terms = terms.split(",")
                terms = list(set(terms))

                cosine_matrix_all = [0 for i in range(len(terms))]
                cosine_matrix_doc = [0 for i in range(len(terms))]
                for term in terms:
                    if(all_result_lda[all_topic_number][1].count(term) > 0):
                        cosine_matrix_all[terms.index(term)] = \
                        all_result_lda[all_topic_number][2][all_result_lda[all_topic_number][1].index(term)]
                    if(doc_result_lda[doc_topic_number][1].count(term) > 0):
                        cosine_matrix_doc[terms.index(term)] = \
                        doc_result_lda[doc_topic_number][2][doc_result_lda[doc_topic_number][1].index(term)]

                # print(len(terms), cosine_matrix_doc.count(0), cosine_matrix_all.count(0))
                terms = ''

                temp_cos_sim_result.append(LSA_SVD.cosine_sim(cosine_matrix_all, cosine_matrix_doc))
            temp_cos_sim_result2.append([all_topic_number, temp_cos_sim_result.index(max(temp_cos_sim_result)), max(temp_cos_sim_result)])

            # print(cosine_matrix_all, cosine_matrix_doc)
            # print("all topic number :", all_topic_number, "doc number :", KWK_CLASS_NUM, "  temp cos:", temp_cos_sim_result, "   cos result : ", Cosine_similarity_result[all_topic_number])
        # print(temp_cos_sim_result2)
        Cosine_similarity_result.append(temp_cos_sim_result2)
        temp_cos_sim_result2 = []

    # print(Cosine_similarity_result[1])

    Cosine_similarity_matrix = []

    for cos in Cosine_similarity_result:
        temp = []
        for topic in cos:
            temp.append(topic[2])
        Cosine_similarity_matrix.append(temp)


    print("End of Making Cos Sim Matrix")
    return numpy.array(Cosine_similarity_matrix)

def Term_From_LDA_TO_Documents(All_KWK_CLASS, DOC_KWK_CLASS):
    all_result_lda = All_KWK_CLASS.result_lda
    All_topic_num = All_KWK_CLASS.topic_num
    Words_num = All_KWK_CLASS.words_num
    doc_topic_number = DOC_KWK_CLASS[0].topic_num
    doc_store = []
    all_term_store = []
    cls_store = []
    for items in all_result_lda:
        all_term_store.append(items[1])

    for cls in DOC_KWK_CLASS:
        doc_store.append(cls.texts)

    all_result = []
    temp_result = []

    matrix = term_matrix(all_term_store[0], doc_store)
    temp_re = []
    for alltopic in all_term_store:
        temp_re.append(term_matrix(alltopic, doc_store))




    index = 0
    f = open("C:\Alrescha\Research\FILE_LO\새파일.txt", 'a')
    f.write(','.join(str(x) for x in range(len(DOC_KWK_CLASS))))
    f.write("\n")

    for itemss in temp_re[index]:
        strasd = ','.join(str(x) for x in itemss)
        f.write(strasd + "\n")
    f.close()

    f = open("C:\Alrescha\Research\FILE_LO\새파일3.txt", 'a')
    strasd = ','.join(str(x) for x in all_term_store[index])
    f.write(strasd + "\n")
    f.close()

def term_matrix (all_topicnum_term, doc_list):
    result = []
    for terms in all_topicnum_term:

        temp_result = []
        for doc in doc_list:
            temp_result.append(doc[0].count(terms))
        result.append(temp_result)


    return result