
import requests
from tqdm import tqdm

class VKAPI:
    API_BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def common_params(self):
        return {
            'access_token': self.token,
            'v': '5.154'
        }

    def get_status(self):
        params = self.common_params()
        params.update({'user_id': self.user_id})
        response = requests.get(url=f'{self.API_BASE_URL}status.get', params=params)
        return response.json()

    def set_status(self, new_stat):
        params = self.common_params()
        params.update({'user_id': self.user_id, 'text': new_stat})
        response = requests.get(url=f'{self.API_BASE_URL}status.set', params=params)
        return response.json()

    def get_photo(self):
        params = self.common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1})
        response = requests.get(url=f'{self.API_BASE_URL}photos.get', params=params)
        count = response.json()['response']['count']
        photos = response.json()['response']['items']
        info = []
        for photos_info in photos:
            size_photo = photos_info['sizes'][-1]['url']
            type_photo = photos_info['sizes'][-1]['type']
            like_photo = photos_info['likes']['count']
            date_publish = photos_info['date']
            info.append({'url': size_photo, 'like': like_photo, 'type': type_photo, 'date': date_publish})
        return info

class YAdisk:

    def __init__(self, token):
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {'Authorization': token,
                        }
        self.folder = 'photos_vk'

    def mkdir(self):
        url = self.base_url
        params = {
            'path': self.folder
        }
        r = requests.put(url=url, headers=self.headers, params=params)
        return r

    def get_url(self):
        url = self.base_url + 'upload/'

        params = {
            'path': 'photos_vk'
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()['href']

    def get_files(self):
        params = {
            'path': 'photos_vk'
        }
        url = self.base_url
        r = requests.get(url=url, headers=self.headers, params=params).json()
        name_files = {}
        for i in r['_embedded']['items']:
            # name_files.append(i['name'])
            name_files += i['name']
        return
    def check_name(self, photo):
        for name in self.get_files():
            print(name['name'])
            if photo['like'] != name['name']:
                return photo['like']
            else:
                return photo['date']
        return

    def upload(self, photo):
        url = self.base_url + 'upload?'
        params = {
            'path': self.folder + '/' + str(photo['like']),
            'url': photo['url'],
        }
        r = requests.post(url=url, headers=self.headers, params=params)
        return r.json()
        # self.mkdir()
        # url = self.base_url + 'upload?'
        # name = self.check_name(photo)
        # if name == photo['like'] or name is None:
        #     params = {
        #         'path': self.folder + '/' + str(photo['like']),
        #         'url': photo['url'],
        #     }
        #     r = requests.post(url=url, headers=self.headers, params=params)
        #     return r.json()
        # else:
        #     params = {
        #         'path': self.folder + '/' + str(photo['date']),
        #         'url': photo['url'],
        #     }
        #     r = requests.post(url=url, headers=self.headers, params=params)
        #     return r.json()



# id_client = input('Введите id от необходимого аккаунта VK:\n')
# token_vk = input('Введите  от необходимого аккаунта VK:\n')

if __name__ == '__main__':
    # vk_client = VKAPI(TOKEN, 22769715)
    # photos = vk_client.get_photo()
    # url_file = photos['url']
    # like = photos[-1]['like']
    # ya = YAdisk(TOKEN_YA)
    # pprint(ya.get_files())
    def push_photo():
        ya = YAdisk(TOKEN_YA)
        vk_client = VKAPI(TOKEN, 22769715)
        photos = vk_client.get_photo()
        print(ya.get_files())

        # for photo in tqdm(photos):
        # #     # url_file = photo['url']
        # #     # like = photo['like']
        # #     # type = photo['type']
        #     ya.upload(photo)

    push_photo()

