from rest_framework import serializers
from .models import DepositProducts
from .models import DepositOptions

class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta():
        model = DepositProducts
        fields = '__all__'
        
class DepositOptionsSerializer(serializers.ModelSerializer):
    class Meta():
        model = DepositOptions
        fields = '__all__'  # 모든 필드를 사용하도록 설정
        read_only_fields = ('fin_prdt_cd',) 