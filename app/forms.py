from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AppointmentForm(FlaskForm):
    # Name field
    name = StringField("Name", validators=[DataRequired()])

    # Start datetime fields
    start_date = DateField("Start Date", format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField("Start Time", format='%H:%M', validators=[DataRequired()])

    # End datetime fields
    end_date = DateField("End Date", format='%Y-%m-%d', validators=[DataRequired()])
    end_time = TimeField("End Time", format='%H:%M', validators=[DataRequired()])

    # Description field
    description = TextAreaField("Description", validators=[DataRequired()])

    # Private field
    private = BooleanField("Private")

    # Submit button
    submit = SubmitField("Create Appointment")

    # Custom validation for end_date
    def validate_end_date(form, field):
        # Combine start date and time into a single datetime object
        start = datetime.combine(form.start_date.data, form.start_time.data)
        # Combine end date and time into a single datetime object
        end = datetime.combine(form.end_date.data, form.end_time.data) # can also be field.data, form.end_time.data

        # Check if start is greater than or equal to end
        if start >= end:
            raise ValidationError("End date/time must come after start date/time")
        
        # Ensure start_date and end_date are the same day
        if form.start_date.data != form.end_date.data:
            raise ValidationError("Start date and end date must be on the same day")