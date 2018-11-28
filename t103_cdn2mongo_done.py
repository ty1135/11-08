from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs

from sheep.db.mongodb_pool import MongodbDriver

import datetime


@func.register()
def cdn2mongo(material: Material):
    """
    保存音频文件(CDN)到mongo
    input:
        音频文件CDN地址： material.get("cdn")
    """
    rds = get_rds()

    doc = {
        "cdn": material.get('cdn', ''),
        "marked": False,
        "ctime": datetime.datetime.now()
    }

    # collection.insert_one(doc).inserted_id
    rds.insert_one('audio_background', doc)
    return material


def get_rds():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create client
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    return rds


if __name__ == '__main__':
    material = dict(cdn='cdn://test')
    ret_material = cdn2mongo(material)
    print(ret_material)

    rds = get_rds()
    ret = rds.find('audio_background')
    print(list(ret))