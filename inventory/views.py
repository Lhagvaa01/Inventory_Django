from admin_soft.utils import JsonResponse
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.timezone import now
from .models import *
from .serializers import *
from datetime import timedelta
from rest_framework import status


@api_view(['POST'])
def register_user(request):
    data = request.data
    try:
        register = data.get('register')
        username = data.get('username')
        password = data.get('password')

        # Регистерээр компанийн бүртгэл олох
        company = Company.objects.get(register=register)

        # Апп ашиглах хугацааг автоматаар 1 сар (30 хоног) тохируулах
        app_usage_period = now() + timedelta(days=30)

        # Хэрэглэгч үүсгэх
        user = User.objects.create(
            username=username,
            company=company,
            app_usage_period=app_usage_period
        )
        user.password = password  # Нууц үг хадгалах
        user.save()

        return Response({'special_code': user.special_code}, status=201)
    except Company.DoesNotExist:
        return Response({'error': 'Company with this register not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=400)


# @api_view(['POST'])
# def login_user(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     imei_code = request.data.get('imei_code')
#
#     try:
#         user = User.objects.get(username=username, password=password)
#         if user.is_app_active():
#             if user.imei_code is None or user.imei_code == imei_code:
#                 user.imei_code = imei_code
#                 user.last_login = now()
#                 user.save()
#                 return Response({'message': 'Login successful', 'special_code': user.special_code})
#             else:
#                 return Response({'error': 'IMEI mismatch'}, status=403)
#         else:
#             return Response({'error': 'App usage period expired'}, status=403)
#     except User.DoesNotExist:
#         return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
def login_user(request):
    print("Request data:", request.data)  # Log the request
    username = request.data.get('username')
    password = request.data.get('password')
    imei_code = request.data.get('imei_code')

    # Your existing logic
    return JsonResponse({'message': 'Login successful'})


@api_view(['POST'])
def upload_inventory(request):
    try:
        # `special_code`-ийг хүсэлтээс авна
        special_code = request.data.get('special_code')
        if not special_code:
            return Response({"error": "Special code not provided"}, status=400)

        # Хэрэглэгчийг `special_code`-оор таних
        try:
            user = User.objects.get(special_code=special_code)
        except User.DoesNotExist:
            return Response({"error": "Invalid special code"}, status=403)

        # Оруулсан inventories-г хадгалах
        inventories = request.data.get('inventories', [])
        for item in inventories:
            serializer = InventorySerializer(data=item)
            if serializer.is_valid():
                serializer.save(user=user)  # `user`-г автоматаар тохируулна
            else:
                return Response(serializer.errors, status=400)

        return Response({"success": "All data saved!"}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['GET'])
def merge_inventory(request):
    inventories = Inventory.objects.all()
    file_path = 'merged_inventory.txt'
    with open(file_path, 'w') as file:
        for inv in inventories:
            file.write(f"{inv.barcode}, {inv.quantity}\n")
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='merged_inventory.txt')
