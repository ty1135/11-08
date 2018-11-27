from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.oss.oss import OSSDriver

import oss2
import requests

import os
import uuid
import pathlib
import logging


@func.register()
def crawl2cdn(material: Material):
    """
    爬取视频并上传到CDN
    input:
        视频文件地址：material.get("href")
    output:
        未打标的音频文件CDN地址：material.set("cdn", "cdn://...")
    """
    # check href
    if material.get("href") is None:
        # TODO 没有怎么处理,所有算子都是
        logging.error("'href' not found in material")
        raise Exception

    path = pathlib.Path('./downloads')
    path.mkdir(parents=True, exist_ok=True)
    file_path = str(path.absolute()) + '/' + str(uuid.uuid4())

    fetch(material['href'], file_path)
    key = upload(file_path)
    remove_file(file_path)
    return key


def fetch(url, file_path):
    ret = requests.get(url, allow_redirects=True, stream=True)
    with open(file_path, 'wb+') as f:
        for chunk in ret.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


def upload(file_path):
    driver = get_oss_driver()

    key = str(uuid.uuid4())
    try:
        cdn = driver.put_object_from_file(key, file_path, cdn=True)
    except oss2.exceptions.OssError as e:
        logging.error(str(e))
    return cdn


def remove_file(file_path):
    os.remove(file_path)


def get_oss_driver():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Get bucket obj
    oss_driver = OSSDriver(**OSSDriver.configs(center, 'oss.video_editor.address'))
    return oss_driver