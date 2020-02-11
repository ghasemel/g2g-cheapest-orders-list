from wow_classic_fetch import WowClassicFetch


class WowNormalFetch(WowClassicFetch):
    __WOW_REALM = [
        'Silvermoon',
        'Argent Dawn',
        'Dentarg',
        'Draenor',
        'Kazzak',
        'Ragnaros',
        'Ravencrest',
        'Tarren Mill',
        'Twisting Nether'
    ]

    def get_realms_name(self):
        return WowNormalFetch.__WOW_REALM

    def is_keyword_include(self):
        return False

    def should_process(self, realm: str):
        return realm in WowNormalFetch.__WOW_REALM
