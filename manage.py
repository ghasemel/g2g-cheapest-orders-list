from wow_classic_fetch import WowClassicFetch


def start():
    wow_classic = WowClassicFetch()
    wow_classic_orders = wow_classic.fetch_orders()
    return True


if __name__ == "__main__":
    result = start()
    assert result == True
    0
# end if
