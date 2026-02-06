from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

ONBOARDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=no">
  <title>Setup Profile - Luviio</title>

  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
  
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

  <style>
    /* --- DESIGN TOKENS (MATCHING WAITLIST PAGE) --- */
    :root { 
      --bg: #050505; --card-bg: rgba(20, 20, 20, 0.6); --border: rgba(255,255,255,0.08); 
      --text: #fff; --text-dim: #a1a1aa; 
      --accent: #3b82f6; --accent-glow: rgba(59, 130, 246, 0.4);
      --success: #22c55e; --error: #ef4444;
    }

    /* --- RESET & APP FEEL --- */
    * { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; outline: none; }
    
    body { 
      background: var(--bg); color: var(--text); 
      font-family: 'Plus Jakarta Sans', sans-serif; 
      height: 100dvh; width: 100vw; overflow: hidden; 
      display: flex; flex-direction: column;
      user-select: none; -webkit-user-select: none; /* App Like */
    }

    /* GRID BACKGROUND */
    .grid-bg { 
      position: absolute; inset: 0; z-index: -1; 
      background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px); 
      background-size: 80px 80px; opacity: 0.12; 
      mask-image: radial-gradient(circle at center, black 40%, transparent 80%); 
      pointer-events: none;
    }

    /* --- LAYOUT --- */
    nav {
      width: 100%; padding: 20px 30px; display: flex; justify-content: space-between; align-items: center;
      position: relative; z-index: 10;
    }
    .brand { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.2rem; letter-spacing: -0.03em; color: white; text-decoration: none; }
    .brand img { height: 24px; width: auto; }
    
    .logout-btn {
      font-size: 0.85rem; color: var(--text-dim); cursor: pointer; transition: 0.3s;
      display: flex; align-items: center; gap: 6px;
    }
    .logout-btn:hover { color: #fff; }

    main { flex: 1; display: flex; justify-content: center; align-items: center; padding: 20px; position: relative; z-index: 5; }

    footer {
      width: 100%; padding: 20px; text-align: center; color: #444; font-size: 0.75rem; font-weight: 500;
      position: relative; z-index: 10;
    }

    /* --- WIZARD CARD --- */
    .wizard-wrapper {
      width: 100%; max-width: 480px; position: relative;
    }

    .step-card {
      background: var(--card-bg); border: 1px solid var(--border);
      backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
      border-radius: 24px; padding: 40px 30px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
      position: absolute; top: 0; left: 0; width: 100%;
      opacity: 0; visibility: hidden; transform: translateX(20px);
    }
    .step-card.active { position: relative; opacity: 1; visibility: visible; transform: translateX(0); }

    /* PROGRESS BAR */
    .progress-track {
      width: 100%; height: 4px; background: rgba(255,255,255,0.05);
      border-radius: 10px; margin-bottom: 30px; overflow: hidden;
    }
    .progress-fill {
      height: 100%; background: var(--accent); width: 20%;
      transition: width 0.5s cubic-bezier(0.25, 1, 0.5, 1);
      box-shadow: 0 0 10px var(--accent-glow);
    }

    /* TYPOGRAPHY */
    h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 8px; letter-spacing: -0.02em; }
    .label { display: block; font-size: 0.9rem; color: var(--text-dim); margin-bottom: 24px; line-height: 1.5; }

    /* FORMS */
    input, select, textarea {
      width: 100%; padding: 16px; background: rgba(0,0,0,0.3);
      border: 1px solid var(--border); border-radius: 14px;
      color: white; font-size: 1rem; outline: none; transition: 0.3s;
      font-family: inherit; margin-bottom: 15px;
      user-select: text; -webkit-user-select: text; /* Allow typing */
    }
    input:focus, select:focus, textarea:focus {
      border-color: var(--accent); background: rgba(0,0,0,0.5);
      box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    }

    /* RADIO CARDS */
    .radio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 25px; }
    .radio-card {
      background: rgba(255,255,255,0.02); border: 1px solid var(--border);
      border-radius: 16px; padding: 20px; cursor: pointer; text-align: center;
      transition: all 0.2s;
    }
    .radio-card:hover { background: rgba(255,255,255,0.05); transform: translateY(-2px); }
    .radio-card.selected {
      background: rgba(59, 130, 246, 0.1); border-color: var(--accent);
      box-shadow: 0 0 20px rgba(59, 130, 246, 0.15);
    }
    .radio-icon { font-size: 1.5rem; margin-bottom: 8px; color: var(--text-dim); }
    .selected .radio-icon { color: var(--accent); }

    /* BUTTONS */
    .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 20px; }
    
    .btn-next {
      background: white; color: black; border: none;
      padding: 14px 32px; border-radius: 100px; font-weight: 700;
      cursor: pointer; transition: 0.3s; opacity: 0.3; pointer-events: none;
      box-shadow: 0 4px 15px rgba(255,255,255,0.1);
    }
    .btn-next.enabled { opacity: 1; pointer-events: all; }
    .btn-next:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(255,255,255,0.2); }
    
    .btn-back {
      color: var(--text-dim); cursor: pointer; font-size: 0.9rem; font-weight: 500;
      padding: 10px; transition: 0.2s;
    }
    .btn-back:hover { color: white; }

    /* LOADER OVERLAY */
    #auth-loader {
        position: fixed; inset: 0; background: #050505; z-index: 9999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: opacity 0.5s;
    }
    .spinner { width: 40px; height: 40px; border: 3px solid rgba(255,255,255,0.1); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; }
    @keyframes spin { to { transform: rotate(360deg); } }
    
    #reset-btn {
        margin-top: 20px; padding: 10px 20px; background: rgba(255,50,50,0.1); 
        color: #ff4444; border: 1px solid #ff4444; border-radius: 8px; 
        cursor: pointer; display: none; font-size: 0.8rem;
    }
  </style>
