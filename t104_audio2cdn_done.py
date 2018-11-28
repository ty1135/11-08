from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.oss.oss import OSSDriver


import oss2

import uuid
import base64
import logging


@func.register()
def audio2cdn(material: Material):
    logging.info('audio2cdn: {}'.format(str(material)))
    """
    上传音频文件到CDN
    input:
        音频文件base64编码：material.get("audio")
        文件名字: material.get("filename")
    output:
        音频文件cdn地址：material.set("cdn", "cdn://...")
        音频文件名称：material.set("filename_without_ext", "cdn://...")
    """
    name, ext = split_filename(material.get('filename'))
    cdn_key = upload(decode(material.get('audio')), ext)

    material['ext'] = ext
    material['name'] = name
    material['cdn_key'] = cdn_key
    return material


def decode(encoded_data):
    return base64.b64decode(encoded_data)


def upload(file_bytes, ext):
    driver = get_oss_driver()
    key = str(uuid.uuid4()) + '.' + ext
    try:
        cdn_key = driver.put_object(key, file_bytes)
    except oss2.exceptions.OssError as e:
        logging.error(str(e))
        raise
    return cdn_key


def get_oss_driver():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Get bucket obj
    oss_driver = OSSDriver(**OSSDriver.configs(center, 'oss.video_editor.address'))
    return oss_driver


def split_filename(filename):
    sections = filename.split('.')
    return '.'.join(sections[:-1]), sections[-1]


if __name__ == '__main__':
    with open("./resources/secosmic_lo.wav", "rb") as f:
        encoded_audio = base64.b64encode(f.read())
    material = dict(audio=encoded_audio, filename='secosmic_lo.wav')
    ret_material = audio2cdn(material)

    driver = get_oss_driver()
    url = driver._bucket.sign_url('GET', ret_material['cdn_key'], 300)
    print(url)
    print(ret_material)