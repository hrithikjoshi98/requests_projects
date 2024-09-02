import requests
import pymysql
import lxml.html

conn = pymysql.connect(
        host='localhost',
        user='root',
        password="root",
        db='casio',
        autocommit=True
    )
cur = conn.cursor()

my_pos = 1

cur.execute(f'''CREATE TABLE IF NOT EXISTS worldpostalcode_links(id int AUTO_INCREMENT PRIMARY KEY, continent varchar(
100), country varchar(100), 
links varchar(1000),
status varchar(50))''')

cur.execute(f'''CREATE TABLE IF NOT EXISTS worldpostalcode_data(id int AUTO_INCREMENT PRIMARY KEY,
url varchar(500), 
code_name_key varchar(300),
code varchar(100))''')


first_url = 'https://worldpostalcode.com'

res1 = requests.get(first_url)

dom1 = lxml.html.fromstring(res1.text)

continant_list = dom1.xpath('//div[@class="regions"]')

def scrape_postalcode(url, dom):
    list_of_code_names = dom.xpath('//div[contains(@class,"unit") and not(contains(@class,"noletters")) and not(contains(@class,"units"))]/descendant::div[contains(@class,"place")]')
    for code_name in list_of_code_names:
        code_name_key = ' '.join(code_name.xpath('.//text()'))
        list_of_code = code_name.xpath('./following-sibling::node()/span//text()')
        for code in list_of_code:
            print("Scraped", url, code_name_key, code)
            cur.execute(f"""INSERT INTO worldpostalcode_data(url, code_name_key, code) 
                                    VALUES(%s, %s, %s)""", (url, code_name_key, code))


def rec(continant, contry, url, cur):
    global my_pos
    try:
        res2 = requests.get(url)

        dom2 = lxml.html.fromstring(res2.text)
        regions_ava = dom2.xpath(
            '//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]')
        code_ava = dom2.xpath('//div[@class="codes"]')

        if regions_ava and code_ava:
            cur.execute(f"""SELECT links FROM worldpostalcode_links WHERE links = '{url}'""")
            if cur.fetchone() == None:
                print('1 url save :', url)
                scrape_postalcode(url, dom2)
                cur.execute(f"""INSERT INTO worldpostalcode_links(continent, country, links, status) 
                                        VALUES(%s, %s, %s, %s)""", (continant, contry, url, 'done'))
                regious_list = dom2.xpath(
                    '//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]/a/@href')

                for reg in regious_list:
                    link = first_url + reg
                    cur.execute(f"""SELECT links FROM worldpostalcode_links WHERE links = '{link}'""")
                    if cur.fetchone() == None:
                        rec(continant, contry, link, cur)
                    else:
                        print(f"{link} already exists")
            else:
                print(f"{url} already exists")
        elif regions_ava and code_ava == []:
            regious_list = dom2.xpath(
                '//h2[text()="Regions" and position() = 1]/following-sibling::div[@class="regions"][1]/a/@href')
            for reg in regious_list:
                link = first_url + reg
                cur.execute(f"""SELECT links FROM worldpostalcode_links WHERE links = '{link}'""")
                if cur.fetchone() == None:
                    rec(continant, contry, link, cur)
                else:
                    print(f"{my_pos} {link} already exists")
                    my_pos += 1
        elif regions_ava == [] and code_ava:
            cur.execute(f"""SELECT links FROM worldpostalcode_links WHERE links = '{url}'""")
            if cur.fetchone() == None:
                print('3 url save :', url)
                scrape_postalcode(url, dom2)
                cur.execute(f"""INSERT INTO worldpostalcode_links(continent, country, links, status) 
                        VALUES(%s, %s, %s, %s)""", (continant, contry, url, 'done'))

            else:
                print(f"{my_pos} {url} already exists")
                my_pos += 1
        elif regions_ava == [] and code_ava == []:
            print('4 no code')
    except Exception as e:
        print(str(e))
        print('-----------------')
        print('| Network Error |')
        print('-----------------')


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