from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=255)
    years_of_experience = models.IntegerField()
    breed = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.breed})"

    class Meta:
        db_table = 'spy_cats'