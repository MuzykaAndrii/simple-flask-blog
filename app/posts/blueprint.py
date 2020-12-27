from flask import Blueprint, render_template, request, url_for, flash, abort, redirect
from app.forms import CreatePostForm
from app.models import Post, User
from flask_login import login_required, current_user
from datetime import datetime as dt

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route("/")
def index():
    return redirect(url_for('posts.get_posts'))

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    creator = User.query.get(post.user_id).username
    return render_template('posts/post.html', title=post.title, post=post, creator=creator)

####### CREATE POST
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        creator_id = current_user.id

        post = Post(title, content, creator_id)
        post.save()

        flash('Post created successfully', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    return render_template('posts/create_post.html', title='Create new post', form=form)


######## GET POSTS
@posts.route('/posts', methods=['GET'])
def get_posts():
    # Set the pagination configuration
    POSTS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search_query')

    if search_query:
        # paginate according to search query
        posts = Post.query.filter(Post.title.contains(search_query) | Post.content.contains(search_query)).paginate(page=page, per_page=POSTS_PER_PAGE)
    else:
        #paginate simply
        posts = Post.query.paginate(page=page, per_page=POSTS_PER_PAGE)

    return render_template('posts/posts.html', title='Posts', posts=posts)

###### UPDATE POST
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)

    form = CreatePostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_posted = dt.now()
        post.save()

        flash('Post successfully updated', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('posts/update_post.html', title='Edit post', form=form, post_id=post.id)

####### DELETE POST
@posts.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    post.delete()
    flash('Your post hes been deleted!', 'success')
    return redirect(url_for('posts.get_posts'))