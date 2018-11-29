from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs

from sheep.db.mongodb_pool import MongodbDriver
from sheep.oss.oss import OSSDriver

import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


@func.register()
def audio_tag_tree(material: Material):
    """
    获取音频的打标信息，返回树状层次结构
    output:
        音频文件cdn地址：material.set("tags", [
                {
                    "text": "选项一",
                    "subtree":[
                        {
                            "text":"歌曲名称",
                            "value": "cdn://..."
                        }
                    ]
                }])
    """
    logging.info('audio_tag_tree: {}'.format(str(material)))
    try:
        rds = get_rds()

        cursor = rds.find('audio_background',
                          filter={'$and': [
                              {"cdn_key": {"$ne": None}},
                              {"name": {"$ne": None}}
                          ]},
                          fields=['name', 'cdn_key'])
        audio_list = [
            {"name": each.get('name'),
            "cdn": sign_url(each.get('cdn_key'))} for each in cursor
        ]
        material['audio_list'] = audio_list
        return material
    except:
        logger.error('raising exception in audio_tag_tree', exc_info=True)


def get_rds():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create db
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    return rds


def get_oss_driver():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Get bucket obj
    oss_driver = OSSDriver(**OSSDriver.configs(center, 'oss.video_editor.address'))
    return oss_driver


def sign_url(key):
    # TODO expries
    bucket = get_oss_driver()._bucket
    return bucket.sign_url('GET', key, 5 * 60)


if __name__ == '__main__':
    material = dict()
    ret_material = audio_tag_tree(material)
    print(ret_material)