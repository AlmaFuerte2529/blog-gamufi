from django import forms


class FormMensajes(forms.Form):
    nombre = forms.CharField(label="Para", max_length=50, disabled = True, required=False)
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":70}))
    autor = forms.CharField(max_length=50, disabled = True, required=False)


