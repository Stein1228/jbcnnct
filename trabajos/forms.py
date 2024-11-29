from django import forms
from usuarios.models import Trabajo, Postulacion, Habilidades, Region, Comuna

class TrabajoForm(forms.ModelForm):
    habilidades = forms.ModelMultipleChoiceField(
        queryset=Habilidades.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        empty_label="Selecciona una región"
    )

    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        required=True,
        empty_label="Selecciona una comuna"
    )

    class Meta:
        model = Trabajo
        fields = [
            'titulo', 
            'descripcion',
            'presupuesto_minimo',
            'presupuesto_maximo',
            'region',
            'comuna',
            'habilidades'
        ]

    def __init__(self, *args, **kwargs):
        super(TrabajoForm, self).__init__(*args, **kwargs)
        
        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:  
            if self.instance.region:
                self.fields['comuna'].queryset = self.instance.region.comunas.order_by('nombre')
                self.fields['comuna'].initial = self.instance.comuna 

    def clean(self):
        cleaned_data = super().clean()
        habilidades = cleaned_data.get('habilidades')
        
        if not habilidades or habilidades.count() < 1:
            raise forms.ValidationError("Debes seleccionar al menos una habilidad.")
            
        return cleaned_data


class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['comentario']  # Incluye otros campos si es necesario