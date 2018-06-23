#!/usr/bin/python
# -*- coding:utf-8 -*-

import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders


class Email(object):
    """
    Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。
    """
    def __init__(self, email_subject, email_from, to_addr_list):
        """
        构造邮件对象，并设置邮件主题、发件人、收件人，最后返回邮件对象
        email_subject:邮件主题
        email_from:发件人
        to_addr_list:收件人列表
        """
        # 构造 MIMEMultipart 对象做为根容器
        email_obj = MIMEMultipart()
        email_to = ','.join(to_addr_list)  # 将收件人地址用“,”连接
        # 邮件主题、发件人、收件人
        email_obj['Subject'] = Header(email_subject, 'utf-8')
        email_obj['From'] = Header(email_from, 'utf-8')
        email_obj['To'] = Header(email_to, 'utf-8')

        self.email_obj = email_obj
        self.to_addr_list = to_addr_list
        self.email_from = email_from

    def attach_content(self, email_content, content_type='plain', charset='utf-8'):
        """
        创建邮件正文，并将其附加到跟容器：邮件正文可以是纯文本，也可以是HTML（为HTML时，需设置content_type值为 'html'）
        email_content:邮件正文内容
        content_type:邮件内容格式 'plain'、'html'..，默认为纯文本格式 'plain'
        charset:编码格式，默认为 utf-8
        """
        content = MIMEText(email_content, content_type, charset)  # 创建邮件正文对象
        self.email_obj.attach(content)  # 将邮件正文附加到根容器

    def attach_part(self, source_path, part_name):
        """
        添加附件：附件可以为照片，也可以是文档
        source_path:附件源文件路径
        part_name:附件名
        """
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data   创建附件对象
        part.set_payload(open(source_path, 'rb').read())  # 将附件源文件加载到附件对象
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % part_name)  # 给附件添加头文件
        self.email_obj.attach(part)  # 将附件附加到根容器

    def send_email(self, email_host, host_port, pwd):
        """
        发送邮件
        email_host:SMTP服务器主机
        host_port:SMTP服务端口号
        pwd:发件地址的授权码，而非密码
        发送成功，返回 True；发送失败，返回 False
        """
        try:
            '''
                # import smtplib
                # smtp_obj = smtplib.SMTP([host[, port[, local_hostname]]] )
                    # host: SMTP服务器主机。
                    # port: SMTP服务端口号，一般情况下SMTP端口号为25。
                # smtp_obj = smtplib.SMTP('smtp.qq.com', 25)
            '''
            smtp_obj = smtplib.SMTP_SSL(email_host, host_port)  # 连接 smtp 邮件服务器
            smtp_obj.login(self.email_from, pwd)
            smtp_obj.sendmail(self.email_from, self.to_addr_list, self.email_obj.as_string())  # 发送邮件：email_obj.as_string()：发送的信息
            smtp_obj.quit()  # 关闭连接
            print("发送成功！")
            return True
        except smtplib.SMTPException:
            print("发送失败！")
            return False
