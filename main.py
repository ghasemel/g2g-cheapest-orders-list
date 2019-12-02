import operator
import urllib.request
from bs4 import BeautifulSoup as Bs

# change here
from pip._vendor.distlib.compat import raw_input

from order_record import OrderRecord

# exchange rates
DOLLAR_EXCHANGE = 12550

# fees
G2G_FEE = 9.99
PAYPAL_FEE = 3.99
WITHDRAW_FEE = 0.99


REALM_URL_TEMPLATE = "https://www.g2g.com/wow-eu/gold-2522-19248?server={}&faction={}&sorting=price@asc"
ALLIANCE_ID = 1086
HORDE_ID = 1087
RACES_ID = [ALLIANCE_ID, HORDE_ID]

USER_ACCOUNT = 'gigold'

DESIRED_REALM = [
    'Classic - Ashbringer',
    'Classic - Bloodfang',
    'Classic - Dragonfang',
    'Classic - Dreadmist',
    'Classic - Firemaw',
    'Classic - Flamelash',
    'Classic - Gandling',
    'Classic - Gehennas',
    'Classic - Golemagg',
    'Classic - Judgement',
    'Classic - Mograine',
    'Classic - Noggenfogger',
    'Classic - Razorgore',
    'Classic - Shazzrah',
    'Classic - Skullflame',
    'Classic - Stonespine',
    'Classic - Ten Storms'
]


def fetch_order_info(realm_id, race_id):
    realm_url = REALM_URL_TEMPLATE.format(realm_id, race_id)

    opener = urllib.request.build_opener()

    # cookie to have currencies in dollar
    opener.addheaders.append(('Cookie', 'g2g_regional=%7B%22currency%22%3A%22USD%22%2C%22language%22%3A%22en%22%7D'))
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
    my_account = value == USER_ACCOUNT

    return cheapest_price, gold_stock, my_account


def fetch_realms_info():
    html = urllib.request.urlopen("https://www.g2g.com/wow-eu/gold-2522-19248")
    soup = Bs(html, features="html.parser")
    servers_id = [str(o['value']) for o in soup.find(id='server').find_all('option')]
    realms = [str(o.text) for o in soup.find(id='server').find_all('option')]
    return servers_id, realms


if __name__ == "__main__":

    OrderRecord.G2G_FEE = G2G_FEE
    OrderRecord.PAYPAL_FEE = PAYPAL_FEE
    OrderRecord.WITHDRAW_FEE = WITHDRAW_FEE
    OrderRecord.DOLLAR_EXCHANGE = DOLLAR_EXCHANGE

    Servers_id, Realms = fetch_realms_info()
    OrderList = list()
    for index in range(len(Servers_id)):
        realmId = Servers_id[index]

        if realmId.lower() == 'all':
            continue

        if Realms[index] not in DESIRED_REALM:
            continue

        print(Realms[index] + ',', end='')
        for raceId in RACES_ID:
            order_record = OrderRecord()
            order_record.realm_name = Realms[index]

            Cheapest_price, Gold_stock, My_account = fetch_order_info(realmId, raceId)

            order_record.server_price = Cheapest_price
            order_record.gold_stock = Gold_stock
            order_record.is_my_account = My_account
            order_record.set_alliance(raceId == ALLIANCE_ID)

            OrderList.append(order_record)
        # end for
    # end for

    print("")
    while True:
        rate = raw_input("Enter Interest Rate % (q): ")
        if rate == 'q':
            break

        if rate == '':
            continue

        OrderRecord.calculate_orders_price(OrderList, int(rate))
        OrderList.sort()
        OrderRecord.print_orders(OrderList)
    # end loop

# end if
