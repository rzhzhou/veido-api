#coding:utf-8
import sys
import os
import time
import datetime, calendar
import random
import StringIO

import xlsxwriter

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

reload(sys)
sys.setdefaultencoding("utf-8")

class article():
    def get_output(self, data):
        workbook = None
        # path = os.path.dirname(__file__)+"/briefing.xlsx"
        output = StringIO.StringIO()
        self.workbook = xlsxwriter.Workbook(output)
        drawing(self.workbook, data)
        saveXls(self.workbook)
        return output


def drawing(workbook, data):
    worksheet = default(workbook, data)
    line_chart(workbook, worksheet, data["trend"])
    column_chart(workbook, worksheet, data["bar"])
    pie_chart(workbook, worksheet, data["source"])


def default(workbook, data):
    worksheet = workbook.add_worksheet()

    #set line chart
    headings = ["星期", "行业统计"]
    bold = workbook.add_format({'bold': 1})
    bold.set_bg_color('#dddddd')

    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)

    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data["trend"]["labels"])
    worksheet.write_column('B2', map(int, data["trend"]["data"]))

    #set column chart
    headings = ["关键字", "统计"]
    bold = workbook.add_format({'bold': 1})
    bold.set_bg_color('#dddddd')

    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)

    worksheet.write_row('A24', headings, bold)
    if data["bar"]["show"] == "true":
        lose = map(int, data["bar"]["data"][0])
        lose = [-l for l in lose]
        dataList = lose + map(int, data["bar"]["data"][1])

    else:
        dataList = map(int, data["bar"]["data"][0])
    worksheet.write_column('A25', data["bar"]["labels"])
    worksheet.write_column('B25', dataList)

    #set pie
    headings = ["来源", "统计"]
    bold = workbook.add_format({'bold': 1})
    bold.set_bg_color('#dddddd')

    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:B', 10)

    worksheet.write_row('A48', headings, bold)
    dataList = []
    labels = []
    for dicts in data["source"]["data"]:
        labels.append(dicts["name"])
        dataList.append(int(dicts["value"]))

    worksheet.write_column('A49', labels)
    worksheet.write_column('B49', dataList)

    #set text data
    headings = ["序号", "标题", "来源", "发表时间"]
    bold = workbook.add_format({'bold': 1})
    bold.set_bg_color('#dddddd')

    worksheet.set_column('C:C', 10)
    worksheet.set_column('D:D', 74)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 24)

    worksheet.write_row('C72', headings, bold)
    ids, titles, source, time = [], [], [], []
    for dicts in data["list"]["items"]:
        ids.append(dicts['id'])
        titles.append(dicts['title'])
        source.append(dicts['source'])
        time.append(dicts['time'])

    worksheet.write_column('C73', ids)
    worksheet.write_column('D73', titles)
    worksheet.write_column('E73', source)
    worksheet.write_column('F73', time)

    return worksheet


def line_chart(workbook, worksheet, data):
    length = len(data["labels"])
    values = '=Sheet1!$B$2:$B$%s'%(length+1)
    categories = '=Sheet1!$A$2:$A$%s'%(length+1)

    chart = workbook.add_chart({'type': 'line'})
    chart.set_size({'width': 900, 'height': 400})
    chart.add_series({
        'name': u"趋势",
        'values':     values,
        'categories': categories,
        'marker':     {'type': 'circle', 'fill':0},
        'smooth':     True,
        'line':       {'color': "#4169E1"},
    })
    chart.set_style(47)
    chart.set_title ({'name': '行业统计'})
    chart.set_x_axis({'name': '星期'})
    chart.set_chartarea({'fill':   {'color': "#363636"}})

    worksheet.insert_chart('C1', chart, {'x_offset': 20, 'y_offset': 20})


def column_chart(workbook, worksheet, data):
    length = len(data["labels"])
    values = '=Sheet1!$B$25:$B$%s'%(length+24)
    categories = '=Sheet1!$A$25:$A$%s'%(length+24)

    chart = workbook.add_chart({'type': 'column'})
    chart.set_size({'width': 900, 'height': 400})
    chart.add_series({
        'name':       '关键字统计',
        'categories': categories,
        'values':     values,
        'data_labels': {'value': True}
        })
    # Add a chart title and some axis labels.
    chart.set_title ({'name': '关键字统计'})
    chart.set_x_axis({'name': '项'})
    chart.set_y_axis({'name': '数量 (条)'})
    chart.set_chartarea({'fill':   {'color': "#363636"}})

    # Set an Excel chart style.
    chart.set_style(47)
    worksheet.insert_chart('C23', chart, {'x_offset': 20, 'y_offset': 20})


def pie_chart(workbook, worksheet, data):
    length = len(data["labels"])
    values = '=Sheet1!$B$49:$B$%s'%(length+48)
    categories = '=Sheet1!$A$49:$A$%s'%(length+48)
    chart = workbook.add_chart({'type': 'pie'})

    points = []
    for x in xrange(length):
        color = get_random_color()
        points.append({'fill': {'color': color}})

    chart.add_series({
        'name':       '饼图',
        'categories': categories,
        'values':     values,
        'data_labels': {'value': True, 'category': True},
        'points': points
    })
    chart.set_size({'width': 900, 'height': 400})
    chart.set_style(47)
    chart.set_rotation(28)
    chart.set_chartarea({'fill':   {'color': "#363636"}})

    worksheet.insert_chart('C47', chart, {'x_offset': 20, 'y_offset': 20})


def get_random_color():
    colorList = ['0', '1', '2', '3', '4', '5',
                '6', '7', '8', '9', 'A',
                'B', 'C', 'D', 'E', 'F'
    ]
    color = "#"
    for x in xrange(6):
        color += color.join(random.choice(colorList))

    return color



def saveXls(workbook):
    workbook.close()

