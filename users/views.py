import requests
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User   # Django User modeli
from django.contrib.auth import login

def hemis_login(request):
    """
    1. Login bosqichida foydalanuvchiga Hemis authorization URL qaytariladi
    """
    url = (
        f"{settings.HEMIS_AUTH_URL}"
        f"?response_type=code"
        f"&client_id={settings.HEMIS_CLIENT_ID}"
        f"&redirect_uri={settings.HEMIS_REDIRECT_URI}"
    )
    return JsonResponse({"auth_url": url})


def hemis_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing code"}, status=400)

    # 1️⃣ Token olish
    try:
        token_response = requests.post(
            settings.HEMIS_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": settings.HEMIS_REDIRECT_URI,
                "client_id": settings.HEMIS_CLIENT_ID,
                "client_secret": settings.HEMIS_CLIENT_SECRET,
            },
            timeout=10
        )
        token_response.raise_for_status()
        token_data = token_response.json()
    except Exception as e:
        return JsonResponse({"error": "Token olishda xatolik", "details": str(e)}, status=400)

    access_token = token_data.get("access_token")
    if not access_token:
        return JsonResponse({"error": "Access token topilmadi", "details": token_data}, status=400)

    # 2️⃣ Foydalanuvchi ma’lumotlarini olish
    try:
        user_response = requests.get(
            settings.HEMIS_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        user_response.raise_for_status()
        user_data = user_response.json()
    except Exception as e:
        return JsonResponse({"error": "User ma’lumot olishda xatolik", "details": str(e)}, status=400)

    # 3️⃣ Django User yaratish yoki olish
    # Hemis login field sifatida ishlatiladi
    username = user_data.get("login")
    email = user_data.get("email") or f"{username}@hemis.local"
    first_name = user_data.get("firstname") or user_data.get("name").split()[0]
    last_name = user_data.get("surname") or user_data.get("name").split()[-1]

    user, created = User.objects.get_or_create(username=username, defaults={
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
    })

    # 4️⃣ Django login qilish (session)
    login(request, user)

    # 5️⃣ Natijani qaytarish
    return JsonResponse({
        "message": "Foydalanuvchi login qilindi",
        "user": {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        "token": token_data
    })


