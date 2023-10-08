import datetime
import json

from tokens import TOKEN, TOKEN_YA
import requests
from tqdm import tqdm


class VKAPI:
    API_BASE_URL = 'https://api.vk.com/method/'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def __common_params(self):
        return {
            'access_token': self.token,
            'v': '5.154'
        }

    def get_photo(self):
        params = self.__common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile', 'extended': 1})
        response = requests.get(url=f'{self.API_BASE_URL}photos.get', params=params)
        photos = response.json()['response']['items']
        info = []
        for photos_info in photos:
            size_photo = photos_info['sizes'][-1]['url']
            type_photo = photos_info['sizes'][-1]['type']
            like_photo = photos_info['likes']['count']
            date_publish = photos_info['date']
            info.append({'url': size_photo, 'like': like_photo, 'type': type_photo, 'date': date_publish})
        return info


class YADISK:

    def __init__(self, token):
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {'Authorization': token,
                        }
        self.folder = 'photos_vk'

    def __mkdir(self):
        url = self.base_url
        params = {
            'path': self.folder
        }
        r = requests.put(url=url, headers=self.headers, params=params)
        return r

    def __get_files(self):
        name_list = []
        params = {
            'path': 'photos_vk'
        }
        url = self.base_url
        r = requests.get(url=url, headers=self.headers, params=params).json()
        items = [i for i in r['_embedded']['items']]
        for i in items:
            name_list.append(i['name'])
        return name_list

    def upload(self, photo):
        self.__mkdir()
        url = self.base_url + 'upload?'
        list_name = self.__get_files()
        if f"{photo['like']}" in list_name:
            date = f"{datetime.datetime.fromtimestamp(photo['date']).year}." \
                   f"{datetime.datetime.fromtimestamp(photo['date']).month}." \
                   f"{datetime.datetime.fromtimestamp(photo['date']).day}"
            params = {
                'path': self.folder + f"/{photo['like']}-{date}",
                'url': photo['url'],
            }
            requests.post(url=url, headers=self.headers, params=params)
            return {'file_name': f"{photo['like']}-{date}.jpg", 'size': f"{photo['type']}"}

        else:
            params = {
                'path': self.folder + '/' + str(photo['like']),
                'url': photo['url'],
            }
            requests.post(url=url, headers=self.headers, params=params)
            return {'file_name': f"{photo['like']}.jpg", 'size': f"{photo['type']}"}


# id_client = input('Введите id от необходимого аккаунта VK:\n')
# token_vk = input('Введите  от необходимого аккаунта VK:\n')

if __name__ == '__main__':
    def export_to_json(log_file):
        with open('files/log.json', 'a', encoding='utf-8') as file:
            json.dump(log_file, file)


    def backup_photo():
        ya = YADISK(TOKEN_YA)
        vk_client = VKAPI(TOKEN, 22769715)
        photos = vk_client.get_photo()
        log_file = []
        for photo in tqdm(photos):
            log_file.append(ya.upload(photo))
        export_to_json(log_file)

        print(
            'Выгрузка фотографий на YAdisk заканчана, url для просмотра фото https://disk.yandex.ru/client/disk/photos_vk ')


    backup_photo()
