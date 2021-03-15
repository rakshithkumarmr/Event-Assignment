from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
  id = models.AutoField(primary_key=True)
  title = models.TextField(max_length=100)
  organizer = models.TextField(max_length=100)
  location = models.TextField(max_length=100)
  img= models.ImageField(upload_to="images")
  liked = models.ManyToManyField(User,default=None,blank=True,related_name='liked')
  datetime = models.DateTimeField(auto_now=True,null=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return self.user


Like_CHOICES = {
  ('Like','Like'),
  ('Unlike','Unlike')
}


class Like(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  post = models.ForeignKey(Event,on_delete=models.CASCADE)
  value = models.CharField(choices=Like_CHOICES,default='Like',max_length=10)

  def __str__(self):
    return str(self.post)