import requests
from django.http import JsonResponse
from django.conf import settings

def hemis_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing code"}, status=400)

    # 1. Access token olish
    token_response = requests.post("https://hstudent.nuu.uz/oauth/token", data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:3000/api/auth/callback/hemis",
        "client_id": settings.HEMIS_CLIENT_ID,
        "client_secret": settings.HEMIS_CLIENT_SECRET,
    })

    if token_response.status_code != 200:
        return JsonResponse({"error": "Token olishda xatolik", "details": token_response.json()}, status=400)

    token_data = token_response.json()
    access_token = token_data.get("access_token")

    # 2. Foydalanuvchi ma'lumotlarini olish
    user_response = requests.get(
        "https://hstudent.nuu.uz/api/user",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if user_response.status_code != 200:
        return JsonResponse({"error": "User ma'lumot olishda xatolik", "details": user_response.json()}, status=400)

    user_data = user_response.json()

    # 3. Test uchun foydalanuvchini chiqarish
    return JsonResponse({"user": user_data})
