from observer.utils.str_format import (str_to_md5str, )
from observer.utils.excel import (read_by_openpyxl, )
from observer.utils.logger import Logger
from observer.base.models import *


# init logging
logger = Logger(ln='test')
msg = """Scripts: <scripts/test.py>"""


def main():
   pass


def run():
    title = {'标题': 0 ,
            '链接': 0 ,
            '发布日期': 0 ,
            '抽查类别': 0 ,
            '抽查等级': 0 ,
            '抽检单位': 0 ,
            '地域': 0 ,
            '行业编号': 0 ,
            '产品名称': 0 ,
            '不合格企业': 0 ,
            '不合格企业地域': 0 ,
            '不合格项': 0 ,
            '抽查批次': 0 ,
            '合格批次': 0 ,
            '不合格批次': 0 }

    data = read_by_openpyxl(filename='/mnt/f/inspection.xlsx', title=title)