import flask

from . import db_session
from .posts import Post

blueprint = flask.Blueprint(
    'post_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/posts')
def get_news():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()
    return flask.jsonify(
        {
            'posts':
                [item.to_dict(only=('title', 'content', 'user.name')) 
                 for item in posts]
        }
    )

@blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
def get_one_news(post_id):
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).get(post_id)
    if not posts:
        return flask.jsonify({'error': 'Not found'})
    return flask.jsonify(
        {
            'posts': posts.to_dict(only=(
                'title', 'content', 'author'))
        }
    )

@blueprint.route('/api/posts', methods=['POST'])
def create_post():
    request=flask.request
    if not request.json:
        return flask.jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title', 'content', 'author']):
        return flask.jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    post = Post(
        title=request.json['title'],
        content=request.json['content'],
        author=request.json['author'],
    )
    db_sess.add(post)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})