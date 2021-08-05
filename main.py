from PyPtt import PTT
from datetime import datetime
from getpass import getpass
import yaml
import os

targetWord = ['[發錢]', '(發錢)', '（發錢）', '發錢！']

loginId = ''
loginPw = ''

if __name__ == "__main__":
    bot = PTT.API()

    # 載入儲存的帳號密碼
    if (os.path.isfile('loginInfo.yaml')):
        with open('loginInfo.yaml', 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            loginId = data['id']
            loginPw = data['passwd']

    # 要求輸入帳號密碼
    if (loginId == '' or loginPw == ''):
        while True:
            try:
                loginId = input('輸入PTT ID:')
                loginPw = getpass('輸入PTT密碼:')
                bot.login(loginId, loginPw)
            except PTT.exceptions.LoginError:
                print('帳號或密碼錯誤，請重新輸入')
                pass
            else:
                if (input('是否儲存登入資訊（不安全，建議不要）?(no):') in ['yes', 'Yes', 'Y', 'y']):
                    print('儲存登入資訊到 loginInfo.yaml')
                    with open('loginInfo.yaml', 'w', encoding='utf-8') as f:
                        yaml.dump({
                            'id': loginId,
                            'passwd': loginPw
                        }, f)
                break

    bot.login(loginId, loginPw)

    lastSearch = bot.get_newest_index(PTT.data_type.index_type.BBS, 'Gossiping')
    pushedAid = []
    while (True):
        try:
            newestIndex = bot.get_newest_index(PTT.data_type.index_type.BBS, 'Gossiping')
            curIndex = newestIndex
            if (newestIndex < 100000):
                continue
            while (True):
                if (curIndex <= lastSearch):
                    break
                curPost = bot.get_post("Gossiping", post_index=curIndex, query=True)
                print(curIndex, lastSearch, '上次更新：', datetime.now().strftime('%m%d %H:%M:%S'), curPost.title)
                if (curPost.title):
                    for w in targetWord:
                        if (w in curPost.title and curPost.aid not in pushedAid and 'Re:' not in curPost.title):
                            bot.push('Gossiping', push_type=PTT.data_type.push_type.PUSH, push_content="錢", post_aid=curPost.aid)
                            print('要錢')
                            pushedAid.append(curPost.aid)
                curIndex += -1
            lastSearch = newestIndex
        except Exception as E:
            print(E)
            bot.logout()
            while (True):
                try:
                    bot.login(loginId, loginPw)
                except Exception as E2:
                    continue
                else:
                    break
            pass

    bot.logout()

    pass
