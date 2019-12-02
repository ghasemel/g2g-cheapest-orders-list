from wow_fetch import WowFetch


class WowClassicFetch(WowFetch):
    __WOW_CLASSIC_REALM = [
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

    def get_servers_url(self):
        return "https://www.g2g.com/wow-eu/gold-2522-19248"

    def get_order_url(self):
        return "https://www.g2g.com/wow-eu/gold-2522-19248?server={}&faction={}&sorting=price@asc"

    def get_my_account(self):
        return "gigold"

    def get_alliance_id(self):
        return 1086

    def get_horde_id(self):
        return 1087

    def get_realms_name(self):
        return WowClassicFetch.__WOW_CLASSIC_REALM
