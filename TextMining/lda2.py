import lda_test
string = r"""D:\Documents\2017\특허 유니버시티\특허\신동헌\미국 7~12.xlsx"""

cls_for_open_excel = lda_test.LDA_KWK('a', 1, 20, 5)

result = lda_test.Generate_with_Excel(cls_for_open_excel, string, 1, 0)
result2 = lda_test.Processing_Entire_Class(result)

result2[2].PrintResult()





# doc = cls_for_open_excel.Extract_Excel(string, 0, 5)
#
# print(len(doc))





# 추출전 연습용 !
#
# test = '''There is provided an on-vehicle device including an image acquisition unit, a moving-object detector, a display unit, a switching unit, and a switching instruction unit. The image acquisition unit acquires an image obtained by imaging a peripheral image around a vehicle. The moving-object detector, when the vehicle approaches an intersection, detects whether there is a moving object approaching the vehicle as an own vehicle from a left or a right direction of the intersection based on the peripheral image. The switching unit switches between images in a plurality of systems input to a display unit. The switching instruction unit instructs to switch to the peripheral image when the moving object is detected.'''
# test2 = '''Optical motion detectors of the type used in a computer mouse are mounted on the bottom of a vehicle for detecting motion of the vehicle along a surface. Position of the vehicle can thereafter be computed by “dead reckoning.” In a preferred arrangement, optical markings on the surface can be used, or other arrangements can be used, to calibrate the system. '''
#
# temp = lda_test.LDA_KWK(test, given_topic_num=1, given_words_num=10, given_pass_num=2)
# temp.LDA_TotalProcess()
#
# temp2 = lda_test.LDA_KWK(test2, given_topic_num=1, given_words_num=10, given_pass_num=2)
# temp2.LDA_TotalProcess()