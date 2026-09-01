"""
Email Service
Sends results email to customer after successful payment.
In Iran, SMTP ports are blocked. Email delivery is optional — 
the results page with direct download is the primary delivery method.
"""
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import GMAIL_USER, GMAIL_APP_PASSWORD, FROM_EMAIL


async def send_results_email(
    to_email: str,
    download_url: str,
    file_id: str,
    plan: str = "basic",
) -> bool:
    """Try to send email. Gracefully skip if SMTP is blocked (Iran)."""

    if not to_email or not GMAIL_USER or not GMAIL_APP_PASSWORD:
        return False

    plan_name = "ATS-Optimized Resume" if plan == "basic" else "Resume + Cover Letter + LinkedIn Tips"
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px;">
        <h1 style="color: #2563eb;">Your Optimized Resume is Ready! 🎯</h1>
        <div style="background: #f0f9ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>📋 {plan_name}</h2>
            <p>✅ ATS keyword matching | ✅ Quantified achievements | ✅ Clean formatting</p>
        </div>
        <a href="{download_url}" style="display: inline-block; background: #2563eb; color: white; 
           padding: 14px 32px; text-decoration: none; border-radius: 6px; font-size: 16px;">
            📥 Download Your Documents
        </a>
        <p style="color: #999; font-size: 12px; margin-top: 30px;">ResumeAI</p>
    </div>"""

    msg = MIMEMultipart("alternative")
    msg["From"] = FROM_EMAIL or GMAIL_USER
    msg["To"] = to_email
    msg["Subject"] = "Your Optimized Resume is Ready!"
    msg.attach(MIMEText(html, "html"))

    # Try SMTP — will fail in Iran due to port blocks, but works on deployed servers
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=10) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        print(f"✅ Email sent to {to_email}")
        return True
    except Exception:
        # SMTP blocked (Iran) — user gets download link on results page instead
        return False