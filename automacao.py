import requests
from bs4 import BeautifulSoup

directory = str(input("Directory: "))
search = str(input("What images do you want to dowload? "))
search_mod = search.upper()
num_of_img = int(input("How many images you want to dowload "))
search_mod = search_mod.split()

#Primeira iagem do google imagens
url1 = f'https://www.google.com/search?q={search}&hl=pt-BR&gbv=1&source=lnms&tbm=isch&sa=X&ved=2ahUKEwipwcKTxOfrAhUUDrkGHZ3kB5kQ_AUoAXoECB8QAw&sfr=gws&sei=g8xeX6WWO4KI5OUP1Ne2sAQ'
i_order_image = 0 

response =requests.get(url1)
soup = BeautifulSoup(response.text, 'html.parser')

links_list = []
repeat_img = []

table = soup.find_all('table', attrs={'class':'RntSmf'})

for links in table:
    links_list.append(links.a.get('href'))

links_list = [sites[7:sites.index('&')] for sites in links_list]

for link in links_list:
    if i_order_image == num_of_img:
        break
    try:
        url = link
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        images = soup.find_all('img')

        for image in images:
            if i_order_image == num_of_img:
                break
            if '.svg' in image.get('src') or image.get('src')==None:
                pass
            if image.get('sc') in repeat_img:
                pass
            search_comp = [i in image.get ('src').upper() for i in search_mod ]
            if search_comp.count(True) == len(search_comp) and 'http' in image.get('src'):
                with open(f'{directory}/{search.lower()}_{i_order_image}.png', 'wb') as f:
                    img_response = requests.get(image.get('src'))
                    if img_response.status_code == 200: #sucess
                        if i_order_image == num_of_img:
                            break
                        else:
                            repeat_img.append(image.get('src'))
                            print(image.get('src'), '-', i_order_image)
                            f.write(img_response.content)
                            i_order_image+=1
    except:
        pass