import requests
import json
import pymysql


conn = pymysql.connect(
        host='localhost',
        user='root',
        password="actowiz",
        db='casio',
        autocommit=True
    )
cur = conn.cursor()

def my_print(*args):
    string = ""
    for i in args:
        string += str(i) + "\n"
    print(string, '\n')

# def insert_data(conn, sortby, i,sort_order):
def insert_data(conn, sortby, i):
    print(i)
    with conn.cursor() as cur:
        q3 = f"""INSERT INTO {sortby}(brandDisp, productName, dispPrice, price, image_url) VALUES(%s, %s,
        %s,%s,
        %s)"""
        tu = (i['brandDisp'], i['productName'], i['dispPrice'], i['sellingPrice'], i['image_url'])
        cur.execute(q3, tu)
        conn.commit()

cookies = {
    'AKA_A2': 'A',
    '_abck': 'E1ADE9974EF723510A6250EE03C18C13~0~YAAQvydzaOEUk5WRAQAATCIEnQz51+O673L8teMx90qytICAggxQxvQJeB0LYcU9JuS76sFZx4WY+lLh43IdPISUX6kpDO2HfK26Xf6HWMLJ8a905f7ZUeHvtvXwvSNcxzy2k6lInyCJlstdx/0tl8wlNbKkYa7ZUb3m19KZogHBql3NCYPKX6Mc3gwQWJY2U7saxjwutTTd74H1LEFrLDLNEN/Kehoba6mhS+mE5ooIArPlTIVXZORvD+D1tZmc0yAUFqFalPoY8u9mU+7LTKV9drlDuSST405k+LnyAjhZFiaOZKa8Lh0oC5UrV55fuBsLBkUdtpRIOYCDBlfR4TPlfHq5iwf5ek8jU6QEYUC5sq1Gvw92eH5lIrRZYQYhjWnOBouCOUNm/VwWEgdewxn0eYGA2PM=~-1~||0||~-1',
    'ak_bmsc': '1C1DB015CD44A205CD7DEDA0BA05028E~000000000000000000000000000000~YAAQvydzaDEVk5WRAQAA+CQEnRhmdSNu1Z0/+D023mbw+VF43dFnfVrCIUSy4Ni0LFoSv6ysN6do8Oi2zPhkZmD3syz3Xe9CQHvphogeUXSlRqyodTE/h/15StJrcLazVpjWczux9qQ50c1rVzRtsJYcPahCdOVjgrjilzaSGtr8jFhOxjDLwPEUmP5DSUu0h3w2mwHVzN1TYeQZFPjKX91Qheg2G2CelXVPhG76Kj86q4bNn4Xpzz5uQtsb1MpVegxsG1ZSydXfGIcWWcqowdmcTKImpKuQpXEQiQUX2lult0Ip004+A0ZIr0VvL7/qfa3TeFHw0MzAsi8Gt6IruzwPCZCtYOw4ES+3fUa/Fp3X2a37JgiaHcLvXAkmgWmzcJkEBomvD9p0iBWDnYtyaltMcI0EZaOyauPNhvDXwWdUgzGNBWqiqESrEgmqbr14YZBMBuSm+CGHtA==',
    's_fid': '39B9880172879534-06AC45DEC6BB08A9',
    's_vi': '[CS]v1|336810EBE339A75B-400013FCC00DFA31[CE]',
    'AMCV_21C233CF62178F4E0A495FDD%40AdobeOrg': '179643557%7CMCAID%7C336810EBE339A75B-400013FCC00DFA31%7CvVersion%7C5.5.0',
    '_ga_CCV1BS8RHC': 'GS1.2.1724916191.1.1.1724916191.0.0.0',
    's_sq': 'casiocomputer.gshock.jp.001%3D%2526c.%2526a.%2526activitymap.%2526page%253DG-SHOCK%252520Official%252520Website%252520%25257C%252520G-SHOCK%252520INDIA%2526link%253DVIEW%252520ALL%252520G-SHOCK%2526region%253Dcontainer-e257deed8d%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253DG-SHOCK%252520Official%252520Website%252520%25257C%252520G-SHOCK%252520INDIA%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.casio.com%25252Fin%25252Fwatches%25252Fgshock%25252F%2526ot%253DA',
    '_ga_DGD0L7D7HE': 'GS1.1.1724916190.1.1.1724916194.0.0.0',
    '_ga_8JQMSRZX23': 'GS1.1.1724916191.1.0.1724916194.0.0.0',
    '_fbp': 'fb.1.1724916256892.425998942162417987',
    'pr_visit': '1724916433',
    'bm_sz': 'EFF0E6C2C802B4803694934730CC9185~YAAQvydzaM2ak5WRAQAAUgwKnRiK8b45W3I6uBdf2jcvtkk6tCKWfxD+GUyXfKN/85aIQQoyl79DazjnwEolex0r/p5/5dGStrRul4W8zXlJfUKWIFZeyv8XHDp0i4zn4GAPPvYhVBWNcLXQ7dW8jxGjykvS1y9ZB5dqEBRf6QDpdTnWfJ67RjAGZqRNyIDLSyJDFJsBRJoLxS6zckG1NgjWM3zDpeTytvL18LZtWpUUr0feaK++onK8XbsC4jDi8VtxNCwZdS6VcIkLEOa7Ifuq+Pr/oL3humcL+/M/NN7KJdMHS+JBab/0qwhd8xhrBxbImPoqiLQ4gEUlEei/Ka5+t0Pr4z5Ax0Dc+Ln6O+pm9j9JyUrD+VQN0MgqPjQQ56CYRyQL8ISO4WTtJwlcmnhoc5GzryulMjfxQkKvo3NiGHAwJtRh85Z0Sayx~3486770~3224901',
    'RT': '"z=1&dm=casio.com&si=5e8dfcd6-4348-46b5-9b79-b8af6a44f392&ss=m0eyk0td&sl=4&tt=7n5&bcn=%2F%2F684d0d48.akstat.io%2F"',
    'AWSALB': 'mzbHBg8QLmDPCGabx5eK5RtpJCv5VIdVheMC0gesd0HPdsEZVz0WUibWMgA+Fp5yG3pCzsFc41quyi1F9RnGCzZUCEyFbXdnY5RB23g8KwvqCZ1yhlYEB0yDFO15',
    'AWSALBCORS': 'mzbHBg8QLmDPCGabx5eK5RtpJCv5VIdVheMC0gesd0HPdsEZVz0WUibWMgA+Fp5yG3pCzsFc41quyi1F9RnGCzZUCEyFbXdnY5RB23g8KwvqCZ1yhlYEB0yDFO15',
    'bm_sv': 'ABF47596B8CA4875BC5DF8D4B9C3967D~YAAQvydzaF6bk5WRAQAA7RQKnRiMHG7BqUF0GEVsOH8KTDxagBHGFwfnWwYUlvMeLtHzywNYuChXpl+IYtwwOO9fmWfbQ0Tbzf+J8xvU6ZWAP4PBVHleiVt4I4Gqq2TWL2prcMd8dgEzCOEluQtLpBworkuj4OoCx8nYCrOo1T3R/S2tJN2HwLhKqXZAZMgjGc4bbYn0ZWafGzxmD5s+RP3AoelwvGHkp9knpsRMt5kLbPoI+0jhCgJaWE+gZm9x~1',
}



headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache','pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.casio.com/in/watches/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

response = requests.get(
    'https://www.casio.com/content/casio/locales/in/en/products/watches/jcr:content/root/responsivegrid/container/product_panel_list_f.products.json',
    cookies=cookies,
    headers=headers,
)

watch_dict = json.loads(response.text)


li = []
main_dic = {}
for i in watch_dict['data']:
    temp_dic = {}
    try:
        image_url = 'https://www.casio.com' + i['productAssetList'][0]['path']
        temp_dic['image_url'] = image_url
    except:
        image_url = ''
        temp_dic['image_url'] = ''
    brandDisp = i['brandDisp']
    productName = i['productName']
    dispPrice = i['dispPrice']
    sellingPrice = i['salePrice']

    temp_dic['brandDisp'] = brandDisp
    temp_dic['productName'] = productName
    temp_dic['dispPrice'] = dispPrice
    temp_dic['sellingPrice'] = sellingPrice
    my_print(brandDisp, productName, dispPrice, sellingPrice, image_url)
    li.append(temp_dic)

main_dic['main'] = li

sort_list = ['hightolows', 'lowtohigns']


for sortby in sort_list:
    print(sortby)
    cur.execute(f'''CREATE TABLE IF NOT EXISTS {sortby}(image_url varchar(300), brandDisp varchar(100), productName 
    varchar(
        100) PRIMARY KEY
        ,dispPrice varchar(100), price int(24),sort_order int(23))''')
    conn.commit()

    if sortby == 'hightolows':
        d1 = {}
        newlist = sorted(main_dic['main'], key=lambda d: d['sellingPrice'], reverse=True)
        d1[sortby] = newlist
        # sort_order=0
        for i in d1[sortby]:
            my_print(i['brandDisp'], i['productName'], i['dispPrice'], i['sellingPrice'], i['image_url'])
            # sort_order+=1
            # insert_data(conn, sortby, i,sort_order)
            # insert_data(conn, sortby, i)
            q3 = f"""INSERT INTO {sortby}(brandDisp, productName, dispPrice, price, image_url) VALUES(%s, %s,
                    %s,%s,
                    %s)"""
            tu = (i['brandDisp'], i['productName'], i['dispPrice'], i['sellingPrice'], i['image_url'])
            print(i)
            print(tu)
            cur.execute(q3, tu)
            conn.commit()


    # elif sortby == 'lowtohigns':
    #     d2 = {}
    #     newlist = sorted(main_dic['main'], key=lambda d: d['sellingPrice'])
    #     d2[sortby] = newlist
    #     with open(sortby + '.json', 'w') as file:
    #         y = json.dumps(d2)
    #         print(y, '\n')
    #         file.write(y)
    #     for i in d2[sortby]:
    #         q3 = f"""INSERT INTO {sortby}(brandDisp, productName, dispPrice, price, image_url) VALUES('
    #         {i['brandDisp']}',
    #         '{i['productName']}', '{i['dispPrice']}', '{i['sellingPrice']}', '{i['image_url']}')"""
    #         cur.execute(q3)
    #         conn.commit()
    # elif sortby == 'newests':
    #     d3 = {}
    #     d3[sortby] = main_dic['main']
    #     with open(sortby + '.json', 'w') as file:
    #         y = json.dumps(d3)
    #         print(y, '\n')
    #         file.write(y)
    #     for i in d3[sortby]:
    #         q3 = f"""INSERT INTO {sortby}(brandDisp, productName, dispPrice, price, image_url) VALUES('
    #         {i['brandDisp']}',
    #         '{i['productName']}', '{i['dispPrice']}', '{i['sellingPrice']}', '{i['image_url']}')"""
    #         cur.execute(q3)
    #         conn.commit()




# conn.close()

