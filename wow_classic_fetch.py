from wow_fetch import WowFetch


class WowClassicFetch(WowFetch):
    __WOW_REALM = [
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
        return "https://www.g2g.com/wow-classic-eu/gold-27815-27817"

    def get_order_url(self):
        return "https://www.g2g.com/wow-classic-eu/gold-27815-27817?server={}&faction={}&sorting=price@asc"

    def get_my_account(self):
        return "gigold"

    def get_alliance_id(self):
        return 1086

    def get_horde_id(self):
        return 1087

    def get_realms_name(self):
        return WowClassicFetch.__WOW_REALM

    def get_keyword(self):
        return "Classic"

    def is_keyword_include(self):
        return True

    def should_process(self, realm: str):
        #return realm in WowClassicFetch.__WOW_REALM
        return realm.find(self.get_keyword()) != -1





