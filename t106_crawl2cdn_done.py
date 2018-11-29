from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.oss.oss import OSSDriver

import oss2
import requests

import re
import os
import uuid
import pathlib
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


@func.register()
def crawl2cdn(material: Material):
    """
    爬取视频并上传到CDN
    input:
        视频文件地址：material.get("href")
    output:
        未打标的音频文件CDN地址：material.set("cdn_key", "a_key")
    """
    logging.info('run crawl2cdn: {}'.format(str(material)))
    # check href
    try:
        path = pathlib.Path('./downloads')
        path.mkdir(parents=True, exist_ok=True)
        temp_file_path= str(path.absolute()) + '/' + str(uuid.uuid4())

        info_filename = fetch(material['href'], temp_file_path)
        cdn_key = upload(temp_file_path, info_filename)
        material['cdn_key'] = cdn_key
        remove_file(temp_file_path)
        return material
    except:
        logger.error('raising exception in crawl2cdn', exc_info=True)



def fetch(url, file_path):
    """Download from 'url' to 'file_path' and return a guessed filename"""
    ret = requests.get(url, allow_redirects=True, stream=True)
    with open(file_path, 'wb+') as f:
        for chunk in ret.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    if "Content-Disposition" in ret.headers.keys():
        filename = re.findall("filename=(.+)", ret.headers["Content-Disposition"])[0]
    else:
        filename = url.split("/")[-1]
    return filename


def upload(file_path, info_filename):
    """upload from file with its info"""
    _, ext = split_filename(info_filename)

    driver = get_oss_driver()

    key = str(uuid.uuid4()) + '.' + ext
    try:
        cdn_key = driver.put_object_from_file(key, file_path)
    except oss2.exceptions.OssError as e:
        logging.error(str(e))
    return cdn_key


def split_filename(filename):
    sections = filename.split('.')
    return '.'.join(sections[:-1]), sections[-1]


def remove_file(file_path):
    os.remove(file_path)


def get_oss_driver():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Get bucket obj
    oss_driver = OSSDriver(**OSSDriver.configs(center, 'oss.video_editor.address'))
    return oss_driver






if __name__ == '__main__':
    # TODO cdn 地址链接没开
    material = dict(href='https://cdn.aidigger.com/assets/images/official/all.png')
    ret_material = crawl2cdn(material)
    print(ret_material)

    driver = get_oss_driver()
    url = driver._bucket.sign_url('GET', ret_material['cdn_key'], 300)
    print(url)