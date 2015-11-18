# coding: utf-8
from flask import render_template, Blueprint, jsonify, request, redirect, url_for, g
import json
from random import randint
from leancloud import Object
from leancloud import Query, Relation
from leancloud import LeanCloudError
from ..models import Photo, Tag
from ..utils.permissions import VisitorPermission, UserPermission
from ..forms import MultiTagForm

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
    keyword = request.args.get('q')
    results = Query(Tag).equal_to('name', keyword).find()
    if len(results) != 0:
        tag = results[0]
        query = Relation.reverse_query('Photo', 'tags', tag)
        photos = query.find()
    else:
        photos = []
    return render_template('site/search/search.html', keyword=keyword, photos=photos)

@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about/about.html')


@bp.route('/_next4tag')
def next4tag():
    data = {}
    total = Query.do_cloud_query('select count(*) from Photo')
    try:
        query = Query(Photo).descending('createdAt').skip(randint(0, total.count))
        photo = query.first()
        data['photo_id'] = photo.id
        data['photo_url'] = photo.get('url')
        tags_relation = photo.relation('tags')
        tags_count = tags_relation.query().count()
        data['tags_count'] = tags_count
    except LeanCloudError, e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            data = {}
        else:
            raise e
    return jsonify(result=json.dumps(data))


@bp.route('/tag', methods=['GET', 'POST'])
@UserPermission()
def tag():
    """Tag Photo"""
    form = MultiTagForm()
    if form.validate_on_submit():
        tags = form.data['tags'].split(',')

        photo = Query(Photo).get(form.data['photoid'])
        relation = photo.relation('tags')

        for tag in tags:
            # Obtain existed tag by name
            results = Query(Tag).equal_to('name', tag).find()
            if len(results) != 0:
                avostag = results[0]
                avostag.increment('count', 1)
            else:
                avostag = Tag()
                avostag.set('name', tag)
                avostag.save()
            contributors = avostag.relation('contributors')
            contributors.add(g.user)
            avostag.save()
            # Add relation to photo
            relation.add(avostag)
        photo.save()

        query = Relation.reverse_query('Tag', 'contributors', g.user)
        count = query.count()
        return render_template('site/tag/done.html', user_tag_count=count)
    else:
        total = Query.do_cloud_query('select count(*) from Photo')
        try:
            query = Query(Photo).descending('createdAt').skip(randint(0, total.count))
            item = query.first()
            return render_template('site/tag/tag.html', photo=item, form=form)
        except LeanCloudError, e:
            return redirect(url_for('site.about'))


