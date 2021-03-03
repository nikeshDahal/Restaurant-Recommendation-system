from django.db import models


class Restaurant(models.Model):
    title = models.CharField("title", max_length=255, blank=True, null=True)
    location = models.CharField("location", max_length=255, blank=True, null=True)
    city = models.CharField("city", max_length=255, blank=True, null=True)
    index = models.CharField("index", max_length=255, blank=True, null=True)
    image = models.ImageField(default='media/restropics/Jess.jpg', upload_to='media/restropics', null=True)

    def __str__(self):
        return self.title

    # class Meta:  
    #     db_table = "restaurant1"


class userreg(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    pwd = models.CharField(max_length=100, blank=True, null=True)
    # class Meta:
    #     db_table = "user_registration"
