from django.db import models
from django.urls import reverse
class Home(models.Model):
    movieId = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    userid = models.CharField(max_length=200,blank=True)
    genre = models.CharField(max_length=200,blank=True)
    release_year = models.CharField(max_length=200,blank=True)
    country = models.CharField(max_length=200, blank=True)
    image = models.URLField( max_length=500, blank=True )
    description = models.CharField(max_length=500, blank= True)
    path = models.URLField(max_length=500, blank=True)
    rating = models.CharField(max_length=50,blank=True)
    date = models.DateTimeField(auto_now=True)



    def get_movie_url(self):
        return reverse('details', args=[self.id])
    def __str__(self):
       return self.title

    class Meta:
        verbose_name = 'Home'
        verbose_name_plural='Home'
class ExcelFile(models.Model):
    file =models.FileField(upload_to='excel')
