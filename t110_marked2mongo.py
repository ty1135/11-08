# 现在不用打标了


# from saber.op.pyscript.src.core import func
# from avalon.material import Material
# from eigen_config.config import Configs
#
# from sheep.db.mongodb_pool import MongodbDriver
#
# import datetime
#
#
# @func.register()
# def marked2mongo(material: Material):
#     """
#     保存音频打标信息
#     input:
#         一级标签：material.get("level_1")
#         二级标签：material.get("level_2")
#         音频文件名：material.get("name")
#         音频文件类型：material.get("ext")
#         音频文件地址：material.get("id")
#     """
#
#     db = get_db()
#
#     doc = {
#         "cdn": material.get('cdn', ''),
#         "marked": False,
#         "ctime": datetime.datetime.now()
#     }
#
#     # collection.insert_one(doc).inserted_id
#     db.insert_one('audio_background', doc)
#     return material
#
#
# def get_db():
#     # Load configs
#     center = Configs()
#     center.from_center('leo/editors/video_editor.yaml')
#     # Create client
#     rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
#     client = rds.connection()
#     db = rds.connection()
#
#     return db
#
