from django import forms

class CSVSplitForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV file',
        help_text='Upload a .csv file with a header row'
    )
    output_prefix = forms.CharField(
        label='Output prefix',
        max_length=50,
        initial='split_file'
    )
    rows_per_file = forms.IntegerField(
        label='Rows per file',
        min_value=1,
        initial=1000
    )

    def clean_csv_file(self):
        f = self.cleaned_data['csv_file']
        if not f.name.lower().endswith('.csv'):
            raise forms.ValidationError('Please upload a .csv file')
        return f
