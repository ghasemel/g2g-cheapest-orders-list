# change here
from pip._vendor.distlib.compat import raw_input
from calculate_price import OrderRecord

# fees
from wow_classic_fetch import WowClassicFetch
from wow_normal_fetch import WowNormalFetch

G2G_FEE = 8.99
PAYPAL_FEE = 3.99
WITHDRAW_FEE = 0.99


def calculate_price_list(orders_list: list, interest_rate, dollar_exchange_rate, price_per):
    OrderRecord.calculate_orders_price(
        orders_list,
        float(interest_rate),
        G2G_FEE,
        PAYPAL_FEE,
        WITHDRAW_FEE,
        float(dollar_exchange_rate),
        price_per
    )
    orders_list.sort()


def print_list(order_list: list):
    OrderRecord.print_orders(order_list)


def start():
    wow_norm = WowNormalFetch()
    wow_norm_orders = wow_norm.fetch_orders()

    print("\n===================================")
    while True:
        interest_rate = raw_input("Enter Interest Rate % (q): ")
        if interest_rate == 'q':
            break

        if interest_rate == '':
            continue

        dollar_exchange_rate = raw_input("Enter dollar exchange rate (to destination currency): ")

        calculate_price_list(wow_norm_orders, interest_rate, dollar_exchange_rate, 1000000)
        print_list(wow_norm_orders)

    # end loop


if __name__ == "__main__":
    start()
# end if
