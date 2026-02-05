from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

ONBOARDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <title>Setup Profile - Luviio</title>
  
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root { 
      --bg: #050505; --card: #0f0f0f; --border: #27272a; 
      --text: #fff; --text-dim: #888; --accent: #3b82f6; 
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    
    body { background: var(--bg); color: var(--text); height: 100dvh; display: flex; justify-content: center; align-items: center; padding: 20px; overflow: hidden; }

    /* LOADER (Critical for preventing white flash/stuck screen) */
    #auth-loader {
        position: fixed; inset: 0; background: #000; z-index: 9999;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        transition: opacity 0.5s;
    }
    .spinner { width: 40px; height: 40px; border: 4px solid #333; border-top-color: var(--accent); border-radius: 50%; animation: spin 1s infinite linear; }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* ERROR BUTTON */
    #reset-btn {
        display: none; margin-top: 20px; padding: 10px 20px;
        background: #ef4444; color: white; border: none; border-radius: 8px; cursor: pointer;
    }

    /* WIZARD UI */
    .progress-container { position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #222; }
    .progress-bar { height: 100%; background: var(--accent); width: 0%; transition: width 0.5s ease; }
    .wizard-container { width: 100%; max-width: 500px; position: relative; min-height: 500px; perspective: 1000px; display: none; }

    .step-card {
      position: absolute; top: 0; left: 0; width: 100%;
      background: var(--card); border: 1px solid var(--border); border-radius: 20px;
      padding: 30px; opacity: 0; visibility: hidden; transform: translateX(50px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .step-card.active { position: relative; opacity: 1; visibility: visible; transform: translateX(0); }

    h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
    .label { display: block; font-size: 0.9rem; color: var(--text-dim); margin-bottom: 20px; }

    /* Inputs & Form Elements */
    input, select, textarea {
      width: 100%; padding: 14px; background: rgba(255,255,255,0.05);
      border: 1px solid var(--border); border-radius: 12px; color: white;
      font-size: 1rem; outline: none; transition: 0.3s; margin-bottom: 10px;
    }
    input:focus, select:focus { border-color: var(--accent); background: rgba(255,255,255,0.08); }

    .radio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
    .radio-card {
      padding: 20px; border: 1px solid var(--border); border-radius: 12px;
      cursor: pointer; text-align: center; transition: 0.3s;
    }
    .radio-card:hover { background: rgba(255,255,255,0.05); }
    .radio-card.selected { border-color: var(--accent); background: rgba(59, 130, 246, 0.1); }
    .radio-icon { font-size: 1.5rem; margin-bottom: 5px; color: #ccc; }

    /* Buttons */
    .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 30px; }
    .btn-next {
      background: #fff; color: #000; border: none; padding: 12px 30px;
      border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.3s; opacity: 0.5; pointer-events: none;
    }
    .btn-next.enabled { opacity: 1; pointer-events: all; }
    .btn-back { color: var(--text-dim); cursor: pointer; font-size: 0.9rem; }
  </style>
</head>
<body>

  <div id="auth-loader">
    <div class="spinner"></div>
    <p id="status-text" style="margin-top:15px; color:#666; font-size:0.9rem;">Securing your workspace...</p>
    <button id="reset-btn" onclick="hardReset()">Stuck? Click to Restart</button>
  </div>

  <div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>

  <div class="wizard-container" id="wizard">
    
    <div class="step-card active" id="step1">
      <h2>Q1. Who are you?</h2>
      <span class="label">Let's start with your official name.</span>
      <input type="text" id="fullName" placeholder="e.g. Rahul Sharma" oninput="validate(1)" onkeyup="validate(1)">
      <div class="actions" style="justify-content: flex-end;">
        <button class="btn-next" id="btn1" onclick="nextStep(2)">Next</button>
      </div>
    </div>

    <div class="step-card" id="step2">
      <h2>Q2. What is your purpose?</h2>
      <span class="label">Are you here to buy/rent or to sell/list?</span>
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
        <button class="btn-next" id="btn2" onclick="handleRoleNext()">Next</button>
      </div>
    </div>

    <div class="step-card" id="step3">
      <h2>Q3. Where did you hear about us?</h2>
      <span class="label">Help us know how you found Luviio.</span>
      <select id="source" onchange="validate(3)">
        <option value="" disabled selected>Select an option</option>
        <option value="social_media">Social Media (Insta/X)</option>
        <option value="browser">Search Engine (Google)</option>
        <option value="friend">Friend / Referral</option>
        <option value="other">Other</option>
      </select>
      <div class="actions">
        <div class="btn-back" onclick="prevStep(2)">Back</div>
        <button class="btn-next" id="btn3" onclick="handleSourceNext()">Next</button>
      </div>
    </div>

    <div class="step-card" id="step4">
      <h2>Store Details</h2>
      <span class="label">Tell us about your business entity.</span>
      <input type="text" id="storeName" placeholder="Agency Name" oninput="validate(4)">
      <textarea id="storeAddress" rows="2" placeholder="Address..." oninput="validate(4)"></textarea>
      <div class="actions">
        <div class="btn-back" onclick="prevStep(3)">Back</div>
        <button class="btn-next" id="btn4" onclick="nextStep(5)">Next</button>
      </div>
    </div>

    <div class="step-card" id="step5">
      <h2>Contact & Plan</h2>
      <span class="label">Final details.</span>
      <input type="text" id="storeContact" placeholder="Phone/Email" oninput="validate(5)">
      <select id="category" onchange="validate(5)">
        <option value="" disabled selected>Select Category</option>
        <option value="real_estate">Real Estate</option>
        <option value="independent">Independent</option>
        <option value="builder">Builder</option>
      </select>
      <div class="actions">
        <div class="btn-back" onclick="prevStep(4)">Back</div>
        <button class="btn-next" id="btn5" onclick="submitData()">Finish Setup</button>
      </div>
    </div>

  </div>

  <script>
    // --- 1. CONFIGURATION ---
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    const supabase = supabase.createClient(SB_URL, SB_KEY);
    
    let currentUser = null;
    let formData = { fullName: '', role: '', source: '', storeName: '', storeAddress: '', storeContact: '', category: '' };

    // --- 2. THE FIX: MANUAL HASH PARSING ---
    async function init() {
        console.log("Initializing Onboarding...");

        // Safety Timeout: If loading takes >5 seconds, show reset button
        setTimeout(() => {
            if (!currentUser) {
                document.getElementById('status-text').innerText = "Taking longer than usual...";
                document.getElementById('reset-btn').style.display = 'block';
            }
        }, 5000);

        // A. Check URL Hash for Access Token (The Manual Override)
        const hash = window.location.hash;
        if (hash && hash.includes('access_token')) {
            console.log("Token found in URL, forcing session...");
            
            // Extract tokens manually
            const params = new URLSearchParams(hash.substring(1)); // Remove '#'
            const access_token = params.get('access_token');
            const refresh_token = params.get('refresh_token');

            if (access_token) {
                // Force Supabase to set session
                const { data, error } = await supabase.auth.setSession({
                    access_token: access_token,
                    refresh_token: refresh_token || ''
                });
                
                if (!error) {
                    // Clean URL (Remove the ugly hash)
                    window.history.replaceState(null, null, window.location.pathname);
                    handleSessionFound(data.session);
                    return; // Exit, we are done
                }
            }
        }

        // B. Standard Session Check (For page refreshes)
        const { data: { session } } = await supabase.auth.getSession();
        
        if (session) {
            handleSessionFound(session);
        } else {
            // C. Listener (Backup)
            supabase.auth.onAuthStateChange((event, session) => {
                if (session) handleSessionFound(session);
            });
        }
    }

    async function handleSessionFound(session) {
        if (currentUser) return; // Already loaded
        currentUser = session.user;
        console.log("Session Active:", currentUser.id);

        // Hide Loader -> Show Wizard
        document.getElementById('auth-loader').style.display = 'none';
        document.getElementById('wizard').style.display = 'block';
        
        // Entry Animation
        gsap.to("#step1", { opacity: 1, x: 0, duration: 0.5 });

        // Gatekeeper: If already onboarded, go to Dashboard
        try {
            const { data } = await supabase.from('profiles').select('role').eq('id', currentUser.id).single();
            if (data && data.role) {
                window.location.href = '/dashboard';
            }
        } catch(e) { console.log("New user detected"); }
    }

    // Safety Reset Function
    window.hardReset = async function() {
        await supabase.auth.signOut();
        localStorage.clear();
        window.location.href = '/';
    }

    init(); // Start logic

    // --- 3. UI & FORM LOGIC ---
    window.validate = function(step) {
      let isValid = false;
      const btn = document.getElementById(`btn${step}`);
      
      if (step === 1) isValid = document.getElementById('fullName').value.trim().length > 2;
      if (step === 3) isValid = document.getElementById('source').value !== "";
      if (step === 4) {
        isValid = document.getElementById('storeName').value.length > 2 && 
                  document.getElementById('storeAddress').value.length > 5;
      }
      if (step === 5) {
        isValid = document.getElementById('storeContact').value.length > 5 && 
                  document.getElementById('category').value !== "";
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

    window.handleRoleNext = function() { if(formData.role) nextStep(3); }
    
    window.handleSourceNext = function() {
       formData.source = document.getElementById('source').value;
       if(formData.role === 'buyer') {
           submitData(); 
       } else {
           nextStep(4);
       }
    }

    window.nextStep = function(target) {
      const current = document.querySelector('.step-card.active');
      const next = document.getElementById(`step${target}`);
      
      // Progress Bar
      document.getElementById('progressBar').style.width = `${(target/5)*100}%`;

      gsap.to(current, { x: -50, opacity: 0, duration: 0.3, onComplete: () => {
        current.classList.remove('active');
        current.style.visibility = 'hidden';
        next.style.visibility = 'visible';
        next.classList.add('active');
        gsap.fromTo(next, { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3 });
      }});
    }

    window.prevStep = function(target) {
      const current = document.querySelector('.step-card.active');
      const prev = document.getElementById(`step${target}`);
      
      gsap.to(current, { x: 50, opacity: 0, duration: 0.3, onComplete: () => {
        current.classList.remove('active');
        current.style.visibility = 'hidden';
        prev.style.visibility = 'visible';
        prev.classList.add('active');
        gsap.fromTo(prev, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.3 });
      }});
    }

    window.submitData = async function() {
        if(!currentUser) return alert("Session lost. Please refresh.");
        
        const btn = document.getElementById('btn5') || document.getElementById('btn3');
        const originalText = btn.innerText;
        btn.innerText = "Saving...";
        
        formData.fullName = document.getElementById('fullName').value;
        if(formData.role === 'seller') {
            formData.storeName = document.getElementById('storeName').value;
            formData.storeAddress = document.getElementById('storeAddress').value;
            formData.storeContact = document.getElementById('storeContact').value;
            formData.category = document.getElementById('category').value;
        }

        try {
            // Update Profile
            const { error: pErr } = await supabase.from('profiles').update({
                full_name: formData.fullName,
                role: formData.role,
                referral_source: formData.source
            }).eq('id', currentUser.id);
            
            if(pErr) throw pErr;

            // Create Store (if seller)
            if(formData.role === 'seller') {
                const { error: sErr } = await supabase.from('stores').insert([{
                    owner_id: currentUser.id,
                    store_name: formData.storeName,
                    address: formData.storeAddress,
                    contact_email: formData.storeContact,
                    category: formData.category
                }]);
                if(sErr) throw sErr;
            }

            // Success!
            window.location.href = '/dashboard';

        } catch (err) {
            console.error(err);
            alert("Error: " + err.message);
            btn.innerText = originalText;
        }
    }
  </script>
</body>
</html>
"""

@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page():
    return ONBOARDING_HTML