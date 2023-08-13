
from rest_framework import serializers
from apps.passwords.api.encrypt import retrieve_and_decrypt

from apps.passwords.models import UserPasswords


class UserPasswordsSchema(serializers.ModelSerializer):
    password = serializers.SerializerMethodField()
    
    class Meta:
        model = UserPasswords
        fields = ['id','password','expiry','created_date','modified_date', 'view_users', 'edit_users']

    def get_password(self, obj):
        return obj.raw_password
        
