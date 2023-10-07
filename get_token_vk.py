from urllib.parse import urlencode

import requests
url = 'https://oauth.vk.com/authorize?'
params = {
    'client_id': ***,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'response_type': 'token'

}
url = url+urlencode(params)
print(url)


