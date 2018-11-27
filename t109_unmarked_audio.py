from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs

from sheep.db.mongodb_pool import MongodbDriver


@func.register()
def unmarked_audio(material: Material):
    """
    读取音频文件
    input:
        音频文件数量：material.get("limit")
            limit=0表示读取所有
        音频文件打标状态：material.get("marked", False)
    output:
        未打标的音频文件CDN地址：material.set("cdn", ["cdn://..."])
    """
    # Get filter condition
    limit = material.get("limit", 0)
    marked = material.get("marked", False)
    # Query
    collection = get_db()
    ret = collection.find('audio_background', filter={"marked": marked}).limit(limit)
    # Write ret into "cdn"
    cdn_list = [cursor.get('cdn', '') for cursor in ret]
    material.set("cdn", cdn_list)


def get_db():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create db
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    db = rds.connection()

    return db
