import re
import requests
import json

# global member
station_file = "stations.txt"
station_dict = {}
code_dict = {}

def format_date(date: str):
    # change date format
    result = date.replace('/', '-')

    match = re.search(r'-[0-9]-', result)
    if match:
        # change month format
        index = match.span(0)[0]  # find the index of result
        result = result[:index + 1] + '0' + result[index + 1:]  # insert '0'

    match = re.search(r'-[0-9]$', result)
    if match:
        # change day format
        index = match.span(0)[0]
        result = result[:index + 1] + '0' + result[index + 1:]

    return result


def get_station(url):
    response = requests.get(url)

    # 车站与代码格式: 北京|BJP
    stations = re.findall(r'([\u4e00-\u9fa5]+)\|([A-Za-z]+)', response.text)
    stations_code = dict(stations)
    stations_names = dict(list(zip(stations_code.keys(), stations_code.values())))
    return stations_names


def print_station(stations):
    for key in stations:
        print(key, stations[key])


def save_stations(file, stations):
    # save to file
    try:
        with open(file, 'w') as f:
            for key in stations:
                f.write(key + ' ' + stations[key] + '\n')
    except FileNotFoundError:
        print("file not find!")

    print("Done!")


def query_tickets(date: str, src: str, des: str, is_adult=True):
    # 12306 ticket query url
    url = "https://kyfw.12306.cn/otn/leftTicket/queryZ?"

    if not isinstance(src, str):
        print("source is not a station!")
    if not isinstance(des, str):
        print("destination is not a station!")

    date = "leftTicketDTO.train_date=" + date
    src = "&leftTicketDTO.from_station=" + src[:3]  # src[:3] can avoid include '\n'
    des = "&leftTicketDTO.to_station=" + des[:3]

    if is_adult:
        adult = "&purpose_codes=ADULT"  # adult
    else:
        adult = "&purpose_codes=0X00"  # children

    ticket_url = url + date + src + des + adult

    try:
        response = requests.get(ticket_url, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
    except:
        return ""

    # return html text
    return response.text


def get_tickets(html):
    html = json.loads(html)

    # table field
    name = ["station_train_code",
            "from_station_name",
            'start_time',
            "lishi",
            "swz_num",
            "zy_num",
            "ze_num",
            "gr_num",
            "rw_num",
            "dw_num",
            "yw_num",
            "rz_num",
            "yz_num",
            "wz_num",
            "qt_num",
            "note_num"]

    for i in html['data']['result']:

        # 数据字典
        data = {
            "station_train_code": '',
            "from_station_name": '',
            "to_station_name": '',
            'start_time': '',
            'end': '',
            "lishi": '',
            "swz_num": '',
            "zy_num": '',
            "ze_num": '',
            "dw_num": '',
            "gr_num": '',
            "rw_num": '',
            "yw_num": '',
            "rz_num": '',
            "yz_num": '',
            "wz_num": '',
            "qt_num": '',
            "note_num": ''
        }

        # data 赋值
        item = i.split('|')  # 用"|"进行分割
        data['station_train_code'] = item[3]  # 车次在3号位置
        data['from_station_name'] = item[6]  # 始发站信息在6号位置
        data['to_station_name'] = item[7]  # 终点站信息在7号位置
        data['start_time'] = item[8]  # 出发时间信息在8号位置
        data['arrive_time'] = item[9]  # 抵达时间在9号位置
        data['lishi'] = item[10]  # 经历时间在10号位置
        data['swz_num'] = item[32] or item[25]  # 特别注意：商务座在32或25位置
        data['zy_num'] = item[31]  # 一等座信息在31号位置
        data['ze_num'] = item[30]  # 二等座信息在30号位置
        data['gr_num'] = item[21]  # 高级软卧信息在31号位置
        data['rw_num'] = item[23]  # 软卧信息在23号位置
        data['dw_num'] = item[27]  # 动卧信息在27号位置
        data['yw_num'] = item[28]  # 硬卧信息在28号位置
        data['rz_num'] = item[24]  # 软座信息在24号位置
        data['yz_num'] = item[29]  # 硬座信息在29号位置
        data['wz_num'] = item[26]  # 无座信息在26号位置
        data['qt_num'] = item[22]  # 其他信息在22号位置
        data['note_num'] = item[1]  # 备注在1号位置

        # 如果没有信息用'-'代替
        for pos in name:
            if data[pos] == '':
                data[pos] = '-'


def get_station_name(file, code):

    try:
        with open(file, 'r') as f:
            text = f.readline()
            while text:
                item = text.split(' ')
                if item[1][:3] == code:
                    return item[0]  # return station name

                text = f.readline()
    except IndexError:
        return ""

    return ""


def get_station_code(file, name):
    try:
        with open(file, 'r') as f:
            text = f.readline()
            while text:
                item = text.split(' ')
                if item[0] == name:
                    return item[1]  # return station code

                text = f.readline()
    except IndexError:
        return ""
    
    return ""


def load_train_code(file, station, code):

    with open(file) as f:
        text = f.readline()
        while text:
            item = text.split(' ')
            station[item[1][:3]] = item[0]
            code[item[0]] = item[1][:3]

            text = f.readline()
