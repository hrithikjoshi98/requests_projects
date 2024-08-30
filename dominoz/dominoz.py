import json

import requests
import lxml.html
import datetime

def my_print(*args):
    string = ""
    for i in args:
        string += str(i) + "\n"
    print(string, '\n')


first_url = 'https://stores.dominos.co.in/'

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'cookie':'_ga_BWPE23X4WM=GS1.1.1724845655.1.0.1724845655.0.0.0; _ga=GA1.1.1543036451.1724845656'
}
request = requests.Session()
request.cookies.set('_ga_BWPE23X4WM', 'GS1.1.1724845655.1.0.1724845655.0.0.0')
request.cookies.set('_ga', 'GA1.1.1543036451.1724845656')
res1 = request.get(first_url, headers=header, timeout=10)

print(res1.status_code)

dom1 = lxml.html.fromstring(res1.text)
list_of_state = dom1.xpath('//*[@id="OutletState"]/option[position() > 1]/text()')
master_outlet_id = dom1.xpath('//*[@id="jsCurrentThemeMasterOutletid"]/@value')[0]
print("STATES", list_of_state)

my_dict = {}

pos = 0
for state in list_of_state:
    pos += 1
    print(f"({pos})", state)
    state_name = str(state).title().replace(" ", "-")
    params = {
        'master_outlet_id': f'{master_outlet_id}',
        'state_name': f'{state_name}',
    }
    res2 = request.get(
        'https://stores.vijaysales.com/getCitiesByMasterOutletIdAndStateName.php',
        params=params,
        # cookies=cookies,
        headers=header,
        timeout = 10
    )

    cities = json.loads(res2.text)
    # cities = res2.text

    # print("CITIES :", cities)
    city_dic = {}
    for city in cities:
        params = {
            'master_outlet_id': f'{master_outlet_id}',
            'city_name': f'{city}',
            'state_name': f'{state_name}',
        }

        res3 = request.get(
            'https://stores.dominos.co.in/getLocalitiesByMasterOutletIdAndCityName.php',
            params=params,
            # cookies=cookies,
            headers=header,
        )
        localities = json.loads(res3.text)
        # print("LOCALITIES", localities)
        lo = {}
        for locality in localities:

            main_url = f'https://stores.dominos.co.in/location/{state_name}/{city}/{locality}'
            res4 = request.get(
                main_url,
                # cookies=cookies,
                headers=header,
                timeout=10
            )
            # print(res4.text)
            dom2 = lxml.html.fromstring(res4.text)
            outlate_list = dom2.xpath('/html/body/section[2]/div/div[1]/div[2]/div/div')
            lo2 = {}
            posi = 1
            for outlate in outlate_list:
                locality_dic = {}
                outlet = ' '.join(outlate.xpath('//ul[@class="list-unstyled outlet-detail first"]/li[2]/div['
                                     '@class="info-text"]//text()')).strip()
                address = ' '.join(outlate.xpath('//span[contains(@class, "icn-address")]/parent::node('
                                              ')/following-sibling::node()[@class="info-text"]//text()')).strip()
                landmark = ' '.join(outlate.xpath('//span[contains(@class, "icn-landmark")]/parent::node('
                                               ')/following-sibling::node()['
                                      '@class="info-text"]//text()')).strip()
                phone = ' '.join(outlate.xpath('//span[contains(@class, "icn-phone")]/parent::node('
                                            ')/following-sibling::node()['
                                   '@class="info-text"]//text()')).strip()
                time = ' '.join(outlate.xpath('//span[contains(@class, "icn-time")]/parent::node()/following-sibling::node()['
                                  '@class="info-text"]//text()')).strip()

                map = ' '.join(outlate.xpath('//a[@class="btn btn-map"]/@href')).strip()
                website = ' '.join(outlate.xpath('//a[@class="btn btn-website"]/@href')).strip()


                locality_dic['state'] = state_name
                locality_dic['city'] = city
                locality_dic['outlet'] = outlet
                locality_dic['address'] = address
                locality_dic['landmark'] = landmark
                locality_dic['phone'] = phone
                locality_dic['time'] = time
                locality_dic['map'] = map
                locality_dic['website'] = website

                my_print("---------------------",
                        outlet,
                        address,
                        landmark,
                        phone,
                        time,
                         map,
                         website)
                lo2[f"outlet{posi}"] = locality_dic
                posi += 1
            lo[locality] = lo2
        city_dic[city] = lo
    my_dict[state] = city_dic



with open('dominoz.json', 'w') as file:
    y = json.dumps(my_dict)
    file.write(y)


