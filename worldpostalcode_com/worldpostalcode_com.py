import requests
import json
import pymysql
import lxml.html

conn = pymysql.connect(
        host='localhost',
        user='root',
        password="actowiz",
        db='casio',
        autocommit=True
    )
cur = conn.cursor()

cur.execute(f'''CREATE TABLE IF NOT EXISTS worldpostalcode_links(id int AUTO_INCREMENT PRIMARY KEY, continent varchar(
100), country varchar(100), 
links varchar(1000),
status varchar(50))''')
conn.commit()

first_url = 'https://worldpostalcode.com'

res1 = requests.get(first_url)

dom1 = lxml.html.fromstring(res1.text)

continant_list = dom1.xpath('//div[@class="regions"]')

def rec(continant, contry, url, cur):
    res2 = requests.get(url)
    dom2 = lxml.html.fromstring(res2.text)
    regions_ava = dom2.xpath('//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]')
    code_ava = dom2.xpath('//div[@class="codes"]')
    if regions_ava and code_ava:
        print('1 url save :', url)
        cur.execute(f"""INSERT INTO worldpostalcode_links(continent, country, links, status) 
                VALUES('{continant}','{contry}','{url}','panding')""")
        regious_list = dom2.xpath('//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]/a/@href')
        for reg in regious_list:
            link = first_url + reg
            rec(continant, contry, link, cur)
    elif regions_ava and code_ava == []:
        regious_list = dom2.xpath('//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]/a/@href')
        for reg in regious_list:
            link = first_url + reg
            rec(continant, contry, link, cur)
    elif regions_ava == [] and code_ava:
        print('3 url save :', url)
        cur.execute(f"""INSERT INTO worldpostalcode_links(continent, country, links, status) 
        VALUES('{continant}','{contry}','{url}','panding')""")
    elif regions_ava == [] and code_ava == []:
        print('4 no code')


def rec_new(continent, country, url, cur):
    res = requests.get(url)
    dom = lxml.html.fromstring(res.text)

    regions_ava = dom.xpath('//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]')
    code_ava = dom.xpath('//div[@class="codes"]')

    if regions_ava or code_ava:
        print(f'{"1" if code_ava else "3"} url save :', url)
        cur.execute(f"""INSERT INTO worldpostalcode_new_links(continent, country, links, status) 
                        VALUES('{continent}', '{country}', '{url}', 'panding')""")

        if regions_ava:
            regious_list = dom.xpath(
                '//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]/a/@href')
            for reg in regious_list:
                link = first_url + reg
                rec(continent, country, link, cur)
    else:
        print('4 no code')


p2 = 1
for continant in continant_list:
    contry_list = continant.xpath('./div/a/@href')

    conti = continant.xpath('./preceding-sibling::h2//text()')

    for contry in contry_list:
        second_url = first_url + contry
        res2 = requests.get(second_url)
        dom2 = lxml.html.fromstring(res2.text)
        contry = str(contry).replace('/','').strip()
        print(contry, '\n')
        rec(conti[0], contry, second_url, cur)
        p2 += 1

conn.close()