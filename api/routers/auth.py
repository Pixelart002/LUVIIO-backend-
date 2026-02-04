from fastapi import APIRouter
from fastapi.responses import HTMLResponse

# Router initialize karein
router = APIRouter()

# --- LOGIN PAGE HTML (Jo apne diya tha) ---
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Luviio - Secure Access</title>
  
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
  
  <style>
    :root { --bg: #030303; --card-bg: rgba(20, 20, 20, 0.6); --border: #222; --primary: #ffffff; --primary-fg: #000000; --text-muted: #888; --error: #ff3b30; --success: #34c759; }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background-color: var(--bg); background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px); background-size: 40px 40px; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; }
    .auth-card { width: 100%; max-width: 420px; padding: 40px; background: var(--card-bg); backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
    .header { text-align: center; margin-bottom: 25px; } .brand { font-size: 24px; font-weight: 800; letter-spacing: -1px; margin-bottom: 8px; display: inline-block; } .subtitle { color: var(--text-muted); font-size: 14px; }
    .social-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 25px; }
    .btn-social { display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 12px; color: white; cursor: pointer; transition: all 0.2s; font-size: 14px; font-weight: 500; }
    .btn-social:hover { background: rgba(255,255,255,0.1); border-color: #555; }
    .divider { display: flex; align-items: center; margin-bottom: 25px; color: var(--text-muted); font-size: 13px; } .divider::before, .divider::after { content: ""; flex: 1; height: 1px; background: var(--border); } .divider span { padding: 0 10px; }
    .input-group { margin-bottom: 16px; position: relative; } .input-wrapper { position: relative; }
    .input-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 18px; pointer-events: none; }
    input { width: 100%; padding: 14px 14px 14px 44px; background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; color: white; font-size: 15px; outline: none; transition: all 0.3s ease; }
    input:focus { border-color: #555; background: rgba(255,255,255,0.06); } .hp-field { display: none; visibility: hidden; opacity: 0; }
    .btn-primary { width: 100%; padding: 14px; background: var(--primary); color: var(--primary-fg); border: none; border-radius: 12px; font-weight: 600; cursor: pointer; margin-top: 10px; transition: transform 0.2s; }
    .btn-primary:active { transform: scale(0.98); } .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }
    .loader { display: none; width: 18px; height: 18px; border: 2px solid rgba(0,0,0,0.2); border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto; } @keyframes spin { to { transform: rotate(360deg); } }
    .status-msg { margin-top: 15px; padding: 12px; border-radius: 8px; font-size: 13px; display: none; align-items: center; gap: 8px; }
    .status-msg.error { background: rgba(255, 59, 48, 0.1); color: var(--error); border: 1px solid rgba(255, 59, 48, 0.2); }
    .status-msg.success { background: rgba(52, 199, 89, 0.1); color: var(--success); border: 1px solid rgba(52, 199, 89, 0.2); }
    .footer-text { margin-top: 24px; text-align: center; font-size: 14px; color: var(--text-muted); } .link { color: white; text-decoration: none; font-weight: 500; cursor: pointer; margin-left: 5px; }
  </style>
</head>
<body>
  <div class="auth-card">
    <div class="header">
      <div class="brand">LUVIIO</div>
      <div class="subtitle" id="formSubtitle">Secure Access Portal</div>
    </div>
    <div class="social-grid">
      <button class="btn-social" onclick="signInWithProvider('google')"><i class="ri-google-fill"></i> Google</button>
      <button class="btn-social" onclick="signInWithProvider('github')"><i class="ri-github-fill"></i> GitHub</button>
    </div>
    <div class="divider"><span>OR CONTINUE WITH</span></div>
    <form id="authForm" onsubmit="handleAuth(event)">
      <input type="text" id="_hp_check" class="hp-field" tabindex="-1" autocomplete="off">
      <div class="input-group"><div class="input-wrapper"><input type="email" id="email" placeholder="Email address" required autocomplete="email"><i class="ri-mail-line input-icon"></i></div></div>
      <div class="input-group"><div class="input-wrapper"><input type="password" id="password" placeholder="Password" required autocomplete="current-password"><i class="ri-lock-2-line input-icon"></i></div></div>
      <button type="submit" class="btn-primary" id="authBtn"><span id="btnText">Sign In</span><div class="loader" id="btnLoader"></div></button>
      <div class="status-msg" id="statusMsg"><i class="ri-error-warning-fill" id="statusIcon"></i><span id="statusText"></span></div>
      <div class="footer-text"><span id="footerPrompt">Don't have an account?</span><span class="link" onclick="toggleMode()" id="toggleLink">Sign up</span></div>
    </form>
  </div>
  <script>
    const SUPABASE_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SUPABASE_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    let isSignUp = false; let isProcessing = false;

    async function signInWithProvider(providerName) {
      try {
        const { data, error } = await supabaseClient.auth.signInWithOAuth({
          provider: providerName,
          options: { redirectTo: 'https://auth.luviio.in' } // Domain set kiya hua hai
        });
        if (error) throw error;
      } catch (error) { showStatus("Error logging in with " + providerName, "error"); }
    }

    function toggleMode() {
      isSignUp = !isSignUp;
      document.getElementById('formSubtitle').innerText = isSignUp ? "Create Secure Account" : "Secure Access Portal";
      document.getElementById('btnText').innerText = isSignUp ? "Create Account" : "Sign In";
      document.getElementById('footerPrompt').innerText = isSignUp ? "Already have an account?" : "Don't have an account?";
      document.getElementById('toggleLink').innerText = isSignUp ? "Log in" : "Sign up";
      hideStatus();
    }

    async function handleAuth(e) {
      e.preventDefault();
      if (isProcessing) return;
      if (document.getElementById('_hp_check').value) return; // Honeypot
      
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;
      if (password.length < 6) { showStatus("Password too short.", "error"); return; }
      
      setLoading(true);
      try {
        let result;
        if (isSignUp) {
          result = await supabaseClient.auth.signUp({ 
            email, password, options: { emailRedirectTo: 'https://auth.luviio.in' }
          });
        } else {
          result = await supabaseClient.auth.signInWithPassword({ email, password });
        }
        if (result.error) throw result.error;

        if (isSignUp && result.data.user && !result.data.session) {
           showStatus("Check email for verification link.", "success");
           document.getElementById('authForm').reset();
        } else {
           window.location.href = "https://luviio.in/dashboard";
        }
      } catch (error) {
        showStatus(error.message.includes("Invalid") ? "Invalid credentials" : error.message, "error");
      } finally { setLoading(false); }
    }

    function setLoading(state) {
      isProcessing = state;
      document.getElementById('btnText').style.display = state ? 'none' : 'block';
      document.getElementById('btnLoader').style.display = state ? 'block' : 'none';
      document.getElementById('authBtn').disabled = state;
      if(state) hideStatus();
    }
    function showStatus(msg, type) {
      const el = document.getElementById('statusMsg');
      el.style.display = 'flex'; el.className = `status-msg ${type}`;
      document.getElementById('statusText').innerText = msg;
      document.getElementById('statusIcon').className = type === 'error' ? "ri-error-warning-fill" : "ri-checkbox-circle-fill";
    }
    function hideStatus() { document.getElementById('statusMsg').style.display = 'none'; }
  </script>
</body>
</html>
"""

# Is URL par Login Page dikhega
@router.get("/", response_class=HTMLResponse)
async def get_login_page():
    return LOGIN_HTML