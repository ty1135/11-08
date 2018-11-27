from saber.op.pyscript.src.core import func
from avalon.material import Material
from eigen_config.config import Configs
from sheep.db.mongodb_pool import MongodbDriver

import oss2
import requests

import os
import uuid
import pathlib
import logging

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
    video_clip_url = material.get("video_clip_url")
    article_id = material.get("_id")

    # TODO sheep mongo 没有更新
    # TODO done 1？
    # TODO 更新 video_url 还是 video_cdn

    db = get_db()
    db.find_one_and_update(
        {'_id': article_id},
        {'$set': {'progress': DONE, 'video_url': video_clip_url}}
    )


def get_db():
    # Load configs
    center = Configs()
    center.from_center('leo/editors/video_editor.yaml')
    # Create client
    rds = MongodbDriver(**MongodbDriver.configs(center, "mongodb_pool.video_editor.address"))
    client = rds.connection()
    db = rds.connection()

    return db

