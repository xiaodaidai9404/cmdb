import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys

mail_host = 'smtp.mxhichina.com'
mail_user = 'wuliang@ipaychat.com'
mail_pass = 'Fuliao10086'

def send_mail(to_list,subject,content):
    me = mail_user
    #print me
    msg = MIMEText(content,'plain','utf-8')
    msg["Accept-Language"]="zh-CN"
    msg["Accept-Charset"]="ISO-8859-1,utf-8"
    msg['Subject'] = subject
    msg['From'] = me
    msg['to'] = to_list
    #print msg

    try:
        s = smtplib.SMTP_SSL(mail_host,465)
        print s
        s.login(mail_user,mail_pass)
        s.sendmail(me,to_list,msg.as_string())
        s.close()
        return True
    except Exception,e:
        print str(e)
        return False

if __name__ == "__main__":
     send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
