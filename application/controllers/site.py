# coding: utf-8
from flask import render_template, Blueprint, jsonify, request
import json
from random import randint
from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from ..models import Photo

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    return render_template('site/index/index.html')

@bp.route('/_next_cover')
def next_cover():
    data = {}
    total = Query.do_cloud_query('select count(*) from Photo')
    try:
        query = Query(Photo).descending('createdAt').skip(randint(0, total.count))
        cover = query.first()
        data['cover'] = cover.get('url') + '?imageView2/2/w/1920/interlace/1'
        data['original'] = cover.get('url') + '?download'
    except LeanCloudError, e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            data = {}
        else:
            raise e
    return jsonify(result=json.dumps(data))

@bp.route('/search')
def search(keyword=None):
    keyword = request.args.get('keyword')
    query = Query(Photo).equal_to("tags", keyword).descending('createdAt')
    photos = query.find()
    return render_template('site/search/search.html', keyword=keyword, photos=photos)

@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about/about.html')