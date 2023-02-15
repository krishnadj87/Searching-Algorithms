
from rest_framework import serializers
from .models import Employee2

# StudentSerializer class
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model  =  Employee2
        fields = ('name','age', 'salary', 'email')
