import json
import requests
import lxml.html
from icecream import ic


def my_print(*args):
    string = ""
    for i in args:
        string += str(i) + "\n"
    print(string, '\n')

cookies = {
    '_ga': 'GA1.1.1790363545.1724665573',
    '_ga_Q4NXH4SZM1': 'GS1.1.1724904417.6.1.1724905417.0.0.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache','pragma': 'no-cache',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}
main_url = 'https://stores.vijaysales.com/'
res1 = requests.get(main_url, cookies=cookies, headers=headers)

# print(res1.text)

dom1 = lxml.html.fromstring(res1.text)

state_list = dom1.xpath('//*[@id="OutletState"]/option[1 < position()]//text()')

master_outlet_id = dom1.xpath('//input[@id = "jsMasterOutletId"]/@value')

main_root_dict = {}

for state in state_list:
    state_name = str(state).title().replace(' ', '-').strip()
    params = {
        'master_outlet_id': master_outlet_id,
        'state_name': state_name,
    }

    res2 = requests.get(
        'https://stores.vijaysales.com/getCitiesByMasterOutletIdAndStateName.php',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    city_dict = json.loads(res2.text)
    main_state_dict = {}
    for city in city_dict:
        res4 = requests.get(
                f'https://stores.vijaysales.com/location/{state_name}/{city}',
                cookies=cookies,
                headers=headers,
            )

        dom2 = lxml.html.fromstring(res4.text)
        outlet_list = dom2.xpath('//div[@class="store-info-box"]')
        next_page_available, page = True, 1
        no_of_outlet = 0
        main_city_dict = {}

        while next_page_available:

            for outlet in outlet_list:
                main_outlet_dict = {}
                location = ' '.join(outlet.xpath('.//span[contains(@class,"business")]/parent::node()/following-sibling::node()[@class="info-text"]//text()')).strip()
                address = ' '.join(outlet.xpath('.//span[contains(@class,"address")]/parent::node()/following-sibling::node()[@class="info-text"]//text()')).strip()
                landmark = ' '.join(outlet.xpath('.//span[contains(@class,"landmark")]/parent::node()/following-sibling::node()[@class="info-text"]//text()')).strip()
                phone = ' '.join(outlet.xpath('.//span[contains(@class,"phone")]/parent::node()/following-sibling::node()[@class="info-text"]//text()')).strip()
                time = ' '.join(outlet.xpath('.//span[contains(@class,"time")]/parent::node()/following-sibling::div[@class="info-text"]/span//text()')).strip()
                map = ' '.join(outlet.xpath('.//span[contains(@class,"map")]/parent::node()/@href')).strip()
                website = ' '.join(outlet.xpath('.//span[contains(@class,"website")]/parent::node()/@href')).strip()
                no_of_outlet += 1
                # my_print("---------------------",
                #          str(page)+f"-{str(no_of_outlet)}",
                #          state,
                #          city,
                #          location,
                #          address,
                #          landmark,
                #          phone,
                #          time,
                #          map,
                #          website)
                main_outlet_dict['state'] = state
                main_outlet_dict['city'] = city
                main_outlet_dict['location'] = location
                main_outlet_dict['address'] = address
                main_outlet_dict['landmark'] = landmark
                main_outlet_dict['phone'] = phone
                main_outlet_dict['time'] = time
                main_outlet_dict['map'] = map
                main_outlet_dict['website'] = website
                main_city_dict[location] = main_outlet_dict
                ic(main_city_dict)

            try:
                next_page_url = dom2.xpath('//li[@class="next"]/a/@href')
                if next_page_url == []:
                    next_page_available = False
                else:
                    page += 1
                    params = {
                        'page': page,
                    }
                    res5 = requests.get(f'https://stores.vijaysales.com/location/{state_name}/{city}', params=params,
                                            cookies=cookies, headers=headers)
                    dom2 = lxml.html.fromstring(res5.text)
                    outlet_list = dom2.xpath('//div[@class="store-info-box"]')
            except:
                next_page_available = False
        main_state_dict[city] = main_city_dict
    main_root_dict[state] = main_state_dict

json_file_name = main_url.split('//')[1].split('/')[0].replace('.','_').strip()

with open(json_file_name+'.json', 'w') as file:
    json_data = json.dumps(main_root_dict)
    file.write(json_data)