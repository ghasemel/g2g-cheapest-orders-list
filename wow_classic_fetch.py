from wow_fetch import WowFetch


class WowClassicFetch(WowFetch):
    __WOW_REALM = [        
        'Ashbringer [EU]',
        'Bloodfang [EU]',
        'Dragonfang [EU]',
        'Dreadmist [EU]',
        'Firemaw [EU]',
        'Flamelash [EU]',
        'Gandling [EU]',
        'Gehennas [EU]',
        'Golemagg [EU]',
        'Judgement [EU]',
        'Mograine [EU]',
        'Noggenfogger [EU]',
        'Razorgore [EU]',
        'Shazzrah [EU]',
        'Skullflame [EU]',
        'Stonespine [EU]',
        'Ten Storms [EU]'
    ]

    def get_servers_url(self):
        return "https://www.g2g.com/wow-classic-eu/gold-27815-27817"

    def get_order_url(self):
        return "https://www.g2g.com/wow-classic-eu/gold-27815-27817?server={}&faction={}&sorting=price@asc"

    def get_my_account(self):
        return "gigold"

    def get_alliance_id(self):
        return 33738

    def get_horde_id(self):
        return 33739

    def get_realms_name(self):
        return WowClassicFetch.__WOW_REALM

    def get_keyword(self):
        return "[EU]"

    def is_keyword_include(self):
        return True

    def should_process(self, realm: str):
        #return realm in WowClassicFetch.__WOW_REALM
        return realm.find(self.get_keyword()) != -1





