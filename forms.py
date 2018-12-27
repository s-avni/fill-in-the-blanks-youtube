from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange
from flask import flash

class YTLinkForm(FlaskForm):
    link = StringField('Blah', validators=[DataRequired()])
    submit = SubmitField('Continue')

    def validate(self):
        res = super(YTLinkForm, self).validate()
        if res is False:
            return res

        if self.link.data.strip() == "": #todo: not getting called
            self.link.errors.append('Nothing entered')
            flash('Please insert link')
            return False

        if not "youtube" in self.link.data:
            self.link.errors.append('Not a YouTube link')
            flash('Not a YouTube link')
            return False

        return True


class WorksheetForm(FlaskForm):
    file_name = StringField('File name', validators=[DataRequired()])
    caption_lang = SelectField('Caption language', coerce=str, validators=[DataRequired()])
    skip_every = IntegerField('Skip ever n words', validators=[DataRequired(), NumberRange(min=1, max=20)], default=3)
    output_type = RadioField('File type', choices=[('txt','Plain Text'), ('pdf','PDF')], default='pdf')
    submit = SubmitField('Generate Worksheet')

    def validate(self):
        print("!!!!!!!!")
        print(self.caption_lang.data)
        for v, _ in self.caption_lang.choices:
            print(v)

        res = super(WorksheetForm, self).validate()
        if res is False:
            print("FALSE")
            return res

        print(self.file_name.data) #working
        print(self.skip_every.data) #working
        print(self.output_type.data) #working
        print(self.caption_lang.data) #not working
        return True