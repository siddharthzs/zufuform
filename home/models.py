from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime
# Create your models here.
class BlankForm(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    formtimer = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        temp = slugify(self.title)
        if len(BlankForm.objects.filter(slug=temp)) > 0:
            temp = temp + "-" + temp  
        self.slug = temp
        super(BlankForm, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('web-detail', kwargs={'slug': self.slug})


class UserResponse(models.Model):
    formid = models.ForeignKey(BlankForm, on_delete=models.CASCADE)
    responder = models.ForeignKey(User, on_delete=models.CASCADE)

    response = models.TextField()
    active = models.BooleanField(default=True)


class LogTable(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    formslug = models.SlugField()
    inital_time = models.DateTimeField(default=datetime.datetime.now(datetime.timezone.utc))
