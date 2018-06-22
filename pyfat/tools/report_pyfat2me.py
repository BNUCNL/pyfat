#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from pyfat.tools.myemail import Email
# 邮件发送报告
# （QQ邮箱）
# email_host = "smtp.qq.com"  # smtp 邮件服务器
# host_port = 465  # smtp 邮件服务器端口：SSL 连接
# from_addr = "发件地址"  # 发件地址
# pwd = "授权码"  # 发件地址的授权码，而非密码------每次发送报告前需要修改

# （163邮箱）
email_host = "smtp.163.com"             # smtp 邮件服务器
host_port = 465                       # smtp 邮件服务器端口：SSL 连接
from_addr = "jiangjianbnu@163.com"                  # 发件地址
pwd = "jiangjianbnu163"                    # 发件地址的授权码，而非密码

# 获取最新生成的测试报告附件
result_dir = r'/home/brain/workingdir/pyfat/bin/old_cmd'
# 将文件都放到一个数组中
lists = os.listdir(result_dir)
# 将目录下的文件排序
lists.sort()
# 找到最新生成的文件
file_new = os.path.join(lists[-1])
source_path = result_dir + '/' + file_new
print source_path

# 邮件内容
to_addr_list = ["jiangjianbnu@163.com"]  # 收件地址
email_content = "这是本次自动化测试报告，请查收"
email_subject = "自动化测试报告"
part_name = 'test.html'

email_obj = Email(email_subject, from_addr, to_addr_list)
email_obj.attach_content(email_content)
email_obj.attach_part(source_path, part_name)
email_obj.send_email(email_host, host_port, pwd)
