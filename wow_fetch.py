import urllib
from bs4 import BeautifulSoup as Bs


class Fetch:

    def __init__(self, servers_url, order_url, my_account):
        self.server_list_url = servers_url
        self.order_url = order_url
        self.my_account = my_account

    def fetch_order_info(self, realm_id, race_id):
        realm_url = self.order_url.format(realm_id, race_id)

        opener = urllib.request.build_opener()

        # cookie to have currencies in dollar
        opener.addheaders.append(
            ('Cookie', 'g2g_regional=%7B%22currency%22%3A%22USD%22%2C%22language%22%3A%22en%22%7D'))
        html = opener.open(realm_url)
        soup = Bs(html, features="html.parser")

        # price
        tag = soup.findAll("span", {"class": "products__exch-rate"}, limit=1)
        if tag is None:
            return 0
        tag = tag[0]
        value = str(tag.text).strip().replace(" ", "").replace('1Gold=', '').strip()
        cheapest_price = float(value.replace('US$', ''))

        # stock - total gold
        tag = soup.findAll("span", {"class": "products__statistic-amount"}, limit=1)
        if tag is None:
            return 0
        tag = tag[0]
        value = str(tag.text).strip().replace(" ", "").replace('Gold', '').strip()
        gold_stock = value

        # is seller my account
        tag = soup.findAll("a", {"class": "seller__name"}, limit=1)
        if tag is None:
            return 0
        tag = tag[0]
        value = str(tag.text).strip().replace(" ", "").strip()
        my_account = value == self.my_account

        return cheapest_price, gold_stock, my_account

    def fetch_realms_info(self):
        html = urllib.request.urlopen("https://www.g2g.com/wow-eu/gold-2522-19248")
        soup = Bs(html, features="html.parser")
        servers_id = [str(o['value']) for o in soup.find(id='server').find_all('option')]
        realms = [str(o.text) for o in soup.find(id='server').find_all('option')]
        return servers_id, realms
