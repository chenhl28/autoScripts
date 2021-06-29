# -*- coding:utf-8 -*-
# @Author:huan
# @Time  :2021-06-10

import configparser
import traceback
import json
import yaml

from common.log_handler import log
from pathlib import Path
from string import Template

#获取项目路径
rootPath = Path.cwd().parent

class ReadFileData:

    def load_ini(self, file_path):
        """读取ini文件"""
        file_name = Path.joinpath(rootPath, file_path)

        log.info(f"加载{file_name}文件......")
        cf = configparser.ConfigParser()
        try:
            cf.read(file_name, encoding="utf-8")
            data = dict(cf._sections)
            log.info(f"读到ini文件数据 ==>>  {data}")
            return data
        except FileNotFoundError as err:
            log.error("文件不存在")
            log.error(traceback.format_exc(err))
        except Exception as e:
            log.error("文件出错啦......")
            log.error(traceback.format_exc(e))

    def load_json(self, file_path):
        """加载json文件"""
        file_name = Path.joinpath(rootPath, file_path)

        log.info(f"加载{file_name}文件......")
        with open(file_name, encoding="utf-8") as f:
            self.json_data = json.load(f)
        log.info(f"读到json文件数据 ==>>  {self.json_data}")
        return self.json_data

    def load_yaml(self, yaml_path, json_path=None):
        """
        读取yaml文件
        :param yaml_path: yaml文件路径
        :param json_path: json文件路径
        :return:
        """
        yaml_name = Path.joinpath(rootPath, yaml_path)
        log.info(f"加载{yaml_name}文件......")

        if json_path:
            json_name = Path.joinpath(rootPath, json_path)
            #加载json文件
            self.load_json(json_name)

            with open(yaml_name, encoding="utf-8") as f:
                res = Template(f.read()).safe_substitute(self.json_data)
                data = yaml.safe_load(res)
            log.info(f"读到yaml文件数据 ==>>  {data}")
            return data
        else:
            with open(yaml_name, encoding="utf-8") as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            log.info(f"读到yaml文件数据 ==>>  {data}")
            return data

    def write_yaml(self, yaml_path, data):
        """
        写数据到yaml文件
        :param yaml_path:要写入数据的yaml文件的路径
        :param data: 要写入的数据
        :return:
        """
        yaml_name = Path.joinpath(rootPath, yaml_path)
        if not Path.exists(yaml_name):
            Path.touch(yaml_name)

        with open(yaml_name, "w", encoding="utf-8") as f:
            yaml.dump(data, stream=f, allow_unicode = True)


read = ReadFileData()

if __name__ == '__main__':
    # ini_data = read.load_ini("configs\cfg.ini")
    # # print(ini_data['poll']['url'])
    # json_data = read.load_json("datas\data.json")
    # # print(json_data)
    # yaml_data = read.load_yaml(r"datas\testdata.yml", "datas\data.json")
    # # print(yaml_data)
    # data = read.load_yaml(r"datas\testdata.yml")
    desired_caps = {
    "status": 1,
    "code": "1001",
    "data": [
        {
            "id": 80,
            "regname": "toml",
            "pwd": "QW&@JBK!#&#($*@HLNN",
            "mobilephone": "13691579846",
            "leavemount": "0.00",
            "type": "1",
            "regtime": "2019-08-14 20:24:45.0"
        },
        {
            "id": 81,
            "regname": "toml",
            "pwd": "QW&@JBK!#&#($*@HLNN",
            "mobilephone": "13691579846",
            "leavemount": "0.00",
            "type": "1",
            "regtime": "2019-08-14 20:24:45.0"
        }
    ],
    "msg": "获取用户列表成功"
}
    read.write_yaml("datas\data.yml", desired_caps)