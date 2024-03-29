# from .forms import UpdateProfile
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Required
from .. import db
    
#Pitch Form
class PitForm(FlaskForm):
    content = TextAreaField('Post Your Pitch',validators=[Required()])
    submit = SubmitField('Submit Pitch') 

#Comment Form
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Leave a comment')  
    
#updateProfileForm
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')   

#categoryForm
class CategoryForm(FlaskForm):
    name = TextAreaField('Category')
    submit = SubmitField()  