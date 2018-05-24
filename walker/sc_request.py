import urllib3
from bs4 import BeautifulSoup
import getpass
import os
import urllib3.exceptions as catch

class requester():
    def __init__(self,requestURL):
        self.proxies_ips = [
            "10.24.129.241:8080",
            "10.24.163.218:8080"
        ]
        self.login = os.getenv('username')
        print(self.login)
        self.passcode = getpass.getpass("Passcode: ")
        self.url = requestURL
        self.proxy_auth = '%(login)s:%(password)s' %{'login':self.login,'password':self.passcode}
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        self.proxy_header = urllib3.make_headers(proxy_basic_auth=self.proxy_auth)
        self.request_header = urllib3.make_headers(user_agent=self.user_agent)
        self.scheme = 'https' if self.url[:5]=='https' else 'http'
    def request(self,method):
        for ip in self.proxies_ips:
            print("TRYING IP %(ip)s" %{'ip':ip})
            proxy_str = '%(scheme)s://%(ip)s' %{"scheme":self.scheme,"ip":ip}
            print(proxy_str)
            proxy = urllib3.ProxyManager(proxy_str,timeout=10,proxy_headers=self.proxy_header,headers=self.request_header)
            try:
                print('TRYING')
                r = proxy.request(method,self.url)
                print(r.status)
                return r.data
            except catch.MaxRetryError as e:
                print(e)
            except catch.ProxyError as e:
                print(e)
def processLi(li,item):
    try:
        if not li.find('a') is None:
            a = li.find('a')
            item['name'] = a.contents[0]
            item['url'] = a['href']
        elif not li.find('i') is None:
            i = li.find('i')
            item['name'] = i.contents[0]
            item['url'] = ''
        else:
            item['name'] = li.contents[0]
            item['url']=''
        return item
    except AttributeError as e:
        print(e)

if __name__ == "__main__":
    data = requester('https://en.wikipedia.org/wiki/List_of_programs_broadcast_by_NBC').request('GET')
    soup = BeautifulSoup(data,'html.parser')
    [s.extract() for s in soup('sup')]
    cont = soup.find_all('div',attrs={'class':'mw-parser-output'})
    result =[]
    for c in cont:
        children = c.findChildren(recursive=False)
        for c in children:
            if c.name =='p' or c.has_attr('class'):
                pass
            elif c.name=='h2':
                status = c.find('span',attrs={'class':'mw-headline'})['id']
                print(status)
            elif c.name == 'h3':
                genre = c.find('span',attrs={'class':'mw-headline'})['id']
                print genre
            elif c.name == 'ul':
                for li in c.find_all('li',recursive=False):
                    if len(li.find_all('ul'))==0:
                        item = {'status':status,'genre':genre}
                        item = processLi(li,item)
                        print(item)
                    else:
                        for ul in li.find_all('ul'):
                            for subli in ul.find_all('li'):
                                item = {'status':status,'genre':genre}
                                item = processLi(subli,item)
                                print(item)
            print("--")