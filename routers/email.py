from fastapi import FastAPI, Request, HTTPException
import resend
import os
from pydantic import BaseModel
from typing import Optional, Any

app = FastAPI()

# ---------------------------------------------------------
# CONFIGURATION
# Koyeb ke Settings me RESEND_API_KEY set karna hoga
# ---------------------------------------------------------
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

if not RESEND_API_KEY:
    print("WARNING: RESEND_API_KEY is missing!")

resend.api_key = RESEND_API_KEY

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@app.get("/")
def health_check():
    """Koyeb health check ke liye"""
    return {"status": "healthy", "service": "Luviio Emailer"}

@app.post("/webhook/send-email")
async def handle_supabase_webhook(request: Request):
    try:
        # 1. Supabase se data pakdo
        payload = await request.json()
        print(f"Event Received: {payload}")

        # 2. 'record' aur 'email' nikalo
        record = payload.get('record', {})
        user_email = record.get('email')

        # Safety Check
        if not user_email:
            return {"status": "skipped", "message": "No email found in record"}

        print(f"Preparing to send email to: {user_email}")

        # 3. Email Content (Responsive HTML)
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f9f9f9; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 40px auto; background: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
                .btn { display: inline-block; background-color: #000000; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: 600; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 style="margin-top: 0; color: #000;">LUVIIO</h2>
                <h3 style="color: #333;">You’re in. Welcome to the future of listings.</h3>
                <p style="color: #555; line-height: 1.6;">Hi there,</p>
                <p style="color: #555; line-height: 1.6;">You have successfully secured your spot on the exclusive waitlist for Luviio.</p>
                <p style="color: #555; line-height: 1.6;">The current marketplace ecosystem faces a critical trust deficit. We are rebuilding the foundation. You are now part of a select group waiting for the new <strong>Operating System for Listings</strong>.</p>
                <a href="https://x.com/LUVIIO_in" class="btn">Follow updates on X</a>
                <p style="margin-top: 30px; font-size: 12px; color: #999;">&copy; 2026 Luviio Technologies.</p>
            </div>
        </body>
        </html>
        """

        # 4. Send Email via Resend
        params = {
            "from": "Luviio Team <no-reply@luviio.in>",
            "to": [user_email],
            "subject": "You’re in. Welcome to the future of listings.",
            "html": html_content,
        }

        email = resend.Emails.send(params)
        print("Email Sent! ID:", email)

        return {"status": "success", "email_id": email}

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # Hum 200 hi return karenge taaki Supabase bar-bar retry na kare
        return {"status": "error", "details": str(e)}