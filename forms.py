from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateField, TimeField, FileField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Length, NumberRange, Optional, InputRequired, Regexp
from wtforms.widgets import ListWidget, CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    """Model representing MultiCheckboxField."""
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class RegistrationForm(FlaskForm):
    """Model representing RegistrationForm."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    gender = SelectField('Gender', choices=[('', 'Select...'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()])
    date_of_birth = StringField('Date of Birth', validators=[Optional()], render_kw={"placeholder": "DD-MM-YYYY"})
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    """Model representing LoginForm."""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    """Model representing ProfileForm."""
    profile_name = StringField('Profile Name', validators=[DataRequired(), Length(min=2, max=100)])
    date_of_birth = StringField('Date of Birth', validators=[Optional()], render_kw={"placeholder": "DD-MM-YYYY"})
    gender = SelectField('Gender', choices=[('', 'Select...'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[Optional()])
    profile_picture = FileField('Update Profile Picture')
    submit = SubmitField('Update Profile')
    
class ChangePasswordForm(FlaskForm):
    """Model representing ChangePasswordForm."""
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')

class MedicineForm(FlaskForm):
    """Model representing MedicineForm."""
    name = StringField('Medicine Name', validators=[DataRequired()])
    current_stock = IntegerField('Current Stock', validators=[DataRequired(), NumberRange(min=0)])
    meal_timing = SelectField('Meal Timing', choices=[('Before', 'Before'), ('After', 'After')], validators=[DataRequired()])
    meal_type = SelectField('Meal', choices=[('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], validators=[DataRequired()])
    reason = TextAreaField('Reason/Purpose', validators=[Optional()])
    submit = SubmitField('Save Medicine')

class ReminderForm(FlaskForm):
    """Model representing ReminderForm."""
    medicine_id = SelectField('For Medicine', validators=[InputRequired(message="Please select a medicine.")])
    time = TimeField('At Time', format='%H:%M', validators=[DataRequired()])
    days = MultiCheckboxField('On Days', 
                               choices=[('Mon', 'Mon'), ('Tue', 'Tue'), ('Wed', 'Wed'), ('Thu', 'Thu'), ('Fri', 'Fri'), ('Sat', 'Sat'), ('Sun', 'Sun')],
                               validators=[InputRequired(message="Please select at least one day.")])
    note = StringField('Note (Optional)', validators=[Optional()])
    submit = SubmitField('Set Reminder')

class HistoryForm(FlaskForm):
    """Model representing HistoryForm."""
    condition = StringField('Condition/Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    report_file = FileField('Upload Report (Optional)')
    submit = SubmitField('Add Record')

class AppointmentForm(FlaskForm):
    """Model representing AppointmentForm."""
    doctor_name = StringField('Doctor Name', validators=[DataRequired()])
    hospital = StringField('Hospital/Clinic', validators=[Optional()])
    date_time = StringField('Date and Time', validators=[DataRequired()], render_kw={"placeholder": "DD-MM-YYYY HH:MM (24-hr format)"})
    purpose = StringField('Purpose', validators=[DataRequired()])
    reminder_minutes_before = SelectField('Remind Me Before', coerce=int, choices=[
        (0, 'No Reminder'), (15, '15 Minutes'), (30, '30 Minutes'), (60, '1 Hour'), (1440, '1 Day')
    ], default=0, validators=[Optional()])
    submit = SubmitField('Schedule Appointment')
    
class EmergencyContactForm(FlaskForm):
    """Model representing EmergencyContactForm."""
    name = StringField('Contact Name', validators=[DataRequired()])
    relationship = StringField('Relationship', validators=[Optional()])
    phone = StringField('Phone Number', validators=[
        DataRequired(),
        Regexp(r'^\d{10}$', message="Phone number must be exactly 10 digits for Indian format.")
    ])
    submit = SubmitField('Save Contact')