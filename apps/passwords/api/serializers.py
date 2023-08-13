from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from apps.passwords.api.encrypt import encrypt_and_save
from apps.passwords.models import UserPasswords
from django.contrib.auth.hashers import make_password

from apps.users.models import Users



class PasswordRegisterSerializer(serializers.ModelSerializer):
    user_passwod          = serializers.PrimaryKeyRelatedField(read_only=False,default=None, queryset=UserPasswords.objects.all(), required=False)
    user          = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Users.objects.all())
    password      = serializers.CharField(required=True)
    expiry        = serializers.IntegerField(required=True)
    view_users        = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=Users.objects.all(), required=True)
    edit_users        = serializers.PrimaryKeyRelatedField(read_only=False, many=True, queryset=Users.objects.all(), required=True)


    class Meta:
        model = UserPasswords
        fields = ['id', 'user', 'user_passwod', 'password', 'expiry', 'view_users', 'edit_users']

    def validate(self, attrs):
            
        return super().validate(attrs)

    def create(self, validated_data):

        request  = self.context.get('request', None)
        instance = UserPasswords()
        unhashed_password = encrypt_and_save(validated_data.get('password',None)) 
        instance.raw_password = validated_data.get('password',None)
        instance.password = make_password(validated_data.get('password',None))
        # instance.hashed_password = unhashed_password[1]
        print('unssssssss ', unhashed_password)
        instance.user = validated_data.get('user',None)    
        instance.expiry = validated_data.get('expiry',None)    
        view_users = validated_data.pop('view_users')
        instance.save()    

        for view_user in view_users:
            if view_user is not None:
                view_user.view_users.add(instance)
                
        edit_users = validated_data.pop('edit_users')
            
        for edit_user in edit_users:
            if edit_user is not None:
                edit_user.edit_users.add(instance)
                        
        return instance

    def update(self, instance, validated_data):
        try:
            request  = self.context.get('request', None)
            
            view = validated_data.pop('view_users')
            edit = validated_data.pop('edit_users')
            unhashed_password = encrypt_and_save(validated_data.get('password',None)) 
            instance.raw_password = validated_data.get('password',None)
            instance.password = make_password(validated_data.get('password',None))
            instance.expiry = validated_data.get('expiry',None)    

            view_users = instance.view_users.all()
            edit_users = instance.edit_users.all()

            destroy_view = list(set(list(view_users)).difference(view))
            destroy_edit = list(set(list(edit_users)).difference(edit))



                    
            instance.save()
            
            if instance is not None:    
                for vi in view:
                    if vi is not None:
                        vi.view_users.add(instance)
                for destroy_vi in destroy_view:
                    remove_vi_instance = destroy_vi
                    if remove_vi_instance is not None:
                        remove_vi_instance.view_users.remove(instance)
                        
                for vi in edit:
                    if vi is not None:
                        vi.edit_users.add(instance)
                for destroy_vi in destroy_edit:
                    remove_vi_instance = destroy_vi
                    if remove_vi_instance is not None:
                        remove_vi_instance.edit_users.remove(instance)        
            
        except Exception as e:
            print("exception on update is ", e)
            pass

        return instance

    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    