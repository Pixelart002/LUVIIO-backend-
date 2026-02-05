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

    /* PROGRESS BAR */
    .progress-container { position: absolute; top: 0; left: 0; width: 100%; height: 4px; background: #222; }
    .progress-bar { height: 100%; background: var(--accent); width: 0%; transition: width 0.5s ease; }

    /* FORM CONTAINER */
    .wizard-container { width: 100%; max-width: 500px; position: relative; min-height: 400px; perspective: 1000px; }

    .step-card {
      position: absolute; top: 0; left: 0; width: 100%;
      background: var(--card); border: 1px solid var(--border); border-radius: 20px;
      padding: 40px; opacity: 0; visibility: hidden; transform: translateX(50px);
      box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    .step-card.active { position: relative; opacity: 1; visibility: visible; transform: translateX(0); }

    h2 { font-size: 1.5rem; font-weight: 700; margin-bottom: 10px; }
    .label { display: block; font-size: 0.9rem; color: var(--text-dim); margin-bottom: 20px; }

    /* INPUTS */
    input, select, textarea {
      width: 100%; padding: 14px; background: rgba(255,255,255,0.05);
      border: 1px solid var(--border); border-radius: 12px; color: white;
      font-size: 1rem; outline: none; transition: 0.3s; margin-bottom: 10px;
    }
    input:focus, select:focus { border-color: var(--accent); background: rgba(255,255,255,0.08); }

    /* RADIO CARDS (For Role) */
    .radio-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
    .radio-card {
      padding: 20px; border: 1px solid var(--border); border-radius: 12px;
      cursor: pointer; text-align: center; transition: 0.3s;
    }
    .radio-card:hover { background: rgba(255,255,255,0.05); }
    .radio-card.selected { border-color: var(--accent); background: rgba(59, 130, 246, 0.1); }
    .radio-icon { font-size: 1.5rem; margin-bottom: 5px; color: #ccc; }

    /* BUTTONS */
    .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 30px; }
    .btn-next {
      background: #fff; color: #000; border: none; padding: 12px 30px;
      border-radius: 50px; font-weight: 600; cursor: pointer; transition: 0.3s;
    }
    .btn-next:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-back { color: var(--text-dim); cursor: pointer; font-size: 0.9rem; }
    .btn-back:hover { color: #fff; }

    /* ERROR */
    .error-msg { color: #ef4444; font-size: 0.85rem; margin-top: 5px; display: none; }

  </style>
</head>
<body>

  <div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>

  <div class="grid-bg"></div>

  <div class="wizard-container">
    
    <div class="step-card active" id="step1">
      <h2>Q1. Who are you?</h2>
      <span class="label">Let's start with your official name.</span>
      <input type="text" id="fullName" placeholder="e.g. Rahul Sharma" oninput="validate(1)">
      <div class="actions" style="justify-content: flex-end;">
        <button class="btn-next" id="btn1" onclick="nextStep(2)" disabled>Next</button>
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
        <button class="btn-next" id="btn2" onclick="handleRoleNext()" disabled>Next</button>
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
        <button class="btn-next" id="btn3" onclick="handleSourceNext()" disabled>Next</button>
      </div>
    </div>

    <div class="step-card" id="step4">
      <h2>Store Details</h2>
      <span class="label">Tell us about your business entity.</span>
      
      <label style="font-size:0.8rem; color:#666;">Q4. Store/Agency Name</label>
      <input type="text" id="storeName" placeholder="e.g. Sharma Estates" oninput="validate(4)">
      
      <label style="font-size:0.8rem; color:#666; margin-top:10px; display:block">Q5. Store Address</label>
      <textarea id="storeAddress" rows="2" placeholder="Full business address..." oninput="validate(4)" 
        style="width:100%; padding:14px; background:rgba(255,255,255,0.05); border:1px solid var(--border); border-radius:12px; color:white;"></textarea>

      <div class="actions">
        <div class="btn-back" onclick="prevStep(3)">Back</div>
        <button class="btn-next" id="btn4" onclick="nextStep(5)" disabled>Next</button>
      </div>
    </div>

    <div class="step-card" id="step5">
      <h2>Contact & Plan</h2>
      <span class="label">How can customers reach you?</span>

      <label style="font-size:0.8rem; color:#666;">Q6. Store Contact (Phone/Email)</label>
      <input type="text" id="storeContact" placeholder="Official Email or Phone" oninput="validate(5)">

      <label style="font-size:0.8rem; color:#666; margin-top:10px; display:block">Q7. What is your Category?</label>
      <select id="category" onchange="validate(5)">
        <option value="" disabled selected>Select Category</option>
        <option value="real_estate">Real Estate Agency</option>
        <option value="independent">Independent Broker</option>
        <option value="builder">Builder / Developer</option>
      </select>

      <div style="margin-top:20px; padding:15px; background:rgba(34, 197, 94, 0.1); border:1px solid #22c55e; border-radius:10px;">
        <p style="color:#22c55e; margin:0; font-size:0.85rem;"><i class="ri-checkbox-circle-line"></i> Current Plan: <b>Free Tier</b> (New User)</p>
      </div>

      <div class="actions">
        <div class="btn-back" onclick="prevStep(4)">Back</div>
        <button class="btn-next" id="btn5" onclick="submitData()">Complete Setup</button>
      </div>
    </div>

  </div>

  <script>
    // --- CONFIG ---
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    const supabase = supabase.createClient(SB_URL, SB_KEY);

    // --- STATE ---
    let formData = {
      fullName: '',
      role: '',
      source: '',
      storeName: '',
      storeAddress: '',
      storeContact: '',
      category: ''
    };

    // --- ANIMATION ---
    document.addEventListener("DOMContentLoaded", () => {
      gsap.to("#step1", { opacity: 1, x: 0, duration: 0.6 });
    });

    // --- VALIDATION & NAVIGATION ---
    function validate(step) {
      let isValid = false;
      if (step === 1) isValid = document.getElementById('fullName').value.length > 2;
      if (step === 3) isValid = document.getElementById('source').value !== "";
      if (step === 4) {
        isValid = document.getElementById('storeName').value.length > 2 && 
                  document.getElementById('storeAddress').value.length > 5;
      }
      if (step === 5) {
        isValid = document.getElementById('storeContact').value.length > 5 && 
                  document.getElementById('category').value !== "";
      }
      
      document.getElementById(`btn${step}`).disabled = !isValid;
    }

    function selectRole(role, el) {
      formData.role = role;
      document.querySelectorAll('.radio-card').forEach(c => c.classList.remove('selected'));
      el.classList.add('selected');
      document.getElementById('btn2').disabled = false;
    }

    function handleRoleNext() {
      // Save Role Logic
      nextStep(3);
    }

    function handleSourceNext() {
      formData.source = document.getElementById('source').value;
      
      if (formData.role === 'buyer') {
        // Buyers skip store details -> Submit directly
        submitData(); 
      } else {
        // Sellers go to Step 4
        nextStep(4);
      }
    }

    function nextStep(target) {
      const current = document.querySelector('.step-card.active');
      const next = document.getElementById(`step${target}`);
      
      // Update Progress
      const progress = (target / 5) * 100;
      document.getElementById('progressBar').style.width = `${progress}%`;

      gsap.to(current, { x: -50, opacity: 0, duration: 0.4, onComplete: () => {
        current.classList.remove('active');
        current.style.visibility = 'hidden';
        next.style.visibility = 'visible';
        next.classList.add('active');
        gsap.fromTo(next, { x: 50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4 });
      }});
    }

    function prevStep(target) {
      const current = document.querySelector('.step-card.active');
      const prev = document.getElementById(`step${target}`);
      
      gsap.to(current, { x: 50, opacity: 0, duration: 0.4, onComplete: () => {
        current.classList.remove('active');
        current.style.visibility = 'hidden';
        prev.style.visibility = 'visible';
        prev.classList.add('active');
        gsap.fromTo(prev, { x: -50, opacity: 0 }, { x: 0, opacity: 1, duration: 0.4 });
      }});
    }

    // --- FINAL SUBMISSION (DOUBLE CHECKED) ---
    async function submitData() {
      // 1. Gather Data
      formData.fullName = document.getElementById('fullName').value;
      if(formData.role === 'seller') {
        formData.storeName = document.getElementById('storeName').value;
        formData.storeAddress = document.getElementById('storeAddress').value;
        formData.storeContact = document.getElementById('storeContact').value;
        formData.category = document.getElementById('category').value;
      }

      try {
        const { data: { user } } = await supabase.auth.getUser();
        if (!user) throw new Error("Authentication failed");

        // 2. Update PROFILE (Q1, Q2, Q3)
        const { error: profileError } = await supabase
          .from('profiles')
          .update({
            full_name: formData.fullName,
            role: formData.role,
            referral_source: formData.source
          })
          .eq('id', user.id);

        if (profileError) throw profileError;

        // 3. If SELLER -> Insert into STORES (Q4, Q5, Q6, Q7)
        if (formData.role === 'seller') {
          const { error: storeError } = await supabase
            .from('stores')
            .insert([{
              owner_id: user.id,
              store_name: formData.storeName,
              address: formData.storeAddress,
              contact_email: formData.storeContact, // Assuming mixed field
              category: formData.category,
              plan_type: 'free_tier' // Default
            }]);
          
          if (storeError) throw storeError;
        }

        // 4. Success -> Redirect
        window.location.href = '/dashboard';

      } catch (err) {
        console.error(err);
        alert("Setup Error: " + err.message);
      }
    }
  </script>
</body>
</html>
"""

@router.get("/onboarding", response_class=HTMLResponse)
async def onboarding_page():
    return ONBOARDING_HTML