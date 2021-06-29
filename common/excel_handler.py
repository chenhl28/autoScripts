# -*- coding:utf-8 -*-
# @Author:huan
# @Time  :2021-06-01

import openpyxl
from pathlib import Path

class ExcelHandler:

    def __init__(self, file_name, sheet_name=None):
        self.file_name = Path.cwd().parent.joinpath("datas", file_name)
        self.sheet_name = sheet_name

    def open_wb(self):
        #打开工作簿
        self.wb = openpyxl.load_workbook(self.file_name)

        #获取要操作的工作表
        if not self.sheet_name:
            self.sh = self.wb.active
        else:
            self.sh = self.wb[self.sheet_name]

    def close_wb(self):
        self.wb.close()

    def read_wb(self):
        """按行读取数据，最后返回一个存储字典的列表"""
        self.open_wb()
        #获取所有行
        rows = list(self.sh.rows)

        #获取表头
        titles = []
        for t in rows[0]:
            title = t.value
            titles.append(title)

        all_info = []
        # 获取每行内容
        for row in rows[1:]:
            child = [cell.value for cell in row]
            all_info.append(dict(zip(titles, child))) #返回一个存储字典的列表
        self.close_wb()
        return all_info

    def write_wb(self, row, column, data):
        """
        往单元格写入数据
        :param row:
        :param column:
        :param data:
        :return:
        """
        self.open_wb()
        self.sh.cell(row=row, column=column, value=data)
        self.save_wb()
        self.close_wb()

    def save_wb(self):
        self.wb.save(self.file_name)


if __name__ == '__main__':
    eh = ExcelHandler("外卖平台测试用例.xlsx","登录模块")
    print(eh.read_wb())
    # for i in range(len(eh.read_wb())):
    #     eh.write_wb(i+2,13,"测试通过")