import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from bs4 import element
import getpass
import os
import urllib3.exceptions as catch
import sqlite3
import hashlib
def get_passcode():
    return getpass.getpass("Passcode: ")

class Sql():
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'data.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()
    def create_table(self,values,tb_nm):
        columns = ''
        for key in values.keys():
            columns += '{0} {1},'.format(key,values[key])
        columns = columns[:-1]
        query = '''CREATE TABLE {0}({1})'''.format(tb_nm,columns)
        print(query)
        self.cur.execute(query)
        self.conn.commit()
        self.conn.close()
    def update_to_db(self,values,tb_name):
        columns = ', '.join(values.keys())
        placeholders = ', '.join('?' * len(values))
        sql = 'REPLACE INTO {} ({}) VALUES ({})'.format(tb_name,columns,placeholders)
        try:
            self.cur.execute(sql, values.values())
        except sqlite3.InterfaceError as e:
            print(e)
            print(values)
            print(type(values['name']))
        self.conn.commit()
        self.conn.close()
    def get_all_from_tb(self,tb_nm):
        self.cur.execute('''
            SELECT * from {}
        '''.format(tb_nm))
        return self.cur.fetchall()
def init_all_shows():
    map = {
        'key': 'text primary key',
        'status': 'text',
        'network': 'text',
        'url': 'text',
        'genre': 'text',
        'name':'text'
    }
    Sql().create_table(map,'all_shows')
def init_catelog():
    map = {
        'name': 'text primary key',
        'url': 'text'
    }
    Sql().create_table(map,'catelog')
class Requester():
    def __init__(self,requestURL,passcode):
        self.proxies_ips = [
            "10.24.129.241:8080",
            "10.24.163.218:8080"
        ]
        self.login = os.getenv('username')
        self.passcode = passcode
        self.url = requestURL
        self.proxy_auth = '%(login)s:%(password)s' %{'login':self.login,'password':self.passcode}
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36'
        self.proxy_header = urllib3.make_headers(proxy_basic_auth=self.proxy_auth)
        self.request_header = urllib3.make_headers(user_agent=self.user_agent)
        self.scheme = 'https' if self.url[:5]=='https' else 'http'
    def request(self,method):
        for ip in self.proxies_ips:
            proxy_str = '%(scheme)s://%(ip)s' %{"scheme":self.scheme,"ip":ip}
            proxy = urllib3.ProxyManager(proxy_str,timeout=10,proxy_headers=self.proxy_header,headers=self.request_header)
            try:
                r = proxy.request(method,self.url)
                return r.data
            except catch.MaxRetryError as e:
                print(e)
            except catch.ProxyError as e:
                print(e)
def process_catelog(seed,passcode):
    data = Requester(seed,passcode).request('GET')
    soup = BeautifulSoup(data,'html.parser')
    div = soup.find('div',attrs={'aria-labelledby':'Lists_of_TV_programs_broadcast_by_country'})
    th = [t for t in div.find_all('th') if t.contents[0]=='United States'][0]
    td = th.parent.find('td')
    lis = td.find_all('li')
    for li in lis:
        a = li.find('a')
        #if a.has_attr('class'):
        #    print(a['class'])
        if a.has_attr('href'):
            Sql().update_to_db({'url':a['href'],'name':a.contents[0]},'catelog')
        elif 'selflink' in a['class']:
            Sql().update_to_db({'url':seed,'name':a.contents[0]},'catelog')
        else:
            pass
def process_network(url,passcode,name):
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
                try:
                    item['name'] = li.contents[0]
                    item['url']=''
                except IndexError as e:
                    print(e)
                    print(li)
            try:
                item['key']=hashlib.md5(item['network'].encode('utf-8')+item['name'].encode('utf-8')).hexdigest()
                if type(item['name']) is element.Tag:
                    item['name'] = item['name'].contents[0]
                Sql().update_to_db(item,'all_shows')
            except UnicodeEncodeError as e:
                print(e)
                print(item['name'])
                print(item['network'])
            except KeyError as e:
                print(e)
            return item
        except AttributeError as e:
            print(e)
    print('process {}'.format(name.encode('utf-8')))
    data = Requester(url,passcode).request('GET')
    soup = BeautifulSoup(data,'html.parser')
    [s.extract() for s in soup('sup')]
    cont = soup.find_all('div',attrs={'class':'mw-parser-output'})
    genre = ''
    for c in cont:
        children = c.findChildren(recursive=False)
        for c in children:
            if c.name =='p' or c.has_attr('class'):
                pass
            elif c.name=='h2':
                status = c.find('span',attrs={'class':'mw-headline'})['id']
            elif c.name == 'h3':
                genre = c.find('span',attrs={'class':'mw-headline'})['id']
            elif c.name == 'ul':
                for li in c.find_all('li',recursive=False):
                    if len(li.find_all('ul'))==0:
                        if li.has_attr('class'):
                            if not 'mw-empty-elt' in li['class']:
                                item = {'status':status,'genre':genre,'network':name}
                                item = processLi(li,item)
                        else:
                            item = {'status':status,'genre':genre,'network':name}
                            item = processLi(li,item)
                    else:
                        for ul in li.find_all('ul'):
                            for subli in ul.find_all('li'):
                                item = {'status':status,'genre':genre,'network':name}
                                item = processLi(subli,item)
def process_all(passcode):
    head = 'https://en.wikipedia.org'
    catelog = Sql().get_all_from_tb('catelog')
    for item in catelog:
        url = item[0]
        name = item[1]
        if url[:len(head)]!=head:
            url = head + url
        process_network(url,passcode,name)
if __name__ == "__main__":
    #init_catelog()
    passcode = get_passcode()
    process_catelog('https://en.wikipedia.org/wiki/List_of_programs_broadcast_by_NBC',passcode)
    process_all(passcode)


    