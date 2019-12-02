import operator


class OrderRecord:
    RACES = ['AL', 'HO']
    G2G_FEE = 0
    PAYPAL_FEE = 0
    WITHDRAW_FEE = 0
    DOLLAR_EXCHANGE = 0

    def __init__(self):
        self.realm_name = ""
        self.server_price = 0
        self.race = OrderRecord.RACES[0]
        self.price_toman = 0
        self.is_my_account = False
        self.gold_stock = 0

    def is_alliance(self):
        return self.race == OrderRecord.RACES[0]

    def set_alliance(self, value: bool):
        self.race = OrderRecord.RACES[0] if value else OrderRecord.RACES[1]

    def calculate_price_toman(self, interest_rate: int):
        self.price_toman = \
            (self.server_price * 1000 *
             (100 - OrderRecord.G2G_FEE) / 100 *
             (100 - OrderRecord.PAYPAL_FEE) / 100 - OrderRecord.WITHDRAW_FEE) * \
            OrderRecord.DOLLAR_EXCHANGE * \
            (100 - interest_rate) / 100 \
            / 1000
        return self.price_toman

    def __gt__(self, other):
        return self.price_toman < other.price_toman

    def print_order(self, big_width, medium_width, small_width):
        print("{}{}{}{}{}{}"
              .format(self.realm_name.ljust(big_width),
                      self.race.ljust(small_width),
                      str(self.gold_stock).ljust(medium_width),
                      str(self.server_price).ljust(medium_width),
                      str(format(self.price_toman, ",.0f")).ljust(medium_width),
                      ('*' if self.is_my_account else '').ljust(small_width)))

    @staticmethod
    def __print_order_titles(big_width, medium_width, small_width):
        print("Realm".ljust(big_width) +
              "Race".ljust(small_width) +
              "Gold Stock".ljust(medium_width) +
              "Price($)".ljust(medium_width) +
              "Buy(Toman)".ljust(medium_width) +
              "My".ljust(small_width))

    @staticmethod
    def print_orders(wow_record_list: list):
        big_width = 40
        medium_width = 15
        small_width = 8

        OrderRecord.__print_order_titles(big_width, medium_width, small_width)
        for rec in wow_record_list:
            rec.print_order(big_width, medium_width, small_width)

    @staticmethod
    def calculate_orders_price(wow_record_list: list, interest_rate: int):
        for rec in wow_record_list:
            rec.calculate_price_toman(interest_rate)
