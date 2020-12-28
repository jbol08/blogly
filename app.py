"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, PostTag, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'asfdsfds'

connect_db(app)
db.create_all()

@app.route('/')
def home():

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()


    return render_template('home.html',posts=posts)

@app.route('/users')
def list_users():

    users = User.query.all()
    return render_template('index.html',users=users)

@app.route('/users/new',methods=['GET'])
def show_form():

    return render_template('add.html')


@app.route('/users/new', methods=['POST'])
def add_form():

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_info(user_id):
    '''show info about a specific user'''

    user = User.query.get_or_404(user_id)
    return render_template('user.html',user=user)

@app.route('/users/<int:user_id>/edit',)
def edit_info(user_id):
    '''show form to edit user'''

    user = User.query.get_or_404(user_id)
    return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=['POST'])
def user_update(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete',methods=['POST'])
def delete(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def posts_form(user_id):
    
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    
    return render_template('new_post.html', user=user,tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods= ['POST'])
def user_posts(user_id):    
        
        user = User.query.get_or_404(user_id)
        tag_ids = [int(num) for num in request.form.getlist("tags")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        new_post = Post(title=request.form['title'],
                        content=request.form['content'],
                        user=user, tags=tags)

        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{user_id}')
 
@app.route('/posts/<int:post_id>')
def show_posts(post_id):

    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit(post_id):

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('edit_post.html',post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit',methods=['POST'])
def edit_posts(post_id):
    
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for nums in request.form.getlist('tags')]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
       
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete',methods=['POST'])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def list_tags():

    tags = Tag.query.all()

    return render_template('tag_index.html',tags=tags)

@app.route('/tags/new')
def new_tag():

    posts = Post.query.all()

    return render_template('new_tag.html',posts=posts)


@app.route('/tags/new', methods=['POST'])
def tag_form():
    
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>')
def tag_details(tag_id):
    ''' show tag details, give ability to edit form '''
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit')
def tag_edit(tag_id):
    '''show edit form'''

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag_edit.html',tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def edit_submit(tag_id):
    '''handle edit form'''
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit',methods=['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')