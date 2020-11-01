from wow_classic_fetch import WowClassicFetch


class WowNormalFetch(WowClassicFetch):
    __WOW_REALM = [
        'Silvermoon [EU]',
        'Argent Dawn [EU]',
        'Dentarg [EU]',
        'Draenor [EU]',
        'Kazzak [EU]',
        'Ragnaros [EU]',
        'Ravencrest [EU]',
        'Tarren Mill [EU]',
        'Twisting Nether [EU]'
    ]

    def get_servers_url(self):
        return "https://www.g2g.com/wow-eu/gold-2522-19248"

    def get_order_url(self):
        return "https://www.g2g.com/wow-eu/gold-2522-19248?server={}&faction={}&sorting=price@asc"

    def get_alliance_id(self):
        return 1086

    def get_horde_id(self):
        return 1087

    def get_realms_name(self):
        return WowNormalFetch.__WOW_REALM

    def is_keyword_include(self):
        return False

    def should_process(self, realm: str):
        return realm in WowNormalFetch.__WOW_REALM
