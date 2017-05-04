from flask import Flask, session, render_template, redirect, url_for
from getcontens import get_allzj_title
from booknums import contents_number, book_number
from getpost import get_posts
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_cache import Cache


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
manage = Manager(app)
# 我们使用了’simple’类型缓存，其内部实现是Werkzeug中的SimpleCache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


class SearchForm(FlaskForm):
    name = StringField('你要搜索的小说名是？', validators=[DataRequired()])
    submit = SubmitField('搜索')

@app.route('/',methods=['GET','POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        session['search_name'] = form.name.data
        return redirect(url_for('search'))
    return render_template('index.html', form=form)

@app.route('/search')
def search():
    search_name = session.get('search_name')

    data = book_number(search_name)

    # search_id = [k for k, v in data.items() if v == search_name]

    return render_template('search.html',data=data,search_name=search_name)

@app.route('/contents/<int:id>')
def contents(id):
    search_name = session.get('search_name')

    titles = get_allzj_title(search_name)[id]
	bookid = id
    # list = get_contents_url(search_name)
    data = contents_number(titles)

    return render_template('contents.html', data=data,\
					bookid=bookid, search_name=search_name)

@app.route('/post/<bookid>/<int:id>')
@cache.cached(timeout=300, key_prefix='view_%s', unless=None)
def post(bookid, id):
    search_name = session.get('search_name')

    title = get_allzj_title(search_name)[bookid][id]

    list = get_posts(search_name, bookid, id)
    post = list[0]

    return render_template('post.html',title=title,post=post,search_name=search_name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    manage.run()