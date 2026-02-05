from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

MAGIC_LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <title>Login - Luviio</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">

  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

  <style>
    :root { 
      --bg: #050505; --surface: rgba(20, 20, 20, 0.6); --border: #27272a; 
      --text: #fff; --text-dim: #888; --accent: #3b82f6; 
      --success: #22c55e; --error: #ef4444;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    
    body { 
      background: var(--bg); color: var(--text); height: 100dvh; 
      display: flex; justify-content: center; align-items: center; overflow: hidden;
    }

    .grid-bg { 
      position: absolute; inset: 0; z-index: -1; 
      background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px); 
      background-size: 60px 60px; opacity: 0.1; 
      mask-image: radial-gradient(circle at center, black 40%, transparent 80%); 
    }

    /* CARD DESIGN */
    .login-card {
      width: 100%; max-width: 380px; padding: 40px 30px;
      background: var(--surface); border: 1px solid var(--border); border-radius: 24px;
      backdrop-filter: blur(20px); box-shadow: 0 40px 80px rgba(0,0,0,0.5);
      text-align: center; opacity: 0; transform: translateY(10px);
    }

    .brand { font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 24px; display: block; }
    
    h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; }
    p { color: var(--text-dim); font-size: 0.9rem; margin-bottom: 32px; line-height: 1.5; }

    /* INPUT */
    .input-box { position: relative; margin-bottom: 16px; }
    
    input { 
      width: 100%; padding: 14px 14px 14px 44px; 
      background: rgba(255,255,255,0.03); border: 1px solid var(--border); 
      border-radius: 12px; color: white; font-size: 1rem; outline: none; 
      transition: 0.3s;
    }
    input:focus { border-color: var(--accent); background: rgba(255,255,255,0.05); }
    
    .icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-dim); font-size: 1.1rem; transition: 0.3s; }
    input:focus + .icon { color: var(--accent); }

    /* BUTTON */
    button { 
      width: 100%; padding: 14px; background: white; color: black; 
      border: none; border-radius: 12px; font-weight: 600; cursor: pointer; 
      font-size: 0.95rem; transition: 0.2s; position: relative; overflow: hidden;
      display: flex; justify-content: center; align-items: center; gap: 8px;
    }
    button:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(255,255,255,0.1); }
    button:disabled { opacity: 0.6; cursor: wait; }

    /* TOAST */
    .toast {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%) translateY(-100px);
      background: #111; border: 1px solid #333; padding: 12px 24px; border-radius: 50px;
      font-size: 0.9rem; display: flex; align-items: center; gap: 10px;
      transition: 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); z-index: 100;
    }
    .toast.show { transform: translateX(-50%) translateY(0); }
    .toast svg { color: var(--success); }
    .toast.error svg { color: var(--error); }

    .spinner { width: 16px; height: 16px; border: 2px solid rgba(0,0,0,0.1); border-left-color: #000; border-radius: 50%; animation: spin 0.8s infinite linear; display: none; }
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>
</head>
<body>

  <div class="grid-bg"></div>

  <div class="login-card" id="card">
    <span class="brand">LUVIIO</span>
    <h2>Welcome back</h2>
    <p>Enter your email to receive a secure magic login link.</p>

    <form id="loginForm">
      <div class="input-box">
        <input type="email" id="email" placeholder="name@company.com" required autocomplete="email">
        <i class="ri-mail-line icon"></i>
      </div>
      
      <button type="submit" id="btn">
        <span id="btnText">Send Magic Link</span>
        <div class="spinner" id="spinner"></div>
      </button>
    </form>
  </div>

  <div class="toast" id="toast">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-1.177-7.86l-2.765-2.767L7 12.431l3.119 3.121a1 1 0 001.414 0l8.752-8.754-1.06-1.06-7.402 7.402z"/></svg>
    <span id="toastMsg">Link sent! Check your inbox.</span>
  </div>

  <script>
    // --- CONFIG ---
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    const supabase = supabase.createClient(SB_URL, SB_KEY);

    // --- ANIMATION ---
    gsap.to("#card", { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" });

    // --- LOGIC ---
    const form = document.getElementById('loginForm');
    const btn = document.getElementById('btn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('spinner');

    function showToast(msg, isError = false) {
      const t = document.getElementById('toast');
      const m = document.getElementById('toastMsg');
      const icon = t.querySelector('svg');
      
      m.innerText = msg;
      icon.style.color = isError ? 'var(--error)' : 'var(--success)';
      if(isError) icon.innerHTML = '<path d="M12 22C6.477 22 2 17.523 2 12S6.477 2 12 2s10 4.477 10 10-4.477 10-10 10zm-1-7v2h2v-2h-2zm0-8v6h2V7h-2z" fill="currentColor"/>'; // Exclamation

      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), 4000);
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      
      // UI Loading
      btn.disabled = true;
      btnText.style.display = 'none';
      spinner.style.display = 'block';

      try {
        const { error } = await supabase.auth.signInWithOtp({
          email: email,
          options: {
            // User wapis dashboard par aayega
            emailRedirectTo: window.location.origin + '/dashboard'
          }
        });

        if (error) throw error;

        showToast("Magic Link sent! Check your email.");
        btn.style.background = "#22c55e"; // Green success
        btn.style.color = "#fff";
        btnText.innerText = "Sent";
        document.getElementById('email').value = ""; // Clear

      } catch (err) {
        showToast(err.message || "Error sending link", true);
        gsap.to("#card", { x: -10, duration: 0.1, repeat: 3, yoyo: true }); // Shake
        
        btn.disabled = false;
        btnText.innerText = "Try Again";
      } finally {
        // Reset UI if not success or after delay
        setTimeout(() => {
            if(btnText.innerText !== "Sent") {
                spinner.style.display = 'none';
                btnText.style.display = 'block';
                btn.disabled = false;
            }
        }, 2000);
      }
    });
  </script>
</body>
</html>
"""

@router.get("/login", response_class=HTMLResponse)
async def login_page():
    return MAGIC_LOGIN_HTML