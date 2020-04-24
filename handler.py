import json
import re
import dns.resolver
import socket
import smtplib
import urllib

# def main(event, context):
def main(request_params):
    # request_params = event['body']

    decoded_str = urllib.parse.unquote(request_params)
    mail_addresses = re.split('mailAddresses\[\]=', decoded_str)

    mail_addresses = list(filter(lambda x:False if len(x) == 0 else True, mail_addresses))
    mail_addresses = list(map(lambda x: x.rstrip('&'), mail_addresses))

    response = []
    for mail_address in mail_addresses:
        checked = check(mail_address)
        response.append(checked)
        print(checked)

    ','.join(response)
    print(response)
    return response

def check(mail_address):
    # メールアドレス構文チェック
    match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', mail_address)
    if match == None:
        return json.dumps({
            "statusCode": 500,
            "message": "syntax error",
            "mailAddress": mail_address
        })

    # ドメインチェック
    mail_domain = re.search("(.*)(@)(.*)", mail_address).group(3) # ドメイン部分の取り出し
    try:
        records  = dns.resolver.query(mail_domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        print(mxRecord)
    except Exception as e:
        return json.dumps({
            "statusCode": 500,
            "message": "None of DNS query names exist",
            "mailAddress": mail_address
        })

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

        return json.dumps({
            "statusCode": code,
            "message": "Address exists" if code == 250 else "Address doesnt exists",
            "mailAddress": mail_address
        })
    except Exception as e:
        print(e)
