from django import forms
from .models import AGM, BoardOfDirector, Category, Company, CompanyData, CompanyUrls, Floorsheet, News

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color'}),
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CompanyDataForm(forms.ModelForm):
    SOURCES = [
        ('', '---------'),
        ('Nepse', 'Nepse'),
        ('Share sansar', 'Share sansar'),
        ('Mero lagani', 'Mero lagani'),
    ]

    last_scrapped_from = forms.ChoiceField(choices=SOURCES)
    class Meta:
        model = CompanyData
        fields = '__all__'
        widgets = {
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'updated_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),        
        }

    def __init__(self, *args, **kwargs):
        super(CompanyDataForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class CompanyUrlsForm(forms.ModelForm):
    class Meta:
        model = CompanyUrls
        fields = ('nepse_url', 'mero_lagani_url', 'share_sansar_url')

    def __init__(self, *args, **kwargs):
        super(CompanyUrlsForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class BoardOfDirectorForm(forms.ModelForm):
    class Meta:
        model = BoardOfDirector
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(BoardOfDirectorForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class CompanyCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyCategoryForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class FloorsheetForm(forms.ModelForm):
    class Meta:
        model = Floorsheet
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FloorsheetForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class AGMForm(forms.ModelForm):
    class Meta:
        model = AGM
        fields = ['company', 'title', 'description', 'file', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AGMForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'