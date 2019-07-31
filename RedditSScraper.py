import time
import json
import datetime
import requests
import threading
from random import randint
from dhooks import Webhook, Embed

def getProxies():
    proxy_list = []
    proxies = open('proxies.txt', 'r')
    for x in proxies:
        proxy = x.strip('\n')
        proxy_list.append(proxy)
    return proxy_list

def getCPost(name):
    proxy_list = getProxies()
    title_list = []
    url = ('https://www.reddit.com/r/{}/new/.json'.format(name))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    condition = True
    while condition == True:
        if len(proxy_list) > 0:
            try:
                x = randint(0 , (len(proxy_list) - 1))
                proxy = proxy_list[x]
                proxy_dict = {'http': ('http://{}'.format(proxy)), 'https': ('https://{}'.format(proxy))}
                page = requests.get(url, headers=headers, proxies=proxy_dict)
                titles = json.loads((page.text))['data']['children']
                data = (titles[0]['data'])
                title = (data['title'])
                title_list.append(title)
                condition = False
            except:
                print('Connection failed trying again...')
                time.sleep(20)
        else:
            try:
                page = requests.get(url, headers=headers)
                titles = json.loads((page.text))['data']['children']
                data = (titles[0]['data'])
                title = (data['title'])
                title_list.append(title)
                condition = False
            except:
                print('Connection failed trying again...')
                time.sleep(20)
    
    return title_list

def monitor(name):
    proxy_list = getProxies()
    title_list = getCPost(name)
    new_list = []

    wh_file = open('webhook.txt', 'r')
    wh_link = wh_file.readline().strip()
    wh_file.close()
    
    while True:
        print('Scraping {} subreddit$$'.format(name))
        if len(proxy_list) > 0:
            try:
                x = randint(0 , (len(proxy_list) - 1))
                proxy = proxy_list[x]
                proxy_dict = {'http': ('http://{}'.format(proxy)), 'https': ('https://{}'.format(proxy))}
                url = ('https://www.reddit.com/r/{}/new/.json'.format(name))
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
                page = requests.get(url, headers=headers, proxies=proxy_dict)
                titles = json.loads((page.text))['data']['children']
                data = (titles[0]['data'])
                title = (data['title'])
            except:
                print('Connection failed trying again...')
                time.sleep(20)
        else:
            try:
                url = ('https://www.reddit.com/r/{}/new/.json'.format(name))
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
                page = requests.get(url, headers=headers)
                titles = json.loads((page.text))['data']['children']
                data = (titles[0]['data'])
                title = (data['title'])
            except:
                print('Connection failed trying again...')
                time.sleep(20)

        if title not in new_list:
            new_list.append(title)

        if new_list != title_list:
            t = (list(set(new_list) - set(title_list)))
            t = ''.join(t)
            title_list.append(t)

            link = (data['url'])
            sub_name = (data['subreddit'])
            text = (data['selftext'])
            sus_count = (data['subreddit_subscribers'])

            hook = Webhook(wh_link)
            embed = Embed(description='***New post found!***', color=0x1e0f3, timestamp='now')
            image = ('https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwiM8aujr5XjAhXymOAKHRfiClYQjRx6BAgBEAU&url=%2Furl%3Fsa%3Di%26source%3Dimages%26cd%3D%26ved%3D%26url%3D%252Furl%253Fsa%253Di%2526source%253Dimages%2526cd%253D%2526ved%253D2ahUKEwj2m6-hr5XjAhVvdt8KHVRYA-cQjRx6BAgBEAU%2526url%253Dhttps%25253A%25252F%25252Fwww.wired.com%25252F2015%25252F07%25252Freddit-amageddon%25252F%2526psig%253DAOvVaw2U53l3kdn1OnhD0mVVclHq%2526ust%253D1562127151112687%26psig%3DAOvVaw2U53l3kdn1OnhD0mVVclHq%26ust%3D1562127151112687&psig=AOvVaw2U53l3kdn1OnhD0mVVclHq&ust=1562127151112687')
            embed.set_author(name='Reddit Scraper', icon_url=image)
            embed.add_field(name='Title', value=title)
            embed.add_field(name='Subreddit Name', value=sub_name)
            embed.add_field(name='Contained Text', value=text)
            embed.add_field(name='URL', value=link)
            embed.add_field(name='Suscribers', value=sus_count)
            embed.set_footer(text='Reddit Scraper', icon_url=image)
            try:
                hook.send(embed=embed)
                print('{} SENT MESSAGE*$'.format(datetime.datetime.now()))
            except:
                pass

        time.sleep(30)

print('Reddit Scraper 1.0')
choice = input('Enter any key to initialize scraper$* (Press \'Q\' to quit) ')
choice = (choice.lower())
if choice == ('q'):
    exit()

sub_reddits = []
subreddits_file = open('subreddits.txt', 'r')
for x in subreddits_file:
    x = x.strip('\n')
    sub_reddits.append(x)
subreddits_file.close()

for x in range(len(sub_reddits)):
    getProxies_thread = threading.Thread(target=getProxies, name=('Function 1 {} sub'.format(sub_reddits[x])))
    getCPost_threads = threading.Thread(target=getCPost, name=('Function 2 {} sub'.format(sub_reddits[x])), args=(sub_reddits[x],))
    monitor_threads = threading.Thread(target=monitor, name=('Function 3 {} sub'.format(sub_reddits[x])), args=(sub_reddits[x],))
    getProxies_thread.start()
    getCPost_threads.start()
    monitor_threads.start()
    print('Initialized {} subreddit thread$'.format(sub_reddits[x]))