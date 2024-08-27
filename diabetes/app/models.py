from django.db import models

# Create your models here.
class Patients_Details(models.Model):
    p_id = models.BigAutoField(primary_key=True)
    p_fname = models.CharField(max_length=50)
    p_lname = models.CharField(max_length=50)
    contact_no = models.PositiveIntegerField()
    age = models.PositiveIntegerField()
    pregnancies = models.PositiveIntegerField()
    glucose = models.PositiveIntegerField()
    blood_pressure = models.PositiveIntegerField()
    skin_thikness = models.PositiveIntegerField()
    insulin = models.PositiveIntegerField()
    bmi = models.CharField(max_length=6)
    dpf = models.CharField(max_length=6)
    prediction = models.CharField(max_length=50)
    precautions = models.CharField(max_length=500)
    date = models.DateField()

    def __str__(self):
        return self.p_fname + " " + self.p_lname
