from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import textmining
import numpy



def clean(doc):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()

    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())


    return normalized



def translist(nor):

    temp = 0
    count = 0

    for i in range(len(nor)):
        for j in range(len(nor[i])):
            temp = temp + 1

    test_terms = [0 for i in range(temp)]

    for i in range(len(nor)):
        for j in range(len(nor[i])):
            test_terms[count] = nor[i][j]
            count = count + 1
    return test_terms

def reduplication(trans):
    trans = list(set(trans))
    # temp_save = [0 for i in range(len(trans))]
    # count = 0
    #
    # # for i in range(len(trans)):
    # #     for j in range(len(trans)):
    # #         if (trans[i] == trans[j] and i != j):
    # #             temp_save[count] = j
    # #             count = count + 1
    # #
    # # if (len(temp_save) != 0):
    # #     for i in range(len(temp_save)):
    # #         if (temp_save[0] == 0 or temp_save[i] != 0):
    # #             del trans[temp_save[i]]

    return trans

def cleantotaldoc(docset):
    return [clean(i).split() for i in docset]



def totalDocProcess(total):
    temp = translist(cleantotaldoc(total))
    final = reduplication(temp)
    return sorted(final)



def createrepeatmartix(totaldoc):
    temp_totaldoc = totalDocProcess(totaldoc)
    temp_targetdoc = cleantotaldoc(totaldoc)

    temp_matrix = [[0 for column in range(len(temp_targetdoc))] for row in range(len(temp_totaldoc))]

    for row in range(len(temp_matrix)):
        for col in range(len(temp_matrix[0])):
            for tarcol in range(len(temp_targetdoc[col])):
                # print(temp_totaldoc[row], temp_targetdoc[col][tarcol], "\n\n")
                if(temp_totaldoc[row] == temp_targetdoc[col][tarcol]):
                    temp_matrix[row][col] = temp_matrix[row][col] + 1

    return numpy.array(temp_matrix).astype(numpy.float64).T


def ExtractwithValues (document, identify_value, second_value):
    temp_matrix = createrepeatmartix(document)
    temp_totaldoc = totalDocProcess(document)
    final_list = ['' for i in range(len(temp_totaldoc))]
    second_list = ['' for i in range(len(temp_totaldoc))]
    count_term_list = ['' for i in range(len(temp_totaldoc))]
    count_final = 0
    count_second = 0
    count_term_list_number = 0

    for doc_number in range(len(temp_matrix)):
        for term_number in range(len(temp_totaldoc)):
            if (temp_matrix[doc_number][term_number] >= second_value):
                second_list[count_second] = temp_totaldoc[term_number]
                count_second += 1
                final_list[count_final] = temp_totaldoc[term_number]
                count_final += 1
            elif (temp_matrix[doc_number][term_number] >= identify_value):
                final_list[count_final] = temp_totaldoc[term_number]
                count_final += 1

    final_list = list(set(final_list))
    second_list = list(set(second_list))
    return [sorted(final_list, reverse=True), sorted(second_list, reverse=True)]

    return final_list



def createrepeatmartix2(totaldoc,terms):

    temp_totaldoc = terms
    temp_targetdoc = cleantotaldoc(totaldoc)

    temp_matrix = [[0 for column in range(len(temp_targetdoc))] for row in range(len(temp_totaldoc))]

    for row in range(len(temp_matrix)):
        for col in range(len(temp_matrix[0])):
            for tarcol in range(len(temp_targetdoc[col])):
                # print(temp_totaldoc[row], temp_targetdoc[col][tarcol], "\n\n")
                if(temp_totaldoc[row] == temp_targetdoc[col][tarcol]):
                    temp_matrix[row][col] = temp_matrix[row][col] + 1

    return numpy.array(temp_matrix).astype(numpy.float64).T
