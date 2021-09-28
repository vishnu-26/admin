from rest_framework import serializers
from django.contrib.auth.hashers import make_password,check_password
from .models import User,Role,Permission
#import bcrypt

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields='__all__'


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True)

    class Meta:
        model=Role
        fields='__all__'

    
    def create(self,validated_data):
        permissions = validated_data.pop('permissions')
        role = Role.objects.create(**validated_data)

        for permission in permissions:
            print(permission['name'])
            _permission ,created= Permission.objects.get_or_create(name=permission['name'])
            role.permissions.add(_permission)
        
        return role


#    Here role is the instance which is to be updated
    def update(self,role,validated_data):
        permissions = validated_data.pop('permissions')

        role.name= validated_data['name']
        
        permissions_list=[]
        for permission in permissions:
            _permission ,created= Permission.objects.get_or_create(name=permission['name'])
#            print(created)
            permissions_list.append(_permission)
        
        role.permissions.set(permissions_list)
        return role
        
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
        extra_kwargs={
            'password':{'write_only': True,'read_only': False}
        }

    def create(self,user_data):
        password = user_data.pop('password')
        instance = self.Meta.model(**user_data)
        hashed_password = make_password(password)
    
        if hashed_password is not None:
            instance.password=hashed_password

        instance.save()
        return instance
