from django.db import models

# Create your models here.
class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    usn =models.CharField(max_length=70,default="")
    phone=models.CharField(max_length=12,default="")
    desc=models.CharField(max_length=500,default="")
    timeStamp=models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return self.name

class Blogpost(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=50)
    content=models.TextField()
    author=models.CharField(max_length=50)
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)
    views=models.IntegerField(default=0)

    def __str__(self):
        return self.title +  "\n" 'by'  "\n" +self.author        

