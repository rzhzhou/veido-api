from xlrd import open_workbook, xldate_as_tuple
from datetime import datetime


def read(filename=None, file_contents=None, title={}):
    '''
    title like this:
    {
        'GUID': 0, 
        '标题': 0, 
        'URL': 0, 
        '发布时间': 0, 
        '发布媒体': 0, 
        '风险程度': 0, 
        '地域': 0, 
        '类别': 0, 
    }
    '''
    wb = open_workbook(filename=filename, file_contents=file_contents)
    sheet = wb.sheet_by_index(0)
    rows = sheet.nrows
    cols = sheet.ncols

    rvalues = sheet.row_values(0)
    for k in title.keys():
        title[k] = rvalues.index(k)

    # DATA FORMAT
    def format(i, j):
        ctype = sheet.cell(i, j).ctype  # 表格的数据类型
        cell = sheet.cell_value(i, j)
        if ctype == 2 and cell % 1 == 0:  # 如果是整形
            cell = int(cell)
        elif ctype == 3: # 转成datetime对象
            cell = datetime(*xldate_as_tuple(cell, 0))
        elif ctype == 4:
            cell = True if cell == 1 else False

        return cell

    data = []
    for i in range(1, rows):
        data2 = {}
        for k, v in title.items():
            data2[k] = format(i, v)
        data.append(data2)

    return data