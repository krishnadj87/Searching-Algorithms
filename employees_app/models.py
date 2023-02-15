from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name).upper()  # receiving in upper case
    

class Employee(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    dept  = models.ForeignKey(Department, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField()
    join_date = models.DateTimeField(auto_now_add=True)
    image     = models.ImageField(upload_to='Employee/images')

# user profile model here extend
class Profile(models.Model):
    """User Profile Model for adding information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio  = models.TextField(default='Write details/description about your self. Like you can also describe your past experiences as well',   max_length=500)
    pic  = models.ImageField(upload_to='Profile/images')
    address = models.CharField(max_length=78)


######## API APP Model Here #####


class Employee2(models.Model):
    name = models.CharField(max_length=77)
    email = models.EmailField(unique=True)
    salary = models.PositiveIntegerField()