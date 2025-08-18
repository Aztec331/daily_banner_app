from rest_framework import serializers
from .models import CustomUser, CompanyDetails
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = ['name','address','phone','email']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'phone', 'username', 'password', 'user_type']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone(self, value):
        import re
        pattern = r'^\+91\d{10}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone number must start with +91 and be followed by exactly 10 digits.")
        return value

    def create(self, validated_data):
        user_type = validated_data.get('user_type', 'user')
        company_data = validated_data.pop('company_details', None)

        # ✅ explicitly pass user_type
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            user_type=user_type
        )

        # ✅ if admin → mark as staff
        if user_type == 'admin':
            user.is_staff = True
            user.save()

        if company_data:
            company = CompanyDetails.objects.create(**company_data)
            user.company_details = company
            user.save()

        return user

        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email','phone', 'username', 'name', 'profile_image','user_type']
        read_only_fields = ['id','phone', 'email', 'username', 'user_type']  # 🔐 Locked fields

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email,password=password)
            if not user:
                raise serializers.ValidationError("Invalid Credentials.")
        else:
            raise serializers.ValidationError("Both email and password are required.")
        
        data['user'] = user
        return data

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','password','name', 'phone', 'profile_image']
        extra_kwargs = {
            'password': {'write_only':True, 'required':False},
            'profile_image':{'required':False},
            'phone':{'required':False},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)

        if 'profile_image' in validated_data:
            instance.profile_image = validated_data.get('profile_image')

        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance