# ResumeAI — AI-Powered Resume Optimizer

> **Get Past the Robots. Land the Interview.**

ResumeAI is a full-stack SaaS platform that uses AI to optimize resumes for ATS (Applicant Tracking Systems). Upload your resume, paste a job description, and get an ATS-optimized resume in minutes.

## 🚀 Quick Start

```bash
# Clone the project
cd Projects/resume-optimizer

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the app
python main.py
```

Open http://localhost:8000 in your browser.

## 🏗️ Architecture

```
resume-optimizer/
├── main.py                  # FastAPI entry point
├── config.py                # Configuration / env vars
├── requirements.txt         # Python dependencies
├── routers/
│   ├── pages.py            # Page routes (/, /pricing, /blog, etc.)
│   ├── upload.py           # Resume upload & extraction
│   ├── payment.py          # Stripe checkout
│   └── webhooks.py         # Stripe webhook + AI processing
├── services/
│   ├── resume_parser.py    # PDF/DOCX/TXT text extraction
│   ├── ai_optimizer.py     # OpenAI API for resume optimization
│   ├── doc_generator.py    # DOCX & PDF generation
│   └── email_service.py    # SendGrid email delivery
├── templates/
│   ├── base.html           # Base template with Tailwind CSS
│   ├── index.html          # Landing page
│   ├── upload.html         # File upload form
│   ├── preview.html        # Resume preview before payment
│   ├── checkout.html       # Pricing & payment page
│   ├── success.html        # Payment success
│   ├── cancel.html         # Payment cancelled
│   ├── results.html        # Download optimized documents
│   ├── pricing.html        # Pricing page
│   ├── blog.html           # Blog listing
│   └── ...                 # Other pages
├── static/
│   ├── sitemap.xml
│   └── robots.txt
├── MARKETING.md            # Full marketing strategy
├── LAUNCH.md               # Launch checklist
├── ACQUISITION.md          # Customer acquisition playbook
└── .hermes/plans/          # Implementation plan
```

## 🔑 Environment Variables

Copy `.env.example` to `.env` and fill in:

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `STRIPE_SECRET_KEY` | Stripe secret key (sk_test_...) |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (pk_test_...) |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `SENDGRID_API_KEY` | SendGrid API key |
| `FROM_EMAIL` | From email address |

## 💰 Pricing

| Plan | Price | Features |
|------|-------|----------|
| **Basic** | $19 | ATS-optimized resume, DOCX + PDF |
| **Premium** | $39 | Everything in Basic + Cover letter + LinkedIn tips |

## 📈 Business Model

- Pay-per-resume pricing (no subscriptions)
- 90%+ gross margins (only cost is OpenAI API ~$0.50/resume)
- Global market (serves English-speaking job seekers worldwide)
- Stripe payments (accepts cards from 135+ countries)

## 🛠️ Tech Stack

- **Backend:** Python 3.11, FastAPI
- **Frontend:** Jinja2 templates, Tailwind CSS (CDN)
- **AI:** OpenAI GPT-4o
- **Payments:** Stripe Checkout
- **Email:** SendGrid
- **Document Generation:** python-docx, ReportLab

## 📊 Business Documents

- **[MARKETING.md](MARKETING.md)** — Full marketing strategy with SEO, channels, and conversion funnel
- **[LAUNCH.md](LAUNCH.md)** — Step-by-step launch checklist
- **[ACQUISITION.md](ACQUISITION.md)** — Customer acquisition playbook with scripts and templates

## 🔜 Roadmap

- [ ] Free ATS Score tool (lead magnet)
- [ ] User accounts & history
- [ ] Multi-language support
- [ ] API for white-label partners
- [ ] Chrome extension for LinkedIn job postings
- [ ] Mobile app