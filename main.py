import os
import requests
import random
import glob

from urllib.parse import urlparse
from dotenv import load_dotenv


def get_image_extension_from_url(url):
    url_parts = urlparse(url)
    file_name = os.path.split(url_parts.path)[1]
    file_extension = os.path.splitext(file_name)[1]
    return file_extension


def download_comic(comic_number, images_folder_path, image_name):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    image_url = response.json()['img']
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_extension = get_image_extension_from_url(image_url)
    image_path = f'{images_folder_path}/{image_name}{image_extension}'
    with open(image_path, 'wb') as file:
        file.write(image_response.content)


def get_last_comic_num():
    last_comic_url = 'https://xkcd.com/info.0.json'
    response = requests.get(last_comic_url)
    response.raise_for_status()
    return response.json()['num']


def get_comic_comment(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['alt']


def upload_comic_to_vk(group_id, access_token, comic, api_version):
    api_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': api_version,
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    with open(comic, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        vk_photo = response.json()['photo']
        vk_server = response.json()['server']
        vk_hash = response.json()['hash']
    return vk_photo, vk_server, vk_hash


def save_vk_wall_photo(photo, server, vk_hash, group_id, access_token, api_version):
    api_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'photo': photo,
        'server': server,
        'hash': vk_hash,
        'v': api_version,
    }
    response = requests.post(api_url, params=params)
    response.raise_for_status()
    owner_id = response.json()['response'][0]['owner_id']
    media_id = response.json()['response'][0]['id']
    return owner_id, media_id


def post_vk_photo(group_id, owner_id, media_id, access_token, comment, api_version):
    api_url = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': -group_id,
        'access_token': access_token,
        'message': comment,
        'attachments': f'photo{owner_id}_{media_id}',
        'v': api_version,
    }
    response = requests.post(api_url, params=params)
    response.raise_for_status()


def post_comic_to_vk_group(group_id, access_token, comic_file_name, comment, api_version):
    vk_photo, vk_server, vk_hash = upload_comic_to_vk(
        group_id,
        access_token,
        comic_file_name,
        api_version
    )
    vk_owner_id, vk_media_id = save_vk_wall_photo(
        vk_photo,
        vk_server,
        vk_hash,
        group_id,
        access_token,
        api_version
    )
    post_vk_photo(
        group_id,
        vk_owner_id,
        vk_media_id,
        access_token,
        comment,
        api_version
    )


if __name__ == '__main__':
    load_dotenv()
    vk_group_id = int(os.getenv('VK_GROUP_ID'))
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_api_version = float(os.getenv('VK_API_VERSION'))
    comic_name = 'comic'
    last_comic_num = get_last_comic_num()
    comic_number = random.randint(1, last_comic_num)
    download_comic(comic_number, '.', comic_name)
    comic_comment = get_comic_comment(comic_number)
    comic_file = glob.glob(f'{comic_name}.*')[0]
    post_comic_to_vk_group(
        vk_group_id,
        vk_access_token,
        comic_file,
        comic_comment,
        vk_api_version
    )
    os.remove(comic_file)
