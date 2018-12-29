from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange, Regexp


class YTLinkForm(FlaskForm):
    link = StringField('Blah', validators=[DataRequired(), Regexp(regex='.*youtube.*', message="Please enter a YouTube Link")])
    submit = SubmitField('Continue')
    # recaptcha = RecaptchaField()


class WorksheetForm(FlaskForm):
    file_name = StringField('File name', validators=[DataRequired()])
    caption_lang = SelectField('Caption language', coerce=str, validators=[DataRequired()])
    skip_every = IntegerField('Skip ever n words', validators=[DataRequired(), NumberRange(min=1, max=20)], default=3)
    output_type = RadioField('File type', choices=[('txt', 'Plain Text'), ('pdf', 'PDF')], default='pdf')
    submit = SubmitField('Generate Worksheet')

    def validate(self):
        # print("!!!!!!!!") #kept for nostalgic reasons, took me a while to realize the error here...
        # print(self.caption_lang.data)
        # for v, _ in self.caption_lang.choices:
        #     print(v)

        res = super(WorksheetForm, self).validate()
        if res is False:
            print("FALSE")
            return res

        print(self.file_name.data)
        print(self.skip_every.data)
        print(self.output_type.data)
        print(self.caption_lang.data)
        return True
