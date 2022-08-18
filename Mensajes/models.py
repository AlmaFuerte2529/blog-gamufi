from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Mensajes(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    mensaje=models.TextField(max_length=250)
    autor=models.CharField(max_length=50)
    creado = models.DateTimeField(auto_now_add=True)
    leido=models.BooleanField(default=False)

    def _str_(self):
        return f"De: {self.autor}  -  Para: {self.nombre}"