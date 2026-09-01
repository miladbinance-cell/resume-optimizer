# ResumeAI — Agent Architecture 🤖

## 🎯 Vision
تبدیل شدن به **پلتفرم جامع career optimization** با AI agent‌های خودکار که کل مسیر job search رو پوشش میدن — از رزومه تا مصاحبه تا مذاکره حقوق.

---

## 🏗️ Agent Architecture

```
                        ResumeAI Platform
                              │
              ┌───────────────┼───────────────┐
              │               │               │
     ┌────────▼────────┐ ┌───▼────┐ ┌────────▼────────┐
     │  Content Agent   │ │Growth │ │  Analytics Agent │
     │  (تولید محتوا)    │ │ Agent  │ │  (تحلیل داده)    │
     └────────┬────────┘ └───┬────┘ └────────┬────────┘
              │               │               │
     ┌────────▼────────┐ ┌───▼────┐ ┌────────▼────────┐
     │  Support Agent   │ │SEO    │ │  Product Agent   │
     │  (پشتیبانی خودکار)│ │Agent   │ │  (بهبود محصول)    │
     └─────────────────┘ └────────┘ └─────────────────┘
```

### ۱. Content Agent (روزانه)
- تولید ۱ پست LinkedIn
- تولید ۲ پاسخ Reddit
- تولید ۳ توییت/X
- اسکرپت ۱ ویدیو TikTok
- هر جمعه: ۱ پست وبلاگ + newsletter

### ۲. Growth Agent (هفتگی)
- پیدا کردن ساب‌ردیت‌های مرتبط جدید
- مانیتور Mention ها
- پیدا کردن Influencer ها برای همکاری
- A/B test روی landing page
- آنالیز SEO و پیشنهاد keyword جدید

### ۳. Analytics Agent (روزانه)
- Track: visitors, conversions, revenue
- Alert: drop in conversion, spike in traffic
- Weekly report: рост/نزول + دلیل

### ۴. Support Agent (لحظه‌ای)
- پاسخ خودکار به سوالات متداول
- رسیدگی به refund request
- Follow-up: ۳ روز بعد "نتیجه گرفتی؟"

### ۵. SEO Agent (هفتگی)
- Research keyword جدید
- Optimize meta tags
- Build backlink opportunities
- Track ranking changes

### ۶. Product Agent (مستمر)
- A/B test قیمت‌ها
- آنالیز drop-off points
- پیشنهاد feature جدید بر اساس داده

---

## 🔄 Daily Schedule (Cron Jobs)

| ساعت (UTC) | Agent | وظیفه |
|-----------|-------|-------|
| ۰۶:۰۰ | Content | انتشار پست LinkedIn |
| ۰۸:۰۰ | Content | ارسال پاسخ Reddit |
| ۱۰:۰۰ | Analytics | جمع‌آوری آمار روز قبل |
| ۱۲:۰۰ | Content | انتشار توییت |
| ۱۴:۰۰ | SEO | Keyword research |
| ۱۸:۰۰ | Growth | Check mentions + alerts |
| ۲۰:۰۰ | Content | پست دوم LinkedIn |
| جمعه ۱۰:۰۰ | Content | Blog post + Newsletter |

---

## 🔧 پیاده‌سازی با Hermes Cron

همه Agentها با cronjob tool پیاده‌سازی میشن. هر Agent یه cron job با prompt مشخص + skills لازم.