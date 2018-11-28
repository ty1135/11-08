# 现在不用打标了, 应该也不需要读取未打标打


# from saber.op.pyscript.src.core import func
# from avalon.material import Material
# from eigen_config.config import Configs
#
# from sheep.db.mongodb_pool import MongodbDriver
# from sheep.oss.oss import OSSDriver
#
#
# @func.register()
# def unmarked_audio(material: Material):
#     """
#     读取音频文件
#     input:
#         音频文件数量：material.get("limit")
#             limit=0表示读取所有
#         音频文件打标状态：material.get("marked", False)
#     output:
#         未打标的音频文件CDN地址：material.set("cdn", ["cdn://..."])
#     """
#     # Get filter condition
#     limit = material.get("limit", 0)
#     # Query
#     collection = get_rds()
#     ret = collection.find('audio_background').limit(limit)
#     print(list(ret))
#     # Write ret into "cdn"
#     cdn_list = [sign_url(cursor['cdn_key']) for cursor in ret if cursor.get('cdn_key')]
#     material["cdn"] = cdn_list
#     return material
#
#
# def get_rds():
#     # Load configs
#     center = Configs()
#     center.from_center('leo/editors/video_editor.yaml')
#     # Create db
#     rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
#     return rds
#
#
# def get_oss_driver():
#     # Load configs
#     center = Configs()
#     center.from_center('leo/editors/video_editor.yaml')
#     # Get bucket obj
#     oss_driver = OSSDriver(**OSSDriver.configs(center, 'oss.video_editor.address'))
#     return oss_driver
#
#
# def sign_url(key):
#     # TODO expries
#     bucket = get_oss_driver()._bucket
#     return bucket.sign_url('GET', key, 5 * 60)
#
# if __name__ == '__main__':
#     material = dict(limit=10)
#     ret_material = unmarked_audio(material)
#     print(ret_material)