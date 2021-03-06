from avalon.material import Material
from eigen_config.config import Configs
from saber.op.pyscript.src.core import func
from sheep.db.mongodb_pool import MongodbDriver

import datetime
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


@func.register()
def cdn2mongo(material: Material):
    """
    保存音频文件(CDN)到mongo
    input:
        音频文件CDN地址： material.get("cdn_key")
                       material.get("name")
                       material.get("ext")
    """
    logger.info('run cdn2mongo: {}'.format(str(material)))
    try:
        rds = get_rds()

        doc = {
            "cdn_key": material.get('cdn_key'),
            "name": material.get('name'),
            "ext": material.get('name'),
            "ctime": datetime.datetime.now()
        }

        rds.insert_one('audio_background', doc)
        return material
    except:
        logger.error('raising exception in cdn2mongo', exc_info=True)


def get_rds():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create client
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    return rds


if __name__ == '__main__':
    material = dict(
        cdn_key='ea95e49b-64de-4d22-811d-c9af2c9a492e.wav',
        name='音乐',
        ext='wav'
    )
    ret_material = cdn2mongo(material)
    print(ret_material)

    rds = get_rds()
    ret = rds.find('audio_background', filter={"cdn_key": 'ea95e49b-64de-4d22-811d-c9af2c9a492e.wav'})
    print(list(ret))