import re
import dns.resolver
import socket
import smtplib

def main(event, context):
    mail_address = event["queryStringParameters"]["mail_address"]

    # メールアドレス構文チェック
    match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', mail_address)
    if match == None:
        return {
            "statusCode": 400,
            "body": "Syntax error"
        }

    # ドメインチェック
    mail_domain = re.search("(.*)(@)(.*)", mail_address).group(3) # ドメイン部分の取り出し
    try:
        records  = dns.resolver.query(mail_domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        print(mxRecord)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": "None of DNS query names exist"
        }

    # メールアドレス存在チェック
    local_host = socket.gethostname()

    server = smtplib.SMTP(timeout=5)
    server.set_debuglevel(0)

    try:
        server.connect(mxRecord)
        server.helo(local_host)
        server.mail('test@example.com')
        code, message = server.rcpt(str(mail_address))
        server.quit()

        if code == 250:
            return {
                "statusCode": 200,
                "body": "Address exists"
            }
        else:
            return {
                "statusCode": 400,
                "body": "Address does not exists"
            }
    except Exception as e:
        print(e)

