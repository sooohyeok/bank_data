from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DepositProducts
from .serializers import DepositProductsSerializer, DepositOptionsSerializer
import requests


# Create your views here.
# @api_view(['GET'])
# def index(request):
#     api_key = settings.API_KEY
#     url =  f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'

#     response = requests.get(url).json()

#     return Response(response)

@api_view(['GET'])
def save(request): # 'save-deposit-products/
    api_key = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={api_key}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()
    depo = response.get('result').get('baseList')
    op = response.get('result').get('optionList')
    for item in depo:
        try:
            deposit_data = {
                'fin_prdt_cd' : item.get('fin_prdt_cd'),
                'kor_co_nm' : item.get('kor_co_nm'),
                'fin_prdt_nm' : item.get('fin_prdt_nm'),
                'etc_note' : item.get('etc_note'),
                'join_deny' : item.get('join_deny'),
                'join_member' : item.get('join_member'),
                'join_way' : item.get('join_way'),
                'spcl_cnd' : item.get('spcl_cnd'),
            }
            serializer = DepositProductsSerializer(data=deposit_data)
            if serializer.is_valid(raise_exception=True): # 데이터 잘 못 넣었니?
                    serializer.save()
        except:
             pass
    for item in op:
        options_data = {
            'product': DepositProducts.objects.filter(fin_prdt_cd=item.get('fin_prdt_cd'))[0].pk,
            'fin_prdt_cd' : item.get('fin_prdt_cd'),
            'intr_rate_type_nm' : item.get('intr_rate_type_nm'),
            'intr_rate' : item.get('intr_rate') or -1,
            'intr_rate2' : item.get('intr_rate2'),
            'save_trm' : item.get('save_trm'),
        }
        serializer = DepositOptionsSerializer(data=options_data)
        if serializer.is_valid(raise_exception=True): # 데이터 잘 못 넣었니?
                serializer.save()

    return JsonResponse({'message' : 'okay'})
    
@api_view(['GET', 'POST'])
def deposit(request):
    if request.method == 'GET':
        products = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(products, many=True)
        return Response(serializer.data)
    
        
    if request.method == 'POST':
        serializer = DepositProductsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
     
    
@api_view(['GET'])
def options(request):
    pass

@api_view(['GET'])
def top_rate(request):
    pass