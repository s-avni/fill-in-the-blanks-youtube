from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, NumberRange


class YTLinkForm(FlaskForm):
    link = StringField('Blah', validators=[DataRequired()])
    submit = SubmitField('Continue')

    def validate(self):
        res = super(YTLinkForm, self).validate()
        if res is False:
            return res

        # todo: it's not getting here, because it fals in StringValidation and False is returned
        # todo: So the error is silent. I'd prefer it to be noticed
        # todo: would be nice if there was the same alert as when we have nothing inputed
        if self.link.data.isspace():
            print("yes")
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
    output_type = RadioField('File type', choices=[('txt', 'Plain Text'), ('pdf', 'PDF')], default='pdf')
    submit = SubmitField('Generate Worksheet')

    def validate(self):
        # print("!!!!!!!!")
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
