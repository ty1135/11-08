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
    db = get_db()

    doc = {
        "cdn": material.get('cdn', ''),
        "marked": False,
        "ctime": datetime.datetime.now()
    }

    # collection.insert_one(doc).inserted_id
    db.insert_one('audio_background', doc)
    return material


def get_db():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create client
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    client = rds.connection()
    db = rds.connection()

    return db
