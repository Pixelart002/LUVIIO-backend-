from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

ONBOARDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Setup Profile - Luviio</title>
  
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">

  <style>
    :root { 
        --bg: #030303; --card-bg: rgba(20, 20, 20, 0.6); --border: #27272a; 
        --primary: #ffffff; --primary-fg: #000000; --text-muted: #888; 
        --accent: #3b82f6;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
    body { background-color: var(--bg); color: white; min-height: 100dvh; display: flex; justify-content: center; align-items: center; overflow: hidden; }

    /* Login wala Background */
    .grid-bg { position: absolute; inset: 0; z-index: -1; background-image: linear-gradient(var(--border) 1px, transparent 1px), linear-gradient(90deg, var(--border) 1px, transparent 1px); background-size: 50px 50px; opacity: 0.1; mask-image: radial-gradient(circle at center, black 40%, transparent 80%); }

    #auth-loader { position: fixed; inset: 0; background: #000; z-index: 9999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .spinner { width: 30px; height: 30px; border: 3px solid #333; border-top-color: #fff; border-radius: 50%; animation: spin 1s infinite linear; }
    @keyframes spin { to { transform: rotate(360deg); } }

    .wizard-card { 
        width: 100%; max-width: 450px; padding: 40px; background: var(--card-bg); 
        backdrop-filter: blur(20px); border: 1px solid var(--border); border-radius: 24px; 
        display: none; position: relative;
    }

    .step { display: none; }
    .step.active { display: block; animation: fadeIn 0.4s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

    h2 { font-size: 22px; font-weight: 700; margin-bottom: 8px; }
    p { color: var(--text-muted); font-size: 14px; margin-bottom: 24px; }

    input, select { 
        width: 100%; padding: 14px; background: rgba(10,10,10,0.6); 
        border: 1px solid var(--border); border-radius: 12px; color: white; 
        outline: none; margin-bottom: 15px; transition: 0.3s;
    }
    input:focus { border-color: var(--accent); }

    .role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 20px; }
    .role-item { 
        padding: 20px; border: 1px solid var(--border); border-radius: 16px; 
        text-align: center; cursor: pointer; transition: 0.3s;
    }
    .role-item.selected { border-color: var(--accent); background: rgba(59, 130, 246, 0.1); }
    .role-item i { font-size: 24px; display: block; margin-bottom: 8px; }

    .btn-next { 
        width: 100%; padding: 14px; background: var(--primary); color: var(--primary-fg); 
        border: none; border-radius: 12px; font-weight: 700; cursor: pointer;
    }
    .btn-next:disabled { opacity: 0.5; cursor: not-allowed; }
    .btn-back { display: block; text-align: center; margin-top: 15px; color: var(--text-muted); cursor: pointer; font-size: 14px; }
  </style>
</head>
<body>
  <div class="grid-bg"></div>
  
  <div id="auth-loader"><div class="spinner"></div></div>

  <div class="wizard-card" id="wizard">
    <!-- Step 1: Profile Info -->
    <div class="step active" id="step1">
      <h2>Complete Profile</h2>
      <p>Tell us your official name to get started.</p>
      <input type="text" id="fullName" placeholder="Full Name" oninput="checkStep(1)">
      <button class="btn-next" id="btn1" disabled onclick="nextStep(2)">Continue</button>
    </div>

    <!-- Step 2: Role Selection -->
    <div class="step" id="step2">
      <h2>Identity</h2>
      <p>How do you plan to use Luviio?</p>
      <div class="role-grid">
        <div class="role-item" id="role-buyer" onclick="setRole('buyer')">
          <i class="ri-user-search-line"></i> <span>Buyer</span>
        </div>
        <div class="role-item" id="role-seller" onclick="setRole('seller')">
          <i class="ri-store-2-line"></i> <span>Seller</span>
        </div>
      </div>
      <button class="btn-next" id="btn2" disabled onclick="nextStep(3)">Next</button>
      <span class="btn-back" onclick="prevStep(1)">Go Back</span>
    </div>

    <!-- Step 3: Final Submission -->
    <div class="step" id="step3">
        <h2>Business Details</h2>
        <p>Give your store or workspace a name.</p>
        <input type="text" id="storeName" placeholder="Store/Agency Name" oninput="checkStep(3)">
        <button class="btn-next" id="btn3" disabled onclick="finishOnboarding()">Complete Setup</button>
        <span class="btn-back" onclick="prevStep(2)">Go Back</span>
    </div>
  </div>

  <script>
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';
    const supabase = supabase.createClient(SB_URL, SB_KEY);

    let profileData = { fullName: '', role: '', storeName: '' };

    // --- SESSION CHECK ---
    async function init() {
        const { data: { session } } = await supabase.auth.getSession();
        
        // Agar session nahi hai, matlab user login nahi hai -> Login page bhejo
        if (!session) {
            window.location.href = '/login'; 
            return;
        }

        // Loader hide wizard show
        document.getElementById('auth-loader').style.display = 'none';
        document.getElementById('wizard').style.display = 'block';
        gsap.to("#wizard", { opacity: 1, y: 0, duration: 0.5 });
    }

    function checkStep(step) {
        let valid = false;
        if(step === 1) valid = document.getElementById('fullName').value.length > 2;
        if(step === 2) valid = profileData.role !== '';
        if(step === 3) valid = document.getElementById('storeName').value.length > 2;
        document.getElementById(`btn${step}`).disabled = !valid;
    }

    function setRole(role) {
        profileData.role = role;
        document.querySelectorAll('.role-item').forEach(el => el.classList.remove('selected'));
        document.getElementById(`role-${role}`).classList.add('selected');
        checkStep(2);
    }

    function nextStep(s) {
        document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
        document.getElementById(`step${s}`).classList.add('active');
    }
    
    function prevStep(s) { nextStep(s); }

    async function finishOnboarding() {
        const { data: { user } } = await supabase.auth.getUser();
        const finishBtn = document.getElementById('btn3');
        finishBtn.innerText = "Saving...";
        finishBtn.disabled = true;

        // Updating user metadata in Supabase
        const { error } = await supabase.auth.updateUser({
            data: { 
                full_name: document.getElementById('fullName').value,
                role: profileData.role,
                store_name: document.getElementById('storeName').value,
                onboarding_completed: true 
            }
        });

        if (error) {
            alert(error.message);
            finishBtn.innerText = "Try Again";
            finishBtn.disabled = false;
        } else {
            window.location.href = '/dashboard';
        }
    }

    init();
  </script>
</body>
</html>
"""

@router.get("/onboarding", response_class=HTMLResponse)
async def get_onboarding():
    return ONBOARDING_HTML
