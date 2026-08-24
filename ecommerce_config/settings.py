import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# 1. BẢO MẬT & DEBUG (Lấy từ file .env)
# ==========================================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-tạm-thời')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['*']


# ==========================================
# 2. KHAI BÁO APP
# ==========================================
INSTALLED_APPS = [
    # Mặc định của Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Thư viện bên thứ 3 đã cài
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Các app của Team
    'accounts',
    'products',
    'cart',
    'orders',
    'pages',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# ==========================================
# 3. MIDDLEWARE & URLS
# ==========================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce_config.urls'
WSGI_APPLICATION = 'ecommerce_config.wsgi.application'

# ==========================================
# 4. TEMPLATES (Giao diện)
# ==========================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Trỏ tới thư mục templates gốc
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==========================================
# 5. DATABASE (Kết nối MySQL qua .env)
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='ecommerce_fashion_db'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}

# ==========================================
# 6. PASSWORD VALIDATORS
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ==========================================
# 7. NGÔN NGỮ & THỜI GIAN
# ==========================================
LANGUAGE_CODE = 'vi'  # Đổi sang Tiếng Việt cho dễ dùng
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# ==========================================
# 8. STATIC & MEDIA FILES
# ==========================================
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# 9. DEFAULT AUTO FIELD
# ==========================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LƯU Ý CHO TEAM: Nếu dùng Custom User Model thì bỏ comment dòng dưới
AUTH_USER_MODEL = 'accounts.User'