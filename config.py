import os
from dotenv import load_dotenv

load_dotenv()

# AI Provider — supports OpenAI direct OR OpenRouter
# Set OPENROUTER_API_KEY to use OpenRouter, or OPENAI_API_KEY for direct OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o")
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://openrouter.ai/api/v1")

# Determine which key and URL to use
if OPENROUTER_API_KEY:
    AI_API_KEY = OPENROUTER_API_KEY
    AI_BASE_URL = os.getenv("AI_BASE_URL", "https://openrouter.ai/api/v1")
elif OPENAI_API_KEY:
    AI_API_KEY = OPENAI_API_KEY
    AI_BASE_URL = None  # Use OpenAI default
else:
    AI_API_KEY = ""
    AI_BASE_URL = None

# Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

# NowPayments (Crypto)
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY", "")
NOWPAYMENTS_IPN_SECRET = os.getenv("NOWPAYMENTS_IPN_SECRET", "")
NOWPAYMENTS_CURRENCY = os.getenv("NOWPAYMENTS_CURRENCY", "usdt")  # usdt, btc, eth, etc.

# Pricing (in USD)
PRICE_RESUME_OPTIMIZE = 19  # $19
PRICE_PREMIUM = 39  # $39 (resume + cover letter + LinkedIn)
# Stripe needs cents, NowPayments needs dollars
PRICE_RESUME_OPTIMIZE_CENTS = 1900
PRICE_PREMIUM_CENTS = 3900

# Email — Gmail SMTP
GMAIL_USER = os.getenv("GMAIL_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", GMAIL_USER)

# App
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Upload
MAX_UPLOAD_SIZE_MB = 10
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")