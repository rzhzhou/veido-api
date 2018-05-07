from observer.utils.date_format import (str_to_date, get_months)
from observer.utils.str_format import (str_to_md5str, )
from observer.utils.excel import (read_by_openpyxl, write_by_openpyxl)
from observer.utils.logger import Logger
from observer.base.models import *


# init logging
logger = Logger(ln='test')
msg = """Scripts: <scripts/test.py>"""


def run():
    filename = "test.xlsx"
    data = [
        [1, 2, 3, 4, 5, 6],
        [7, 8, 9, 10, 11, 12]
    ]
    write_by_openpyxl(filename, data)