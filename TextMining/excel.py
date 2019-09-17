from xlrd import open_workbook

def excel_converter(workbook, idx):
    document = workbook.sheet_by_index(idx)

    #row length:
    num_rows = document.nrows

    row_val = []
    for val in range(num_rows):
        #append string to row_val
        row_val.append(document.row_values(val)[0])
    return row_val

#98-01 documents
doc98_01 = excel_converter(open_workbook('C:\\Users\\Alrescha\\Documents\\카카오톡 받은 파일\\신동헌\\신동헌 중국.xlsx'), 0)
# doc98 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\1998-2001.xlsx'), 1)
# doc99 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\1998-2001.xlsx'), 2)
# doc00 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\1998-2001.xlsx'), 3)
# doc01 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\1998-2001.xlsx'), 4)
#
# #02-05 documents
# doc02_05 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2002-2005.xlsx'), 0)
# doc02 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2002-2005.xlsx'), 1)
# doc03 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2002-2005.xlsx'), 2)
# doc04 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2002-2005.xlsx'), 3)
# doc05 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2002-2005.xlsx'), 4)
#
# #06-09 documents
# doc06_09 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2006-2009.xlsx'), 0)
# doc06 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2006-2009.xlsx'), 1)
# doc07 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2006-2009.xlsx'), 2)
# doc08 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2006-2009.xlsx'), 3)
# doc09 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2006-2009.xlsx'), 4)
#
# #10-13 documents
# doc10_13 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2010-2013.xlsx'), 0)
# doc10 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2010-2013.xlsx'), 1)
# doc11 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2010-2013.xlsx'), 2)
# doc12 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2010-2013.xlsx'), 3)
# doc13 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2010-2013.xlsx'), 4)
#
# #14-16 documents
# doc14_16 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2014-2016.xlsx'), 0)
# doc14 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2014-2016.xlsx'), 1)
# doc15 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2014-2016.xlsx'), 2)
# doc16 = excel_converter(open_workbook('C:\\Users\\LG\\Desktop\\Task\\외식경영논문초록\\2014-2016.xlsx'), 3)

all_docs = []
def adder(docs):
    for doc in docs:
        all_docs.append(doc)

adder(doc98_01)
# adder(doc02_05)
# adder(doc06_09)
# adder(doc10_13)
# adder(doc14_16)