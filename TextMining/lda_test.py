# https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

from xlrd import open_workbook
import numpy

class LDA_KWK:
    def __init__(self, given_doc, given_topic_num, given_words_num, given_pass_num):
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

    # loop through document list
    def CleanDoc(self):
        # clean and tokenize document string
        raw = self.doc.lower()
        tokens = self.tokenizer.tokenize(raw)

        # remove stop words from tokens
        self.stopped_tokens = [i for i in tokens if not i in self.en_stop]

        # stem tokens
        self.stemmed_tokens = [self.p_stemmer.stem(i) for i in self.stopped_tokens]

        # add tokens to list
        self.texts.append(self.stemmed_tokens)

        # turn our tokenized documents into a id <-> term dictionary
        self.dictionary = corpora.Dictionary(self.texts)

        # convert tokenized documents into a document-term matrix
        self.corpus = [self.dictionary.doc2bow(text) for text in self.texts]

    # generate LDA model
    def Generate_LDA(self):
        self.CleanDoc()
        self.ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics=self.topic_num, id2word=self.dictionary,
                                                        passes=self.pass_num)

    def SplitTopics(self):
        #return [ [v,k] for k, v in self.show_topic(topicno, topn)]
        #gensim.ldamodel => print_topic
        temp_result = self.ldamodel.print_topic(topicno=0, topn=self.words_num)
        for pos in range(len(temp_result)):
            self.result_weight.append(temp_result[pos][0])
            self.result_terms.append(temp_result[pos][1])
        return 0

    def LDA_TotalProcess(self):
        self.Generate_LDA()
        self.SplitTopics()
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
    print("Start extracting document from given excel(lda_test)")


    temp_doc = ldaclass.Extract_Excel(excel_location, sheet_num, idx)
    result = []
    for docnum in range(len(temp_doc)):
        print(temp_doc[docnum])
        result.append(LDA_KWK(temp_doc[docnum], ldaclass.topic_num, ldaclass.words_num, ldaclass.pass_num))

    #엑실 읽기 끝!
    print("End extracting document from given excel")

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

# test_LDA = LDA_KWK(test)
# test_LDA.Generate_LDA()
# test_LDA.PrintTopics()
