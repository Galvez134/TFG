from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class ShowProjectsForm(forms.Form):
    projects = forms.CharField()

class LoginForm(forms.Form):
    username = forms.CharField(help_text="Enter your username")
    password = forms.CharField(help_text="Enter your password")

class SignupForm(forms.Form):
    username = forms.CharField(help_text="Enter your username")
    password = forms.CharField(help_text="Enter your password")

class CreateProjectForm(forms.Form):
    projectName = forms.CharField(help_text="Enter the project name")

class SelectProjectForm(forms.Form):
    projectName = forms.CharField(help_text="Enter the project name")

class UpdateSelectedProjectForm(forms.Form):
    selectedProject = forms.CharField(help_text="Enter the project name")

class UpdatePaperStatsForm(forms.Form):
    file = forms.FileField()
