from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.template.defaultfilters import slugify
from django.urls import reverse

class House(models.Model):
    address = models.CharField(max_length=150, unique=True)
    location = models.JSONField(default = dict, unique=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="owner")
    residents = models.ManyToManyField(User, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    image = models.ImageField(default='house-default.jpg', upload_to='house_pics')
    
    def __str__(self):
        return self.address
        
    def get_absolute_url(self):
        return reverse("house-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.address)
        
        super().save(*args, **kwargs)
        # obj, created = Profile.objects.update_or_create(
        # user=self.owner, defaults={"house": self}
        # )
        
        # Add the house to the user profile of the owner
        self.owner.profile.house = self
        self.owner.profile.save()
        
        # Add the house to each user profile in the residents list
        for user in self.residents.all():
            user.profile.house = self
            user.profile.save()
            
        # Remove house from user profile if they are not a resident anymore
        for user in User.objects.all():
            if user.profile.house == self and user != self.owner and user not in self.residents.all():
                print(user.profile)
                user.profile.house = None
                user.profile.save()
                print(user.profile.house)
                
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            

        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    house = models.ForeignKey(House, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f'{self.user.username} Profile'
      
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
