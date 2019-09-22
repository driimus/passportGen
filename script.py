import os
import json
from urllib.parse import quote

# NOTE: Based on the Telegram Passport JavaScript SDK, available at:
#       https://github.com/TelegramMessenger/TGPassportJsSDK


SCOPE_ALIASES = {
    'personal_details': 'pd',
    'passport': 'pp',
    'driver_license': 'dl',
    'identity_card': 'ic',
    'internal_passport': 'ip',
    'id_document': 'idd',
    'address': 'ad',
    'utility_bill': 'ub',
    'bank_statement': 'bs',
    'rental_agreement': 'ra',
    'passport_registration': 'pr',
    'temporary_registration': 'tr',
    'address_document': 'add',
    'phone_number': 'pn',
    'email': 'em',
}


def packScope(scope):
    if scope['data']:
        scope['d'] = scope.pop('data')
    if not scope['d']:
        # TO-DO: Implement error handler
        # throw new Error('scope data is required');
        pass
    if not scope['v']:
        # TO-DO: Implement error handler
        # throw new Error('scope version is required');
        pass
    for i in range(len(scope['d'])):
        scope['d'][i] = packScopeField(scope['d'][i])
    return json.dumps(scope)


def packScopeField(field):
    if isinstance(field, dict):
        if field['one_of']:
            field['_'] = field.pop('one_of')
        elif field['type']:
            field['_'] = field.pop('type')
        if isinstance(field['_'], list):
            for f in field['_']:
                f = packScopeField(f)
            field = packScopeOpts(field)
        elif field['_']:
            if SCOPE_ALIASES[field['_']]:
                field['_'] = SCOPE_ALIASES[field['_']]
            field = packScopeOpts(field)
    elif SCOPE_ALIASES[field]:
        field = SCOPE_ALIASES[field]
    return field


def packScopeOpts(scope):
    if 'selfie' in scope.keys():
        scope['s'] = 1
        scope.pop('selfie')
    if 'translation' in scope.keys():
        scope['t'] = 1
        scope.pop('translation')
    if 'native_names' in scope.keys():
        scope['n'] = 1
        scope.pop('native_names')
    return scope


def main():
    with open('config.json') as cfg:
        config = json.load(cfg)

    PASSPORT_OPTIONS = {
        "bot_id": config['bot_id'],
        "scope": {
            "data": config['requested_data'],
            "v": 1
        },
        "public_key": config['public_key'],
        "nonce": "".join("%02x" % x for x in os.urandom(8)),
        "callback_url": f'tg://resolve?domain={config["bot_username"]}'
    }

    url = (
        'tg://resolve?domain=telegrampassport'
        f'&bot_id={quote(PASSPORT_OPTIONS["bot_id"], safe="")}'
        f'&scope={quote(packScope(PASSPORT_OPTIONS["scope"]), safe="")}'
        f'&public_key={quote(PASSPORT_OPTIONS["public_key"], safe="")}'
        f'&nonce={quote(PASSPORT_OPTIONS["nonce"], safe="")}'
        f'&callback_url={quote(PASSPORT_OPTIONS["callback_url"])}'
        f'&payload=nonce'
    )

    # unencoded_url = (
    #     'tg://resolve?domain=telegrampassport'
    #     f'&bot_id={PASSPORT_OPTIONS["bot_id"]}'
    #     f'&scope={packScope(PASSPORT_OPTIONS["scope"])}'
    #     f'&public_key={PASSPORT_OPTIONS["public_key"]}'
    #     f'&nonce={PASSPORT_OPTIONS["nonce"]}'
    #     f'&callback_url={PASSPORT_OPTIONS["callback_url"]}'
    #     f'&payload=nonce'
    # )

    print(url)


if __name__ == '__main__':
    main()