</head>
<body>

  <div class="grid-bg"></div>

  <nav>
    <a href="/" class="brand">
      <img src="/images/logo.png" alt="Logo" onerror="this.style.display='none'"> 
      <span>LUVIIO</span>
    </a>
    <div class="logout-btn" onclick="hardReset()">
      <i class="ri-logout-box-r-line"></i> Sign Out
    </div>
  </nav>

  <div id="auth-loader">
    <div class="spinner"></div>
    <p id="status-text" style="margin-top:20px; color:#666; font-size:0.9rem; letter-spacing:0.5px;">INITIALIZING SECURE SESSION</p>
    <button id="reset-btn" onclick="hardReset()">Stuck? Tap to Reset</button>
  </div>

  <main>
    <div class="wizard-wrapper" id="wizard" style="display:none">
      
      <div class="step-card active" id="step1">
        <div class="progress-track"><div class="progress-fill" style="width: 20%"></div></div>
        
        <h2>Who are you?</h2>
        <span class="label">Let's start with your official name for the profile.</span>
        
        <input type="text" id="fullName" placeholder="e.g. Rahul Sharma" oninput="validate(1)" autocomplete="name">
        
        <div class="actions" style="justify-content: flex-end;">
          <button class="btn-next" id="btn1" onclick="nextStep(2)">Continue</button>
        </div>
      </div>

      <div class="step-card" id="step2">
        <div class="progress-track"><div class="progress-fill" style="width: 40%"></div></div>

        <h2>What is your purpose?</h2>
        <span class="label">Choose your primary role on Luviio.</span>
        
        <div class="radio-grid">
          <div class="radio-card" onclick="selectRole('buyer', this)">
            <div class="radio-icon"><i class="ri-shopping-bag-3-line"></i></div>
            <span>Buyer / Renter</span>
          </div>
          <div class="radio-card" onclick="selectRole('seller', this)">
            <div class="radio-icon"><i class="ri-store-2-line"></i></div>
            <span>Seller / Agent</span>
          </div>
        </div>

        <div class="actions">
          <div class="btn-back" onclick="prevStep(1)">Back</div>
          <button class="btn-next" id="btn2" onclick="handleRoleNext()">Continue</button>
        </div>
      </div>

      <div class="step-card" id="step3">
        <div class="progress-track"><div class="progress-fill" style="width: 60%"></div></div>

        <h2>How did you find us?</h2>
        <span class="label">Help us understand our community reach.</span>
        
        <select id="source" onchange="validate(3)">
          <option value="" disabled selected>Select an option</option>
          <option value="social_media">Social Media (Insta/X)</option>
          <option value="browser">Search Engine (Google)</option>
          <option value="friend">Friend / Referral</option>
          <option value="other">Other</option>
        </select>

        <div class="actions">
          <div class="btn-back" onclick="prevStep(2)">Back</div>
          <button class="btn-next" id="btn3" onclick="handleSourceNext()">Continue</button>
        </div>
      </div>

      <div class="step-card" id="step4">
        <div class="progress-track"><div class="progress-fill" style="width: 80%"></div></div>

        <h2>Store Entity</h2>
        <span class="label">Enter your business details below.</span>
        
        <input type="text" id="storeName" placeholder="Agency / Store Name" oninput="validate(4)">
        <textarea id="storeAddress" rows="2" placeholder="Full Business Address" oninput="validate(4)"></textarea>

        <div class="actions">
          <div class="btn-back" onclick="prevStep(3)">Back</div>
          <button class="btn-next" id="btn4" onclick="nextStep(5)">Continue</button>
        </div>
      </div>

      <div class="step-card" id="step5">
        <div class="progress-track"><div class="progress-fill" style="width: 100%"></div></div>

        <h2>Final Details</h2>
        <span class="label">How can customers reach you?</span>
        
        <input type="text" id="storeContact" placeholder="Official Phone or Email" oninput="validate(5)">
        <select id="category" onchange="validate(5)">
          <option value="" disabled selected>Select Category</option>
          <option value="real_estate">Real Estate</option>
          <option value="independent">Independent Broker</option>
          <option value="builder">Builder / Developer</option>
        </select>

        <div class="actions">
          <div class="btn-back" onclick="prevStep(4)">Back</div>
          <button class="btn-next" id="btn5" onclick="submitData()">Complete Setup</button>
        </div>
      </div>

    </div>
  </main>

  <footer>
    &copy; 2026 Luviio Technologies. Secure & Verified.
  </footer>

  <script>
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    
    // --- SAFE INIT ---
    let supabaseClient;
    try {
        supabaseClient = supabase.createClient(SB_URL, SB_KEY);
    } catch (e) {
        console.error("Supabase Error", e);
        document.body.innerHTML = "<h2 style='color:white;text-align:center'>Component Error. Refresh.</h2>";
    }

    let currentUser = null;
    let formData = { fullName: '', role: '', source: '', storeName: '', storeAddress: '', storeContact: '', category: '' };

    function hideLoader() {
      const loader = document.getElementById('auth-loader');
      loader.style.opacity = '0';
      setTimeout(() => { loader.style.display = 'none'; }, 500);
    }

    // --- AUTH FLOW ---
    async function init() {
        console.log("Init Onboarding...");
        
        // Timeout Safety
        setTimeout(() => {
            if (!currentUser) {
                document.getElementById('status-text').innerText = "TAKING LONGER THAN USUAL...";
                document.getElementById('reset-btn').style.display = 'block';
            }
        }, 6000);

        // 1. Hash Check (The Fix)
        const hash = window.location.hash || '';
        if (hash && hash.includes('access_token')) {
            try {
                const params = new URLSearchParams(hash.substring(1));
                const access_token = params.get('access_token');
                const refresh_token = params.get('refresh_token');

                if (access_token) {
                    const { data, error } = await supabaseClient.auth.setSession({
                        access_token, refresh_token: refresh_token || ''
                    });
                    if (!error && data?.session) {
                        window.history.replaceState(null, null, window.location.pathname);
                        handleSessionFound(data.session);
                        return;
                    }
                }
            } catch(e) { console.error(e); }
        }

        // 2. Standard Check
        const { data: { session } } = await supabaseClient.auth.getSession();
        if (session) {
            handleSessionFound(session);
        } else {
            supabaseClient.auth.onAuthStateChange((event, session) => {
                if (session) handleSessionFound(session);
            });
        }
    }

    async function handleSessionFound(session) {
        if (currentUser) return;
        currentUser = session.user;
        console.log("User:", currentUser.id);

        hideLoader();
        
        const wizard = document.getElementById('wizard');
        wizard.style.display = 'block';
        
        // GSAP Entrance
        if(typeof gsap !== 'undefined') {
            gsap.to("#step1", { opacity: 1, x: 0, duration: 0.6, ease: "power3.out" });
        } else {
            document.getElementById('step1').classList.add('active');
        }

        // Gatekeeper
        try {
             const { data } = await supabaseClient.from('profiles').select('role').eq('id', currentUser.id).single();
             if (data && data.role) window.location.href = '/dashboard';
        } catch(e) {}
    }

    window.hardReset = async function() {
        try { await supabaseClient.auth.signOut(); } catch(e){}
        localStorage.clear();
        window.location.href = '/';
    }

    init();

    // --- UI LOGIC ---
    window.validate = function(step) {
      let isValid = false;
      const btn = document.getElementById(`btn${step}`);
      if(!btn) return;

      if (step === 1) isValid = (document.getElementById('fullName').value || '').trim().length > 2;
      if (step === 3) isValid = (document.getElementById('source').value || '') !== "";
      if (step === 4) {
        const name = document.getElementById('storeName').value || '';
        const addr = document.getElementById('storeAddress').value || '';
        isValid = name.length > 2 && addr.length > 5;
      }
      if (step === 5) {
        const contact = document.getElementById('storeContact').value || '';
        const cat = document.getElementById('category').value || '';
        isValid = contact.length > 5 && cat !== "";
      }
      
      if(isValid) btn.classList.add('enabled'); 
      else btn.classList.remove('enabled');
    }

    window.selectRole = function(role, el) {
      formData.role = role;
      document.querySelectorAll('.radio-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      document.getElementById('btn2').classList.add('enabled');
    }

    window.handleRoleNext = function() { 
        if(!formData.role) return; 
        nextStep(3); 
    }

    window.handleSourceNext = function() {
       formData.source = document.getElementById('source').value;
       if(formData.role === 'buyer') submitData(); else nextStep(4);
    }

    window.nextStep = function(target) {
      const current = document.querySelector('.step-card.active');
      const next = document.getElementById(`step${target}`);
      if(!current || !next) return;

      // Update Bar
      const bar = document.querySelector('.active .progress-fill'); 
      if(bar) bar.style.width = `${(target/5)*100}%`; // Fallback logic

      if(typeof gsap !== 'undefined') {
          gsap.to(current, { x: -30, opacity: 0, duration: 0.4, onComplete: () => {
             current.classList.remove('active');
             current.style.visibility = 'hidden';
             
             next.style.visibility = 'visible';
             next.classList.add('active');
             // Update progress bar inside new card
             next.querySelector('.progress-fill').style.width = `${(target/5)*100}%`;
             
             gsap.fromTo(next, { x: 30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4 });
          }});
      } else {
          current.classList.remove('active');
          next.classList.add('active');
      }
    }

    window.prevStep = function(target) {
      const current = document.querySelector('.step-card.active');
      const prev = document.getElementById(`step${target}`);
      if(!current || !prev) return;

      if(typeof gsap !== 'undefined') {
          gsap.to(current, { x: 30, opacity: 0, duration: 0.4, onComplete: () => {
             current.classList.remove('active');
             current.style.visibility = 'hidden';
             
             prev.style.visibility = 'visible';
             prev.classList.add('active');
             gsap.fromTo(prev, { x: -30, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4 });
          }});
      }
    }

    window.submitData = async function() {
        if(!currentUser) return alert("Session expired.");
        
        const btn = document.getElementById(formData.role === 'buyer' ? 'btn3' : 'btn5');
        const origText = btn.innerText;
        btn.innerText = "Finishing...";
        
        // Gather final values
        formData.fullName = document.getElementById('fullName').value;
        if(formData.role === 'seller') {
            formData.storeName = document.getElementById('storeName').value;
            formData.storeAddress = document.getElementById('storeAddress').value;
            formData.storeContact = document.getElementById('storeContact').value;
            formData.category = document.getElementById('category').value;
        }

        try {
            // 1. Upsert Profile (Fixes Foreign Key Error)
            const { error: pErr } = await supabaseClient.from('profiles').upsert({
                id: currentUser.id,
                full_name: formData.fullName,
                role: formData.role,
                referral_source: formData.source,
                updated_at: new Date()
            });
            if(pErr) throw pErr;

            // 2. Insert Store (If Seller)
            if(formData.role === 'seller') {
                const { error: sErr } = await supabaseClient.from('stores').insert([{
                    owner_id: currentUser.id,
                    store_name: formData.storeName,
                    address: formData.storeAddress,
                    contact_email: formData.storeContact,
                    category: formData.category
                }]);
                if(sErr) throw sErr;
            }

            window.location.href = '/dashboard';

        } catch (err) {
            console.error(err);
            alert("Setup Failed: " + err.message);
            btn.innerText = origText;
        }
    }
  </script>
</body>
</html>
"""

@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page():
    return ONBOARDING_HTML