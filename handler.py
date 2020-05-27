import json
import re
import dns.resolver
import socket
import smtplib
import urllib
from multiprocessing import Process, Manager

def main(event, context):
    request_params = event['body']

    decoded_str = urllib.parse.unquote(request_params)
    mail_addresses = re.split(r'mailAddresses\[\]=', decoded_str)

    mail_addresses = list(filter(lambda x:False if len(x) == 0 else True, mail_addresses))
    mail_addresses = list(map(lambda x: x.rstrip('&'), mail_addresses))

    returned_array = Manager().list()
    process_list = []
    for mail_address in mail_addresses:
        p = Process(
            target=check,
            kwargs={
                'mail_address': mail_address,
                'returned_array': returned_array
            })
        p.start()
        process_list.append(p)

    for process in process_list:
        process.join()

    returned_array = '|'.join(returned_array)
    print(returned_array)
    return {
        "statusCode": 200,
        "body": returned_array
    }

def check(mail_address, returned_array):
    # メールアドレス構文チェック
    match = re.match('[A-Za-z0-9._+]+@[A-Za-z]+.[A-Za-z]', mail_address)
    if match == None:
        result = json.dumps({
            "statusCode": 500,
            "message": "syntax error",
            "mailAddress": mail_address
        })
        returned_array.append(result)
        return

    # ドメインチェック
    mail_domain = re.search("(.*)(@)(.*)", mail_address).group(3) # ドメイン部分の取り出し
    try:
        records  = dns.resolver.query(mail_domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        print(mxRecord)
    except Exception as e:
        result = json.dumps({
            "statusCode": 500,
            "message": "None of DNS query names exist",
            "mailAddress": mail_address
        })
        returned_array.append(result)
        return

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

        result = json.dumps({
            "statusCode": code,
            "message": "Address exists" if code == 250 else "Address doesnt exists",
            "mailAddress": mail_address
        })
        returned_array.append(result)
        return
    except Exception as e:
        print(e)
