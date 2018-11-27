from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.oss.oss import OSSDriver


import oss2

import os
import uuid
import pathlib
import base64
import logging


@func.register()
def audio2cdn(material: Material):
    """
    上传音频文件到CDN
    input:
        音频文件base64编码：material.get("audio")
    output:
        音频文件cdn地址：material.set("cdn", "cdn://...")
    """
    path = pathlib.Path('./downloads')
    path.mkdir(parents=True, exist_ok=True)
    file_path = str(path.absolute()) + '/' + str(uuid.uuid4())

    cdn = upload(decode(material.get('audio', '')))
    remove_file(file_path)

    material['cdn'] = cdn
    return material


def decode(encoded_data):
    return base64.b64decode(encoded_data)


def upload(file_bytes):
    driver = get_oss_driver()
    key = str(uuid.uuid4())
    try:
        cdn = driver.put_object(key, file_bytes, cdn=True)
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