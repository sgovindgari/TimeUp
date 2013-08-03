from flaskext import wtf
from flaskext.wtf import validators

class UserForm(wtf.Form):
    username = wtf.TextField('Username', validators=[validators.Required(), validators.Length(min=3, max=20, message='Username must be between %(min)d and %(max)d characters long.')])
    email = wtf.TextField('Email', validators=[validators.Required(), validators.Email()])
    passwd = wtf.PasswordField('Password', validators=[validators.Required(), validators.Length(min=8, max=20, message='Password must be between %(min)d and %(max)d characters long.')])
    confirm = wtf.PasswordField('Repeat Password', validators=[validators.Required(), validators.EqualTo('passwd', message='Passwords must match')])
    f_name = wtf.TextField('First Name', validators=[validators.Required()])
    l_name = wtf.TextField('Last Name', validators=[validators.Required()])

class SigninForm(wtf.Form):
    username = wtf.TextField('Username', validators=[validators.Required()])
    passwd = wtf.PasswordField('Password', validators=[validators.Required()])

class UpdateUserForm(wtf.Form):
    f_name = wtf.TextField('First Name', validators=[validators.Required()])
    l_name = wtf.TextField('Last Name', validators=[validators.Required()])
    email = wtf.TextField('Email', validators=[validators.Required(), validators.Email()])
    mpg = wtf.FloatField('MPG', validators=[validators.Optional(), validators.NumberRange(min=1, max=1000)])
    transit_cost = wtf.FloatField('One-Way Public Transit Cost (dollars)', validators=[validators.Optional(), validators.NumberRange(min=0)])
    passwd = wtf.PasswordField('Change Password (optional)', validators=[validators.Optional(), validators.Length(min=8, max=20, message='Password must be between %(min)d and %(max)d characters long.')])
    confirm = wtf.PasswordField('Repeat Password', validators=[validators.Optional(), validators.EqualTo('passwd', message='Passwords must match')])


