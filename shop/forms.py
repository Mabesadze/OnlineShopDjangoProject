from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ContactForm(forms.Form):
	"""Simple contact form used in the shop app.

	This form was previously deleted, which caused an import error when the
	views module tried to import it (see the stack trace in the development
	server output). Re‑adding it resolves the ``ImportError: cannot import
	name 'ContactForm'`` and allows the project to start.
	"""

	name = forms.CharField(
		max_length=100,
		widget=forms.TextInput(attrs={'placeholder': 'Your full name'})
	)
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={'placeholder': 'your.email@example.com'})
	)
	subject = forms.CharField(
		max_length=200,
		widget=forms.TextInput(attrs={'placeholder': 'Subject of your message'})
	)
	message = forms.CharField(
		widget=forms.Textarea(attrs={
			'placeholder': 'Your message here...',
			'rows': 5,
		})
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-3'),
				Column('email', css_class='form-group col-md-6 mb-3'),
				css_class='form-row',
			),
			'subject',
			'message',
			Submit('submit', 'Send Message', css_class='btn btn-primary'),
		)

