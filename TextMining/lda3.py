import lda_test
import kmean_ver_KWK


# string = r"""D:\Documents\2017\특허 유니버시티\특허\3. 미국.xlsx"""

# string = r"""C:\Alrescha\특허전략유니버시아드\신동헌\신동헌 중국.xlsx"""

string = r"""C:\Alrescha\특허전략유니버시아드\신동헌\us test.xlsx"""

# string = r"""D:\Development\Pycharm\textmine\2. 미국.xlsx"""



def findall(count):
    for i in range(count):

        cls_for_open_excel = lda_test.LDA_KWK('a', 1, 25, 50)

        result = lda_test.Generate_with_Excel(cls_for_open_excel, string, 0, 0)
        result2 = lda_test.Processing_Entire_Class(result)
        result3 = lda_test.Create_Matrix(result2)

        kmean = kmean_ver_KWK.ScableKmenas(result3, g_l=50, g_k=150, g_first_center=5, g_l_multipler=0.5)

        print("\n\nStart Clustering\n K value : ", kmean.k, "/ L value : ", kmean.l, "/ Multipler : ",
              kmean.multipler, "/ Number of first Center : ", len(kmean.init_center),
              "/ Topic number : ", cls_for_open_excel.topic_num, "/ Number of terms : ",
              cls_for_open_excel.words_num, "/ Term Pass count : ", cls_for_open_excel.pass_num, "\n\n")

        resultt = kmean.Final_Result()

        temp = list(resultt[1])
        result_array = [];

        for center_number in range(kmean.k):
            result_center_array = []
            for doc_index in range(len(temp)):
                if (temp[doc_index] == center_number):
                    result_center_array.append(doc_index + 2)
            result_array.append(result_center_array)
            print("Center Number : ", center_number, "Doc list : ", result_array[center_number])
        print("\n\nCounting Number : ", i + 1, "\n\n\n\n")
    return result_array


# 모든 문서들의 최종 클러스터링 결과 출력 !
a = 10
findall(a)































# 번호 보다 -2 ! 예를 들어 엑셀 2번째 행 서부터 문서가 있는데,
# 거기서 143번을 지정하고 싶을 땐, 141을 넣으면 됨!
# 출력 되는 결과는 +2 되어서 나옴!

# finddoc(141, a)




# def finddoc(idx, count):
#     for i in range(count):
#
#         cls_for_open_excel = lda_test.LDA_KWK('a', 1, 30, 1)
#
#         result = lda_test.Generate_with_Excel(cls_for_open_excel, string, 1, 0)
#         result2 = lda_test.Processing_Entire_Class(result)
#         result3 = lda_test.Create_Matrix(result2)
#
#         kmean = kmean_ver_KWK.ScableKmenas(result3, g_l=10, g_k=50, g_first_center=5, g_l_multipler=0.9)
#         resultt = kmean.Final_Result()
#
#
#         temp = list(resultt[1])
#         rr = []
#         for pos in range(len(temp)):
#             if (temp[pos] == temp[idx]):
#                 rr.append(pos + 2)
#
#         print("Count : ", i, "result : ", rr)
#
#     print("\n\n K value : ", kmean.k, "L value : ", kmean.l, "Multipler : ",
#           kmean.multipler, "Number of first Center : ", len(kmean.init_center),
#           "Topic number : ", cls_for_open_excel.topic_num, "Number of terms : ",
#           cls_for_open_excel.words_num, "Term Pass count : ", cls_for_open_excel.pass_num)
#     return 0





# 일단 맞는듯...?
# print(lda_test.Gathering_Terms(result2))
# print(result2[0].result_terms)
# print(result2[0].result_weight)
# print(result3[0])



# 파일 저장 & 출력 테스트...
# https://wikidocs.net/26
# f = open(r"D:\Development\Pycharm\textmine\test_extract_result.txt", 'w')
# f.write(result2)
# f.close()
