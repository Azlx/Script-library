import csv
import datetime

from lxml import etree

START_TIME = '2020-01-16'
HTML_PATH = 'index.html'
CSV_PATH = '全国病例每日确诊数据.csv'

with open(HTML_PATH) as f:
    SELECTOR = etree.HTML(f.read())


def get_time_list():
    start_time = datetime.datetime.strptime(START_TIME, '%Y-%m-%d')
    
    now_time = datetime.datetime.now()
    end_time = datetime.datetime.strptime('{0}-{1}-{2}'.format(now_time.year, now_time.month, now_time.day), '%Y-%m-%d')

    time_list = []
    while start_time < end_time:
        time_list.append(start_time.strftime('%m-%d'))

        start_time += datetime.timedelta(days=1)

    return time_list


def get_citys_data():
    all_citys = SELECTOR.xpath('//g[@id="provinceGroupS"]/g/g[@class="prov rprov"]')

    citys_name = []
    citys_sum = []
    for city in all_citys:
        citys_name.append(city.xpath('g[@class="click"]/text')[0].text)
        citys_sum.append(city.xpath('g[@class="sum"]/text')[0].text)

    return citys_name, citys_sum


def get_all_case_data():
    all_case = SELECTOR.xpath('//g[@id="provinceGroupP"]/g/g[@class="prov rprov"]')

    citys_name, citys_sum = get_citys_data()

    all_city_case = []

    num = 0
    for case in all_case:
        all_days_case = case.xpath('g[@class="day"]')

        city_case = []
        # 加入城市名
        city_case.append(citys_name[num])
        for day_case in all_days_case:
            city_case.append(day_case.xpath('text')[0].text)

        # 加入城市病例总数
        city_case.append(citys_sum[num])

        all_city_case.append(city_case)

        num += 1
        
    return all_city_case


def save_csv():
    time_list = [''] + get_time_list() + ['sum']
    all_city_case = get_all_case_data()

    with open(CSV_PATH, 'w', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(time_list)
        writer.writerows(all_city_case)
    

if __name__ == '__main__':
    save_csv()

