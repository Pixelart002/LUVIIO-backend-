from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

# --- OPTIMIZED SECURE LOGIN PAGE ---
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  
  <title>Luviio - Secure Access Portal</title>
  <meta name="description" content="Secure login access for Luviio Marketplace. Manage your verified listings and account settings.">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://auth.luviio.in/">
  <meta name="theme-color" content="#030303">

  <meta http-equiv="X-Frame-Options" content="DENY">
  <meta http-equiv="X-Content-Type-Options" content="nosniff">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  
  <meta http-equiv="Content-Security-Policy" content="
    default-src 'self'; 
    script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; 
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; 
    font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; 
    connect-src 'self' https://enqcujmzxtrbfkaungpm.supabase.co; 
    img-src 'self' data:; 
    object-src 'none'; 
    base-uri 'self';
  ">

  <link rel="dns-prefetch" href="https://enqcujmzxtrbfkaungpm.supabase.co">
  <link rel="preconnect" href="https://enqcujmzxtrbfkaungpm.supabase.co" crossorigin>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <meta property="og:type" content="website">
  <meta property="og:title" content="Sign In - Luviio">
  <meta property="og:description" content="Access the operating system for verified listings.">
  <meta property="og:image" content="https://www.luviio.in/og-image.jpg">

  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js" defer></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "AccountPage",
    "name": "Luviio Login",
    "description": "Secure access portal for Luviio users.",
    "url": "https://auth.luviio.in"
  }
  </script>

  <style>
    :root { 
        --bg: #030303; --card-bg: rgba(20, 20, 20, 0.6); --border: #27272a; 
        --primary: #ffffff; --primary-fg: #000000; --text-muted: #888; 
        --error: #ef4444; --success: #22c55e; --accent: #3b82f6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    body { 
        background-color: var(--bg); color: white; 
        min-height: 100dvh; display: flex; justify-content: center; align-items: center; 
        overflow: hidden; position: relative;
    }

    /* Animated Grid Background */
    .grid-bg {
        position: absolute; inset: 0; z-index: -1;
        background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px);
        background-size: 50px 50px; opacity: 0.1; mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
        pointer-events: none;
    }

    .auth-card { 
        width: 100%; max-width: 420px; padding: 40px; 
        background: var(--card-bg); backdrop-filter: blur(20px); 
        border: 1px solid var(--border); border-radius: 24px; 
        box-shadow: 0 20px 40px rgba(0,0,0,0.6); 
        position: relative; z-index: 10; opacity: 0; transform: translateY(20px);
    }

    .header { text-align: center; margin-bottom: 25px; } 
    .brand { font-size: 26px; font-weight: 800; letter-spacing: -1px; margin-bottom: 6px; display: inline-block; color: #fff; } 
    .subtitle { color: var(--text-muted); font-size: 14px; }

    /* Social Buttons */
    .social-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 25px; }
    .btn-social { 
        display: flex; align-items: center; justify-content: center; gap: 10px; padding: 12px; 
        background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 12px; 
        color: white; cursor: pointer; transition: all 0.2s; font-size: 14px; font-weight: 600; 
    }
    .btn-social:hover { background: rgba(255,255,255,0.08); border-color: #555; transform: translateY(-1px); }

    .divider { display: flex; align-items: center; margin-bottom: 25px; color: var(--text-muted); font-size: 12px; font-weight: 600; letter-spacing: 0.5px; } 
    .divider::before, .divider::after { content: ""; flex: 1; height: 1px; background: var(--border); } 
    .divider span { padding: 0 12px; }

    /* Inputs */
    .input-group { margin-bottom: 16px; position: relative; } 
    .input-wrapper { position: relative; }
    .input-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); color: var(--text-muted); font-size: 18px; pointer-events: none; transition: 0.3s; }
    
    input { 
        width: 100%; padding: 14px 14px 14px 44px; 
        background: rgba(10,10,10,0.6); border: 1px solid var(--border); 
        border-radius: 12px; color: white; font-size: 15px; outline: none; transition: all 0.3s ease; 
    }
    input:focus { border-color: var(--accent); background: rgba(20,20,20,0.9); box-shadow: 0 0 15px rgba(59, 130, 246, 0.2); }
    input:focus + .input-icon { color: var(--accent); }

    /* Honeypot for Security */
    .hp-field { display: none; visibility: hidden; opacity: 0; position: absolute; left: -9999px; }

    /* Primary Button */
    .btn-primary { 
        width: 100%; padding: 14px; background: var(--primary); color: var(--primary-fg); 
        border: none; border-radius: 12px; font-weight: 700; cursor: pointer; margin-top: 10px; 
        transition: transform 0.2s, box-shadow 0.2s; position: relative; overflow: hidden;
    }
    .btn-primary:hover:not(:disabled) { transform: translateY(-1px); box-shadow: 0 5px 15px rgba(255,255,255,0.15); }
    .btn-primary:active:not(:disabled) { transform: scale(0.98); } 
    .btn-primary:disabled { opacity: 0.6; cursor: wait; filter: grayscale(1); }

    .loader { display: none; width: 18px; height: 18px; border: 2px solid rgba(0,0,0,0.2); border-top-color: #000; border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto; } 
    @keyframes spin { to { transform: rotate(360deg); } }

    /* Toast Notification */
    .toast {
        position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%) translateY(20px);
        background: rgba(20, 20, 20, 0.95); border: 1px solid var(--border);
        padding: 12px 20px; border-radius: 50px; display: flex; align-items: center; gap: 10px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); font-size: 0.9rem; color: #fff; z-index: 100;
        opacity: 0; pointer-events: none; backdrop-filter: blur(10px); transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .toast.visible { opacity: 1; transform: translateX(-50%) translateY(0); }
    .toast.error i { color: var(--error); }
    .toast.success i { color: var(--success); }

    .footer-text { margin-top: 24px; text-align: center; font-size: 14px; color: var(--text-muted); } 
    .link { color: white; text-decoration: none; font-weight: 600; cursor: pointer; margin-left: 5px; transition: color 0.2s; }
    .link:hover { color: var(--accent); text-decoration: underline; }
  </style>
