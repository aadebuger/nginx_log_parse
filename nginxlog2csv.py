#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import csv
import optparse
import re
import sys
import arrow

# 定义正则表达式
re_ = re.compile('''
                ^(?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s  # IP 地址
                -\s
                (?P<remote_user>.*?)\s                                  # 用户名
                \[(?P<time_local>.*?)\]\s                               # 日期时间
                "(?P<request>.*?)"\s                                    # 请求头
                (?P<status>\d{3})\s                                     # 状态
                (?P<body_bytes_sent>\d+)\s                              # 大小
                "(?P<http_referer>.*?)"\s                               # 跳转自
                "(?P<http_user_agent>.*?)"$                             # 用户代理
                ''', re.X)


# 选项生成函数
def options_gen():
    option = optparse.OptionParser()
    option.add_option('-i', '--input', dest='nginx_log_path', help='assign input nginx log file path')
    option.add_option('-o', '--output', dest='csv_file_path', help='assign output csv file path')
    return option.parse_args()


# 逐行正则匹配函数
def line_to_dict(line):
    return re_.search(line).groupdict()


# 写入 CSV 文件函数
def dict_write_to_csv(dict, line_no):
    if line_no == 1:  # 在第一行前面加入表头
#        csv.DictWriter(csv_file_output_fd, dict.keys()).writeheader()
         pass
    csv.DictWriter(csv_file_output_fd, dict.keys()).writerow(dict)


if __name__ == '__main__':
    if not len(sys.argv) == 1:  # 没有输入参数时自动打印帮助
        pass
    else:
        sys.argv.append('-h')
    (options, value) = options_gen()  # 生成选项
    with open(options.csv_file_path, 'w') as csv_file_output_fd:  # 打开 CSV 文件
        with open(options.nginx_log_path, 'r') as nginx_log_file_fd:  # 打开日志文件
            line_no = 1  # 初始化行号
            for line in nginx_log_file_fd:
                dict = line_to_dict(line)  # 调用逐行正则匹配函数
#                print(dict)
                oldtime =dict['time_local']
                x = arrow.Arrow.strptime(oldtime, 
                         '%d/%b/%Y:%H:%M:%S %z')
#                print("x=",x)
                dict['time_local']=x
                dict_write_to_csv(dict, line_no)  # 调用写入 CSV 文件函数
                line_no += 1  # 行号加 1
