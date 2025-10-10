from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ['id','username','email','first_name','last_name','bio','profile_picture','followers_count']
        read_only_fields = ['id','followers_count']


    def get_followers_count(self, obj):
        return obj.followers.count()



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


    class Meta:
        model = User
        fields = ['username','email','password']


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
       )
        return user