import urllib.request
from bs4 import BeautifulSoup as Bs

# change here
from pip._vendor.distlib.compat import raw_input

DOLLAR_EXCHANGE = 12550
EURO_EXCHANGE = 13750

G2G_FEE = 9.99
PAYPAL_FEE = 3.99
WITHDRAW_FEE = 0.99
EURO_DOLLAR = 1.10109923

REALM_URL_TEMPLATE = "https://www.g2g.com/wow-eu/gold-2522-19248?server={}&faction={}&sorting=price@asc"
ALLIANCE_ID = 1086
HORDE_ID = 1087
RACES_ID = [ALLIANCE_ID, HORDE_ID]
RACES = ['AL', 'HO']
DOLLAR = '$'
EURO = '€'
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


def fetch_cheapest_price(realm_id, race_id):
    realm_url = REALM_URL_TEMPLATE.format(realm_id, race_id)
    html = urllib.request.urlopen(realm_url)
    soup = Bs(html, features="html.parser")
    cheapest_price_tag = soup.findAll("span", {"class": "products__exch-rate"}, limit=1)

    if cheapest_price_tag is None:
        return DOLLAR, 0
    cheapest_price_tag = cheapest_price_tag[0]

    value = str(cheapest_price_tag.text).strip().replace(" ", "").replace('1Gold=', '').strip()

    curr = DOLLAR
    if value.find('EUR'):
        curr = EURO

    cheapest_price = float(value.replace('EUR', ''))

    return curr, cheapest_price


def calculate_sell_price(currency, price, interest_rate):
    # =(I2*1000*(100 - g2g_fee)/100*(100-paypal)/100-withdraw)*exchange_rate*(100-interest_fee)/100/1000
    if currency == EURO:
        price = price * EURO_DOLLAR

    return (price * 1000 * (100 - G2G_FEE) / 100 * (100 - PAYPAL_FEE) / 100 - WITHDRAW_FEE) * DOLLAR_EXCHANGE * (
                100 - interest_rate) / 100 / 1000


def print_table(currency, realms, realms_price, interest_rate):
    print("Realm".ljust(max_width) + "Race\tPrice($)\tBuy(Toman)")
    j = 0
    for i in range(len(realms_price)):
        sell_price = calculate_sell_price(currency, realms_price[i], interest_rate)
        print("{}{}\t{}\t{}".format(realms[j].ljust(max_width), RACES[i % 2], realms_price[i], format(sell_price, ",.0f")))

        if i % 2 == 1:
            j += 1
# end


if __name__ == "__main__":
    Html = urllib.request.urlopen("https://www.g2g.com/wow-eu/gold-2522-19248")
    Soup = Bs(Html, features="html.parser")
    servers_id = [str(o['value']) for o in Soup.find(id='server').find_all('option')]
    Realms = [str(o.text) for o in Soup.find(id='server').find_all('option')]

    max_width = max(len(rl) for rl in Realms)

    Currency = ''
    Realms_Price = []
    for index in range(len(servers_id)):
        realmId = servers_id[index]

        if realmId.lower() == 'all':
            continue

        if Realms[index] not in DESIRED_REALM:
            continue

        print(Realms[index] + ',', end='')
        for raceId in RACES_ID:
            Currency, server_price = fetch_cheapest_price(realmId, raceId)
            Realms_Price.append(server_price)
    # end for

    print("")
    while True:
        rate = raw_input("Interest Rate %: ")
        if rate == 'q':
            break

        print_table(Currency, DESIRED_REALM, Realms_Price, int(rate))
    # end loop

# end if
