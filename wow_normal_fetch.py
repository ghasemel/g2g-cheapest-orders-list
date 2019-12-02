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
