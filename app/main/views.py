from . import main
from flask import render_template,request,redirect,url_for, abort
from .forms import UpdateProfile,PitForm,CommentForm,CategoryForm
from ..models import Pitch,User,Category
from .. import db,photos
from flask_login import login_required, current_user
import markdown2 

# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    category=Category.get_catz()
    return render_template('index.html', category=category)

@main.route('/add/category', methods=['GET','POST'])
@login_required
def new_category():
    '''
    View new group route function that returns a page with a form to create a category
    '''
    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name)
        new_category.save_cat()

        return redirect(url_for('.index'))    
    title = 'New category'
    return render_template('nu_category.html', category_form = form,title=title)


@main.route('/categories/<int:id>')
def category(id):
    categorii = Category.get_catz()
    pitches = Pitch.query.filter_by(category=id).all()
    print(category)

    return render_template('category.html', pitches=pitches, category=categorii)



@main.route('/user/<uname>')
def profile(uname):
    '''
    a function to hold profile
    '''
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    '''
    function to update my profile and save the changes
    '''
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    '''
    function to update a picture
    '''
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

#adding a new pitch
@main.route('/categories/view_pitch/add/<int:id>', methods=['GET','POST'])
@login_required
def nu_pitch(id):
    '''
    function to insert or add new pitches and fetch from them some data
    '''
    form = PitForm()
    category = Category.query.filter_by(id=id).first()
    title=f'Welcome To Pitches'
    
    if category is None:
        abort(404)
        
    if form.validate_on_submit():
        content = form.content.data
        nu_pitch= Pitch(content=content,category=category.id,user_id=current_user.id,upvotes=0,downvotes=0)
        nu_pitch.save_pitches()
        return redirect(url_for('.index',id=category.id))
    return render_template('nu_pitch.html', title = title, pitch_form = form, category = category)

#view Pitch with its comments
@main.route('/categories/view_pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def viewing_pitch(id):
    '''
    a function to view inserted pitches
    '''
    print(id)
    
    pitchez=Pitch.get_pitches(id)
    
    if pitchez is None:
        abort(404)
    comment =Comments.get_comments(id)
    
    return render_template('pitch.html',comment=comment, pitchez=pitchez,category_id=id)

#UPVOTES AND DOWNVOTES
@main.route('/downvote/<int:id>',methods = ['GET','POST'])
def downvotes(id):
    '''
    a function to determine and save downvotes of a pitch
    '''

    pitch = Pitch.query.filter_by(id=id).first()
    pitch.downvotes = pitch.downvotes + 1
    db.session.add(pitch)
    db.session.commit()
    return redirect("/".format(id=pitch.id))


@main.route('/upvote/<int:id>',methods = ['GET','POST'])
def upvotes(id):
    '''
    function to check and save upvotes
    '''
    pitch = Pitch.query.filter_by(id=id).first()
    pitch.upvotes = pitch.upvotes +1
    db.session.add(pitch)
    db.session.commit()
    return redirect("/".format(id=pitch.id))
    return redirect(".profile".format(id=pitch.id))

@main.route('/new_comment/<int:id>', methods=['GET','POST'])
@login_required
def new_comment(id):
    '''
    function that adds comment
    '''
    form = CommentForm()
    comment = Comment.query.filter_by(pitch_id=id).all()
    pitches = Pitch.query.filter_by(id=id).first()
    user = User.query.filter_by(id = id).first()
    title=f'welcome to pitches comments'
        
    if form.validate_on_submit():
        feedback = form.comment.data
        new_comment= Comment(feedback=feedback,user_id=current_user.id,pitch_id=pitches.id)
         
        new_comment.save_comment()
        return redirect(url_for('.index',uname=current_user.username))
    return render_template('comment.html', title = title, comment_form = form,pitches=pitches)

# @main.route('/review/<int:id>')
# def single_review(id):
#     review=Review.query.get(id)
#     if review is None:
#         abort(404)
#     format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
#     return render_template('review.html',review = review,format_review=format_review)