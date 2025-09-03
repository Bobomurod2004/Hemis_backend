# your_app_name/cron.py
import requests
import logging
import json
from datetime import datetime
from django.conf import settings

# Logger sozlash
logger = logging.getLogger('api_fetcher')


def fetch_api_data():
    """
    Har kuni soat 2:00da API dan ma'lumot olish funksiyasi
    """
    api_url = "https://student.uzswlu.uz/rest/v1/public/stat-employee"  # sizning API URL'ingiz

    logger.info(f"API ma'lumot olish jarayoni boshlandi: {datetime.now()}")

    try:
        # API ga so'rov yuborish
        headers = {
            'User-Agent': 'Django Cron Job',
            'Content-Type': 'application/json',
            # Agar API key kerak bo'lsa:
            # 'Authorization': 'Bearer YOUR_API_KEY'
        }

        response = requests.get(api_url, headers=headers, timeout=30)

        # Status kodini tekshirish
        if response.status_code == 200:
            data = response.json()
            logger.info(f"API dan muvaffaqiyatli ma'lumot olindi. Ma'lumot hajmi: {len(str(data))} bytes")

            # Ma'lumotni saqlash yoki qayta ishlash
            process_api_data(data)

        else:
            logger.error(f"API xatolik qaytardi. Status kod: {response.status_code}")
            logger.error(f"Xatolik matni: {response.text}")

    except requests.exceptions.ConnectionError:
        logger.error("Internet ulanishida xatolik")
    except requests.exceptions.Timeout:
        logger.error("API so'rovi vaqt tugadi (timeout)")
    except requests.exceptions.RequestException as e:
        logger.error(f"API so'rovida umumiy xatolik: {str(e)}")
    except json.JSONDecodeError:
        logger.error("API javobini JSON formatida o'qib bo'lmadi")
    except Exception as e:
        logger.error(f"Kutilmagan xatolik: {str(e)}")

    logger.info(f"API ma'lumot olish jarayoni tugadi: {datetime.now()}")


def process_api_data(data):
    """
    API dan olingan ma'lumotni qayta ishlash
    """
    try:
        # Bu yerda ma'lumotni database ga saqlash yoki
        # boshqa operatsiyalar bajarish mumkin

        # Misol: ma'lumot sonini log qilish
        if isinstance(data, list):
            logger.info(f"Jami {len(data)} ta element qayta ishlandi")
        elif isinstance(data, dict):
            logger.info(f"Ma'lumot kalitlari: {list(data.keys())}")

        # Ma'lumotni faylga saqlash (ixtiyoriy)
        save_data_to_file(data)

    except Exception as e:
        logger.error(f"Ma'lumot qayta ishlashda xatolik: {str(e)}")


def save_data_to_file(data):
    """
    Ma'lumotni JSON faylga saqlash
    """
    try:
        filename = f"{settings.BASE_DIR}/logs/api_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Ma'lumot faylga saqlandi: {filename}")
    except Exception as e:
        logger.error(f"Faylga saqlashda xatolik: {str(e)}")