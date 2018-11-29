from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.db.mongodb_pool import MongodbDriver

import logging


logging.basicConfig()
logger = logging.getLogger(__name__)


@func.register()
def video_article_progress(material: Material):
    """
    获取视频剪辑文章，返回文章列表
    output: 
        音频文件cdn地址：material.set("progress", [
                {
                    "article_id": {
                        "text": "ID000001" 
                    },
                    "article_name": {
                        "text": "测试文章01"
                    },
                    "create_time": {
                        "text": "2018-09-12 10:32:48"
                    },
                    "progress": {
                        "text": "60%"
                    },
                    "owner": {
                        "text": "钟磬"
                    },
                    "operation": [
                        {
                            "text": "",
                            "method": ""
                        }
                    ]   
                }])
    """
    # TODO 分页
    logging.info('video_article_progress: {}'.format(str(material)))
    try:
        progress_value = []

        collection = get_rds()
        cursor = collection.find('video_article')

        for each in cursor:
            row = {}

            row['article_id'] = {'text': str(each.get('_id', ''))}
            row['article_name'] = {'text': each.get('name', '')}
            row['create_time'] = {'text': each.get('ctime', '')}
            row['progress'] = {'text': each.get('progress', '')}
            row['owner'] = {'text': each.get('owner', '')}
            row['operation'] = [
                {'text': "预览", "method": "preview"},
                {'text': "详情", "method": "detail"},
                {'text': "删除", "method": "delete"},
                {'text': "复制", "method": "copy"}
            ]

            progress_value.append(row)

        material["progress"] = progress_value
        return material
    except:
        logger.error('raising exception in video_article_progress', exc_info=True)


def get_rds():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create db
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    return rds


if __name__ == '__main__':
    material = dict()
    ret_material = video_article_progress(material)
    print(ret_material)