from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.db.mongodb_pool import MongodbDriver
from pymongo.collection import ObjectId

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

DONE = 1


@func.register()
def video_article(material: Material):
    """
    调用MS算子进行视频剪辑
    input:
        视频链接地址：material.get("video_clip_url")
        文章ID：material.get("_id")
    """
    # Get input
    logging.info('video_article: {}'.format(str(material)))

    try:
        video_clip_url = material.get("video_clip_url")
        article_id = material.get("_id")

        # TODO sheep mongo 没有更新
        # TODO done 1？
        # TODO 更新 video_url 还是 video_cdn
        # TODO collection名都没读配置
        # TODO exception

        rds = get_rds()
        ret = rds.find_one_and_update(
            'video_article',
            {'_id': ObjectId(article_id)},
            {'$set': {'progress': DONE, 'video_url': video_clip_url}}
        )
        if not ret:
            logging.error('video_article document({}) not exists'.format(article_id))
            raise Exception
        return material
    except:
        logger.error('raising exception in video_article', exc_info=True)


def get_rds():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create client
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    return rds


if __name__ == '__main__':
    rds = get_rds()

    material = dict(video_clip_url='https://test.test.com', _id='5bfe3386d5678d784970890f')
    ret_material = video_article(material)

    ret = rds.find_one(
        'video_article',
        filter={'_id': ObjectId('5bfe3386d5678d784970890f')},
    )
    print(ret)
