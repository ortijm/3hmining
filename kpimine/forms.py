from django import forms


class AlbumForm(forms.Form):
    movement_total = forms.IntegerField(blank=True)
    extraction = forms.IntegerField(blank=True)
    min_extracted = forms.IntegerField(blank=True)
    min_plant = forms.IntegerField(blank=True)
    law_cu_plant = forms.IntegerField(blank=True)
    as_ppm = forms.IntegerField(blank=True)
