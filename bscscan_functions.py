import hashlib
import time
import requests
from pyquery import PyQuery as pquery
import csv
from settings import COOKIE, USER_AGENT, SID
import datetime
import re
import time
import random


def get_html(url):
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    res = ""
    try:
        response = requests.request("GET", url, headers=headers)
        res = response.text
    except:
        print('network error')
    return res


def clear_html(html):
    re_obj = re.compile(r'<[^>]+>', re.S)
    text = re_obj.sub('', html)
    return text


def save_to_csv(filename, title, data_list):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        if len(title) > 0:
            csv_writer.writerow(title)
        for row in data_list:
            data = []
            for key in row:
                data.append(row[key])
            csv_writer.writerow(data)


def md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def cut_str(split_str, content):
    try:
        arr = split_str.split('*')
        arr2 = content.split(arr[0])
        arr3 = arr2[1].split(arr[1])
        res = arr3[0]
    except:
        res = ''
    return res


def get_page(sid, cookie, user_agent, c_address, w_address, p):
    url = 'https://bscscan.com/token/generic-tokentxns2?contractAddress=' + str(c_address) +\
          '&mode=&sid=' + str(sid) + '&a=' + str(w_address) + '&m=normal&p=' + str(p)
    payload = {}
    headers = {
        'cookie': cookie,
        'referer': 'https://bscscan.com/token/generic-tokentxns2?contractAddress=' +
                   str(c_address) + '&mode=&sid=' + str(sid) + '&a=' + str(w_address) +
                   '&m=normal&p=' + str(p),
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent
    }
    res = ''
    try:
        response = requests.request('GET', url, headers=headers, data=payload)
        res = response.text
    except:
        print('network error')
    return res


def get_total_supply(contractAddress, a):
  url = "https://bscscan.com/token/"+str(contractAddress)+"?a="+str(a)
  html = get_html(url)
  total_supply = cut_str('Total Supply:</span>*</span>', html)
  total_supply = clear_html(total_supply).strip()
  return total_supply


def get_data(sid, cookie, user_agent, c_address, w_address, time_frame):
    page = 1
    html = get_page(sid, cookie, user_agent, c_address, w_address, page)
    time.sleep(random.uniform(0.05,0.75))
    try:
        page_num = cut_str('of <strong class="font-weight-medium">*</strong>', html).strip()
        page_num = int(page_num)
    except:
        page_num = 0

    total_supply = get_total_supply(c_address, w_address)

    print('page_num:' + str(page_num))

    time_curr = datetime.datetime.utcnow()
    if time_frame == '24h':
        time_tgt = time_curr - datetime.timedelta(days=1)
    elif time_frame == '48h':
        time_tgt = time_curr - datetime.timedelta(days=2)
    # elif time_frame == '72h':
    else:
        time_tgt = time_curr - datetime.timedelta(days=3)
    print(time_curr)
    print(time_tgt)
    # test
    page_num = 2

    start_page = 1
    end_page = page_num

    title = ['Txn Hash', 'Method', 'Time', 'From', 'To', 'Quantity']
    mlist = {}
    num = 0
    for page in range(start_page, end_page + 1):
        time.sleep(0.25)
        print('get page:' + str(page))

        html = get_page(sid, cookie, user_agent, c_address, w_address, page)
        time.sleep(0.5)
        html = cut_str('<div class="table-responsive mb-2 mb-md-0">*<script', html)
        doc = pquery(html)

        for tr_info in doc('table tbody tr').items():
            num += 1
            # print(r)
            row = {}
            row['TxnHash'] = str(tr_info('td:nth-child(1)').text())
            row['Method'] = tr_info('td:nth-child(2)').text()
            row['Time'] = tr_info('td:nth-child(4) span').attr('title')
            row['From'] = tr_info('td:nth-child(5) span').attr('title')
            row['To'] = str(tr_info('td:nth-child(7)').text())

            try:
                row['Quantity'] = float(tr_info('td:nth-child(8)').text())
            except:
                row['Quantity'] = 0
            #print(row)

            key = str(num).zfill(10) + '_' + md5(row['TxnHash'] + row['Time'] + row['To'])
            mlist[key] = row

        for key in mlist:
            time_key = datetime.datetime.strptime(mlist[key]['Time'], '%Y-%m-%d %H:%M:%S')
            if time_key < time_tgt:
                break

    # dict mlist
    dlist = []
    for key in mlist:
        row = mlist[key]
        dlist.append(row)

    return total_supply, dlist


def get_quantity(sid, cookie, user_agent, c_address, w_address, time_frame, csv_name=''):
    total_supply, dlist = get_data(sid, cookie, user_agent, c_address, w_address, time_frame)
    title = ['Txn Hash', 'Method', 'Time', 'From', 'To', 'Quantity']

    # quantity coin created/destroyed
    quant = 0
    for row in dlist:
        quant += row['Quantity']

    if csv_name != '':
        print('导出csv')
        # export csv
        save_to_csv(csv_name, title, dlist)

    supply = float(total_supply.replace(',',''))

    percent_value = '{:.5%}'.format(quant/supply)

    return quant, float(supply), percent_value

if __name__ == '__main__':
    cookie = COOKIE
    user_agent = USER_AGENT
    sid = SID
    c_address = '0x53e562b9b7e5e94b81f10e96ee70ad06df3d2657'
    w_address = '0x0000000000000000000000000000000000000000'
    csv_name = 'data.csv'
    time_frame = '24h'

    print(get_quantity(sid, cookie, user_agent, c_address, w_address, time_frame))