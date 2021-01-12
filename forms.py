from flask_wtf import FlaskForm as FF
from wtforms import StringField,TextAreaField, PasswordField, DateTimeField, DateField, SubmitField, BooleanField,FileField, IntegerField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, AnyOf, NoneOf, Optional


class add_hospital(FF):
    city_id = IntegerField('City ID *', validators=[DataRequired()])
    name = TextAreaField('Hospital Name *', validators=[DataRequired(), Length(min = 2, max = 300),Optional()])
    telephone = StringField('Phone Number', render_kw={"placeholder": "+90xxxxxxxxxx"},validators=[Optional(), Length(min = 13, max = 13)])
    capacity = IntegerField('Capacity')
    for_pandemic = SelectField('For pandemic?', choices = [('true','Yes'),('false','No')])
    submit = SubmitField('Add')

class update_hospital(FF):
    city_id = IntegerField('City ID')
    name = StringField('Hospital Name', validators=[ Length(min = 2, max = 300),Optional()])
    telephone = StringField('Phone Number', render_kw={"placeholder": "+90xxxxxxxxxx"},validators=[Optional()])
    capacity = IntegerField('Capacity')
    for_pandemic = SelectField('For pandemic?', choices = [('true','Yes'),('false','No')])
    submit = SubmitField('Update')

class add_testcenter(FF):
    hospital_id = IntegerField('Hospital ID ', validators=[DataRequired()])
    test_stock = IntegerField('Test Stock ')
    personnel_number = IntegerField('Number of Personnel ')
    submit = SubmitField('Add')

class update_testcenter(FF):
    hospital_id = IntegerField('Hospital ID ')
    test_stock = IntegerField('Test Stock ')
    personnel_number = IntegerField('Number of Personnel ')
    submit = SubmitField('Update')

class add_vaccinecenter(FF):
    hospital_id = IntegerField('Hospital ID ', validators=[DataRequired()])
    vaccine_stock = IntegerField('Vaccine Stock ')
    personnel_number = IntegerField('Number of Personnel ')
    submit = SubmitField('Add')

class update_vaccinecenter(FF):
    hospital_id = IntegerField('Hospital ID ')
    vaccine_stock = IntegerField('Vaccine Stock ')
    personnel_number = IntegerField('Number of Personnel ')
    submit = SubmitField('Update')

class add_personnel(FF):
    test_center_id = IntegerField('Test Center ID')
    vaccine_center_id = IntegerField('Vaccine Center ID')
    name = StringField('Name *', validators=[DataRequired(), Length(min = 2, max = 30),Optional()])
    surname = StringField('Surname *', validators=[DataRequired(), Length(min = 2, max = 30),Optional()])
    age = IntegerField('Age ', validators=[DataRequired()])
    sex = StringField('Sexuality', validators=[DataRequired(), Length(min = 1, max = 1)])
    telephone = StringField('Phone Number', render_kw={"placeholder": "+90xxxxxxxxxx"},validators=[Optional(), Length(min = 13, max = 13)])
    submit = SubmitField('Add')

class update_personnel(FF):
    test_center_id = IntegerField('Test Center ID')
    vaccine_center_id = IntegerField('Vaccine Center ID')
    name = StringField('Name', validators=[ Length(min = 2, max = 30),Optional()])
    surname = StringField('Surname', validators=[Length(min = 2, max = 30),Optional()])
    age = IntegerField('Age')
    sex = StringField('Sexuality', validators=[Length(min = 1, max = 1)])
    telephone = StringField('Phone Number', render_kw={"placeholder": "+90xxxxxxxxxx"},validators=[Optional(), Length(min = 13, max = 13)])
    submit = SubmitField('Update')

class add_patient(FF):
    test_center_id = IntegerField('Test Center ID')
    vaccine_center_id = IntegerField('Vaccine Center ID')
    name = StringField('Name *', validators=[DataRequired(), Length(min = 2, max = 30),Optional()])
    surname = StringField('Surname *', validators=[DataRequired(), Length(min = 2, max = 30),Optional()])
    age = IntegerField('Age ', validators=[DataRequired()])
    sex = StringField('Sexuality', validators=[DataRequired(), Length(min = 1, max = 1)])
    test_status = SelectField('Take Test?', choices = [('true','Yes'),('false','No')])
    vaccine_status = SelectField('Take Vaccine?', choices = [('true','Yes'),('false','No')])
    submit = SubmitField('Add')

class update_patient(FF):
    test_center_id = IntegerField('Test Center ID')
    vaccine_center_id = IntegerField('Vaccine Center ID')
    name = StringField('Name', validators=[Length(min = 2, max = 30),Optional()])
    surname = StringField('Surname', validators=[ Length(min = 2, max = 30),Optional()])
    age = IntegerField('Age')
    sex = StringField('Sexuality', validators=[ Length(min = 1, max = 1)])
    test_status = SelectField('Take Test?', choices = [('true','Yes'),('false','No')])
    vaccine_status = SelectField('Take Vaccine?', choices = [('true','Yes'),('false','No')])
    submit = SubmitField('Update')
    