</head>
<body>

  <div class="grid-bg"></div>

  <div class="auth-card" id="authCard">
    <div class="header">
      <div class="brand">LUVIIO</div>
      <div class="subtitle" id="formSubtitle">Secure Access Portal</div>
    </div>

    <div class="social-grid">
      <button class="btn-social" onclick="signInWithProvider('google')">
        <i class="ri-google-fill"></i> Google
      </button>
      <button class="btn-social" onclick="signInWithProvider('github')">
        <i class="ri-github-fill"></i> GitHub
      </button>
    </div>

    <div class="divider"><span>OR CONTINUE WITH EMAIL</span></div>

    <form id="authForm" onsubmit="handleAuth(event)">
      <input type="text" id="_hp_check" class="hp-field" tabindex="-1" autocomplete="off">
      
      <div class="input-group">
        <div class="input-wrapper">
          <input type="email" id="email" placeholder="name@company.com" required autocomplete="email">
          <i class="ri-mail-line input-icon"></i>
        </div>
      </div>
      
      <div class="input-group">
        <div class="input-wrapper">
          <input type="password" id="password" placeholder="Password" required autocomplete="current-password">
          <i class="ri-lock-2-line input-icon"></i>
        </div>
      </div>

      <button type="submit" class="btn-primary" id="authBtn">
        <span id="btnText">Sign In</span>
        <div class="loader" id="btnLoader"></div>
      </button>

      <div class="footer-text">
        <span id="footerPrompt">Don't have an account?</span>
        <span class="link" onclick="toggleMode()" id="toggleLink">Sign up</span>
      </div>
    </form>
  </div>

  <div id="toast" class="toast">
    <i class="ri-information-fill"></i>
    <span id="toastMsg">Notification</span>
  </div>

  <script>
    // --- 1. CONFIGURATION ---
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    let supabaseClient = null;
    let isSignUp = false;
    let isProcessing = false;

    document.addEventListener("DOMContentLoaded", () => {
        // Init Supabase
        if(typeof supabase !== 'undefined') {
            supabaseClient = supabase.createClient(SB_URL, SB_KEY);
        }
        
        // Entrance Animation
        if(typeof gsap !== 'undefined') {
            gsap.to("#authCard", { opacity: 1, y: 0, duration: 0.8, ease: "power3.out" });
        } else {
            document.getElementById('authCard').style.opacity = 1;
            document.getElementById('authCard').style.transform = "translateY(0)";
        }
    });

    // --- 2. AUTH LOGIC ---
    async function signInWithProvider(providerName) {
      if(!supabaseClient) return;
      try {
        // 🔥 CRITICAL UPDATE: Always point to Onboarding first. 
        // This ensures the URL whitelist check passes.
        const { data, error } = await supabaseClient.auth.signInWithOAuth({
          provider: providerName,
          options: { redirectTo: window.location.origin + '/onboarding' }
        });
        if (error) throw error;
      } catch (error) { showToast("Error logging in with " + providerName, "error"); }
    }

    function toggleMode() {
      isSignUp = !isSignUp;
      const title = isSignUp ? "Create Secure Account" : "Secure Access Portal";
      const btn = isSignUp ? "Create Account" : "Sign In";
      const prompt = isSignUp ? "Already have an account?" : "Don't have an account?";
      const link = isSignUp ? "Log in" : "Sign up";

      // Smooth transition
      if(typeof gsap !== 'undefined') {
          gsap.fromTo(".header", {opacity:0, y:-10}, {opacity:1, y:0, duration:0.3});
      }

      document.getElementById('formSubtitle').innerText = title;
      document.getElementById('btnText').innerText = btn;
      document.getElementById('footerPrompt').innerText = prompt;
      document.getElementById('toggleLink').innerText = link;
    }

    async function handleAuth(e) {
      e.preventDefault();
      if (isProcessing) return;
      
      // Honeypot check
      if (document.getElementById('_hp_check').value) return; 
      
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value;

      if (password.length < 6) { 
          showToast("Password must be at least 6 characters.", "error"); 
          shakeCard();
          return; 
      }
      
      setLoading(true);

      try {
        if(!supabaseClient) throw new Error("Connection failed. Refresh page.");

        let result;
        if (isSignUp) {
          // 🔥 SignUp Redirect -> Onboarding
          result = await supabaseClient.auth.signUp({ 
            email, password, options: { emailRedirectTo: window.location.origin + '/onboarding' }
          });
        } else {
          result = await supabaseClient.auth.signInWithPassword({ email, password });
        }

        if (result.error) throw result.error;

        if (isSignUp && result.data.user && !result.data.session) {
           showToast("Confirmation link sent to your email.", "success");
           document.getElementById('authForm').reset();
        } else {
           showToast("Access Granted.", "success");
           
           // 🔥 INTELLIGENT REDIRECT (User Role Check) 🔥
           try {
               const { data: profile } = await supabaseClient
                   .from('profiles')
                   .select('role')
                   .eq('id', result.data.user.id)
                   .single();

               // If Role exists -> Dashboard, Else -> Onboarding
               if (profile && profile.role) {
                   setTimeout(() => window.location.href = "/dashboard", 1000);
               } else {
                   setTimeout(() => window.location.href = "/onboarding", 1000);
               }
           } catch (err) {
               // Fallback: If error checking profile, go to Onboarding
               setTimeout(() => window.location.href = "/onboarding", 1000);
           }
        }

      } catch (error) {
        let msg = error.message;
        if(msg.includes("Invalid login")) msg = "Invalid email or password.";
        showToast(msg, "error");
        shakeCard();
      } finally { 
        setLoading(false); 
      }
    }

    // --- 3. UI HELPERS ---
    function setLoading(state) {
      isProcessing = state;
      document.getElementById('btnText').style.display = state ? 'none' : 'block';
      document.getElementById('btnLoader').style.display = state ? 'block' : 'none';
      document.getElementById('authBtn').disabled = state;
    }

    function showToast(msg, type) {
      const toast = document.getElementById('toast');
      const icon = toast.querySelector('i');
      
      document.getElementById('toastMsg').innerText = msg;
      toast.className = `toast visible ${type}`;
      icon.className = type === 'error' ? "ri-error-warning-fill" : "ri-checkbox-circle-fill";

      setTimeout(() => {
        toast.className = "toast"; // Hide
      }, 4000);
    }

    function shakeCard() {
        if(typeof gsap !== 'undefined') {
            gsap.to(".auth-card", { x: -10, duration: 0.1, repeat: 3, yoyo: true });
        }
    }
  </script>
</body>
</html>
"""

@router.get("/", response_class=HTMLResponse)
async def get_login_page():
    return LOGIN_HTML