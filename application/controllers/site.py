# coding: utf-8
from flask import render_template, Blueprint, jsonify, request, redirect, url_for, g
import json
from random import randint
from leancloud import Object, User
from leancloud import Query, Relation, engine
from leancloud import LeanCloudError
from ..models import Photo, Tag, PhotoTag
from ..utils.permissions import VisitorPermission, UserPermission
from ..forms import MultiTagForm
from flask import session

bp = Blueprint('site', __name__)

@bp.route('/')
def index():
    total = Query.do_cloud_query('select count(*) from Photo')
    try:
        query = Query(Photo).descending('createdAt').skip(randint(0, total.count))
        cover = query.first()
    except LeanCloudError, e:
        raise e
    return render_template('site/index/index.html', cover=cover)

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
        # tag per photo
        print tag.get('name')
        ptags = Query(PhotoTag).equal_to("tag", tag).find()

        photos = []
        for ptag in ptags:
            # print ptag.get('tag').get('name')
            plist = Relation.reverse_query('Photo', 'ptags', ptag).find()
            print len(plist)
            photos.extend(plist)
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

@bp.route('/tagit', methods=['POST'])
def tagit():
    tags = request.form['tags'].split(',')
    photo = Query(Photo).get(request.form['photoid'])

    ptags_relation = photo.relation('ptags')

    for tag in tags:
        # Check if tag name existed
        results = Query(Tag).equal_to('name', tag).find()
        if len(results) != 0:
            # existed
            avostag = results[0]
        else:
            # not existed
            # save general tag
            avostag = Tag()
            avostag.set('name', tag)
            avostag.save()
        
        contributors = avostag.relation('contributors')
        contributors.add(g.user)
        avostag.save()

        ptaglist = ptags_relation.query().equal_to('tag', avostag).find()
        if len(ptaglist) == 0:
            # 标签未在该照片标记
            ptag = PhotoTag()
            ptag.set('tag', avostag)
            # 该标签被打在新的照片上
            avostag.increment('count', 1)
            avostag.save()
        else:
            # 标签已在该照片标记
            ptag = ptaglist[0]
            ptag.increment('count', 1)

        ptag.relation('contributors').add(g.user)
        ptag.save()

        # 给照片加标签
        ptags_relation.add(ptag)

    photo.save()

    query = Relation.reverse_query('PhotoTag', 'contributors', g.user)
    count = query.count()
    # count = photo.relation('ptags').query().count()

    return json.dumps({'status':'OK', 'count':count, 'photoid': request.form['photoid']});


    # relation = photo.relation('tags')

    # for tag in tags:
    #     # Obtain existed tag by name
    #     results = Query(Tag).equal_to('name', tag).find()
    #     if len(results) != 0:
    #         avostag = results[0]
    #         avostag.increment('count', 1)
    #     else:
    #         avostag = Tag()
    #         avostag.set('name', tag)
    #         avostag.save()
    #     contributors = avostag.relation('contributors')
    #     contributors.add(g.user)
    #     avostag.save()
    #     # Add relation to photo
    #     relation.add(avostag)
    # photo.save()

    # query = Relation.reverse_query('Tag', 'contributors', g.user)
    # count = query.count()

    # return json.dumps({'status':'OK','count':count,'photoid': request.form['photoid']});


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
            query = Relation.reverse_query('PhotoTag', 'contributors', g.user)
            count = query.count()
            return render_template('site/tag/tag.html', photo=item, utagcount=count, form=form)
        except LeanCloudError, e:
            return redirect(url_for('site.about'))

@bp.route('/hot')
def hot():
    return render_template('site/hot/hot.html')


@bp.route('/disclaimer')
def disclaimer():
    return render_template('site/static/disclaimer.html')

@bp.route('/wiki')
def wiki():
    return render_template('site/static/wiki.html')
