
import telegram
from bs4 import BeautifulSoup
import requests
from urllib import parse
import os
from collections import OrderedDict #중복제거
import time

#개드립 - 개드립 크롤링
#개드립에 올라간 글 60초마다 체크 새글 올라오면 알려줌
#참고 : https://blog.naver.com/popqser2/221426114267

my_token = '651790947:AAHh2V4gYHbGcg8Z_-die2d9Jl246TCyD1Q'


#bot = telegram.Bot(token  = my_token)
#print('start telegram bot')

#bot.sendMessage(chat_id='794650933',text="i'm bot")

#chat_id = bot.getUpdates()[-1].message.chat.id # 마지막으로 봇한테 메시지 날린사람

def site_on(): #글 목록 크롤링

    mURL = "https://www.dogdrip.net/dogdrip"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }

    list_link = []

    mTemp = requests.get(mURL, timeout=60, allow_redirects=False, headers=headers)
    mheader = mTemp.headers
    msoup = BeautifulSoup(mTemp.text, 'html.parser')

    title_link = msoup.find('div',{'class': 'ed board-list'}).find('table',{'class': 'ed table table-divider'}).find('tbody').find_all('tr')
    aa = range(20)
    for i in aa:
        title_link1 = title_link[i].find('td',{'class':'title'}).find('a')
        #print(title1['href'])
        list2 = list_link.append(title_link1['href']) #href로 자른 링크를 저장
        #print(list2)

    #print(list_link)
    #list_link = list(OrderedDict.fromkeys(list_link))#중복제거
    compare(list_link)#일단 이렇게하니까 됨.... list2는 무서워서 안써봄
    #compare(list2)
#    for link in title.find_all('a', href = True):
#        title_link = link['href']
#        list_link.append(title_link)
#    compare(list_link)

def compare(list_link): #목록 txt파일에 쓰기
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))#현재 파이썬 파일이 있는 폴더
    #print(BASE_DIR) #저장위치 확인
    temp = []
    cnt = 0
    with open(os.path.join(BASE_DIR, 'compare.txt'), 'r') as f_read: #compare.txt 열기
        before = f_read.readlines() #개행을 구분해서 읽음
        before = [line.rstrip() for line in before] #리스트를 \n로 쪼갬

        f_read.close()
        for i in list_link: #크롤링 값 list_link를 하나씩 읽음
            if i not in before: #before 리스트에 있는 링크 값에 list_link가 있는지 확인
                temp.append(i)#없으면 temp에 추가
                cnt = cnt + 1    # cnt값 +1
                with open(os.path.join(BASE_DIR, 'compare.txt'), 'a') as f_write:
                    f_write.write(i+'\n') #list_link주소를 compare.txt에 추가
                    f_write.close()
        if cnt > 0: #cnt가 1이라도 증가하면 새로운글 있음
            main_show(temp,cnt)

def main_show(temp, cnt):
    bot = telegram.Bot(token  = my_token)
    print('bot 실행')
    chat_id = bot.getUpdates()[-1].message.chat.id # 마지막으로 봇한테 메시지 날린사람
    NEW = "[+] 개드립 새로운 글은 {}개 입니다.".format(cnt)
    bot.sendMessage(chat_id = chat_id, text = NEW)
    for n in temp:
        Main_URL = n.strip()

        #####링크 제목 크롤링#####
        response = requests.get(Main_URL)
        html = response.text
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('div',{'class':'ed article-head margin-bottom-large'}).find('h4',{'class':'ed margin-bottom-xsmall'}).find('a')

        bot.sendMessage(chat_id=chat_id, text=title.text.strip()+'\n'+Main_URL)

while True:
    if __name__ == "__main__":
        site_on()
    time.sleep(60) #while문이 60초마다 한번씩 돌아감 새로고침 시간설정
