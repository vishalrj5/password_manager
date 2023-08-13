from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import Users



class UserRegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=255, min_length=4)
    email = serializers.EmailField(max_length=255)
    first_name = serializers.CharField(max_length=255, min_length=4)
    last_name = serializers.CharField(max_length=255, min_length=2)
    is_active = serializers.BooleanField(default = True)
    password      = serializers.CharField(required=False )

    class Meta:
        model = Users
        fields = ['id','phone', 'password', 'email', 'first_name','last_name','is_active']

    def validate(self, attrs):
        phone = attrs.get('phone', '')
        email = attrs.get('email', '') 
        
        password = attrs.get('password', None)
        
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                {'phone': ('Phone number is already in use')})
            
        if password is not None and (len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?\'\"\\/~`' for char in password)):
            raise serializers.ValidationError({"password":('Password Contain 8 Characters, One Uppercase, One Lowercase, One Number and One Special Character')})    
            
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': ('email address is already in use')})
            
        return super().validate(attrs)

    def create(self, validated_data):
        request  = self.context.get('request', None)
        instance = Users()
        password = validated_data.get('password',None) 
        instance.email = validated_data.get('email',None)  
        instance.username = validated_data.get('email', None)
        instance.first_name = validated_data.get('first_name',None)  
        instance.last_name = validated_data.get('last_name',None)  
        instance.is_active = True
        instance.phone = validated_data.get('phone',None)    
        if password != '' and password is not None:
            instance.set_password(password) 
        instance.save()    
        return instance




class UserRegisterUpdateSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    password = serializers.CharField(max_length=65, min_length=8)
    username = serializers.CharField(max_length=255, min_length=4)
    confirm_password = serializers.CharField(max_length=65, min_length=8)

    class Meta:
        model = Users
        fields = ('password', 'username','pk')

    def validate(self, attrs):
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', None)
        pk = attrs.get('pk', None)

        if confirm_password != password:
            raise serializers.ValidationError(
                {'password_mismatch': ('password an confirm password are not match')})
        
        
        if not Users.objects.filter(pk=pk).exists():
            raise serializers.ValidationError(
                {'not_found': ('user not found in our system.')})
            
      
        return super().validate(attrs)
    
    

    def update(self):
        pk = self.data.get('pk')
        if pk:
            user = Users.objects.get(pk=pk)
            user.username = self.data.get('username')
            user.set_password(self.data.get('password'))
            user.is_active = True
            user.save()
            return True
        
        return False
        






class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = Users
        fields = ['username', 'password']


class OTPSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(max_length=255, min_length=4)

    class Meta:
        model = Users
        fields = ['otp']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
