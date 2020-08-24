import ssl
import urllib.request
from abc import ABC
from bs4 import BeautifulSoup as Bs
from calculate_price import OrderRecord


class WowFetch(ABC):

    MAX_FETCH = 20
    MIN_GOLD_STOCK = 300

    def get_servers_url(self):
        pass

    def get_order_url(self):
        pass

    def get_my_account(self):
        pass

    def get_alliance_id(self):
        pass

    def get_horde_id(self):
        pass

    def get_realms_name(self):
        pass

    def get_keyword(self):
        return ""

    def is_keyword_include(self):
        pass

    def get_batch_size(self):
        pass

    def should_process(self, realm: str):
        return False

    def fetch_orders(self):
        soup = self.__fetch_realms_info()
        realms_id, realms_name = self.__process_realms_info(soup)
        #print(realms_name)

        races_ids = [self.get_alliance_id(), self.get_horde_id()]

        order_list = list()
        for index in range(len(realms_id)):
            realm_id = realms_id[index]

            if realm_id.lower() == 'all':
                continue

            if not self.should_process(realms_name[index]):
                continue

            print(realms_name[index] + ',', end='')
            for raceId in races_ids:
                order_record = OrderRecord()
                order_record.realm_name = realms_name[index]

                soup = self.__fetch_order_info(realm_id, raceId)
                cheapest_price, gold_stock, my_account = self.__process_order_info(soup)

                order_record.server_price = cheapest_price
                order_record.gold_stock = gold_stock
                order_record.is_my_account = my_account
                order_record.set_alliance(raceId == self.get_alliance_id())

                order_list.append(order_record)
            # end for
        # end for
        return order_list
    # end

    def __process_order_info(self, soup):
        #print(soup)

        desired_index = -1

        gold_stock = 0

        # stock - total gold
        tag = soup.findAll("span", {"class": "products__statistic-amount"}, limit=WowFetch.MAX_FETCH)
        #print('raouf')
        #print(len(tag))

        for t in range(len(tag)):
            value = str(tag[t].text).strip().replace(" ", "").replace('Gold', '').strip().replace(',', '')
            gold_stock = float(value)
            if gold_stock >= WowFetch.MIN_GOLD_STOCK or t == WowFetch.MAX_FETCH - 1:
                desired_index = t
                break

        if desired_index < 0:
            return 0, 0, 0

        # price
        tag = soup.findAll("span", {"class": "products__exch-rate"}, limit=WowFetch.MAX_FETCH)
        if tag is None:
            return 0

        tag = tag[desired_index]
        value = str(tag.text).strip().replace(" ", "").replace('1Gold=', '').strip()
        cheapest_price = float(value.replace('US$', ''))

        # is seller my account
        tag = soup.findAll("a", {"class": "seller__name"}, limit=WowFetch.MAX_FETCH)
        if tag is None:
            return 0

        tag = tag[desired_index]
        value = str(tag.text).strip().replace(" ", "").strip()
        my_account = value == self.get_my_account()

        return cheapest_price, gold_stock, my_account

    def __fetch_order_info(self, realm_id, race_id):
        realm_url = self.get_order_url().format(realm_id, race_id)

        context=ssl._create_unverified_context()
        sslHandler = urllib.request.HTTPSHandler(context=context)

        opener = urllib.request.build_opener(sslHandler)

        # cookie to have currencies in dollar
        opener.addheaders.append(('Cookie', 'g2g_regional=%7B%22currency%22%3A%22USD%22%2C%22language%22%3A%22en%22%7D'))
        html = opener.open(realm_url)
        soup = Bs(html, features="html.parser")

        return soup

    @staticmethod
    def __process_realms_info(soup):
        realms_id = [str(o['value']) for o in soup.find(id='server').find_all('option')]
        realms_name = [str(o.text) for o in soup.find(id='server').find_all('option')]
        return realms_id, realms_name

    def __fetch_realms_info(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        html = urllib.request.urlopen(self.get_servers_url(), context=ctx)
        soup = Bs(html, features="html.parser")

        return soup

