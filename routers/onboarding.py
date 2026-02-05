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

  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    /* (keep your original CSS unchanged) */
  </style>
</head>
<body>

  <!-- (keep your original HTML body unchanged) -->

  <script>
    // --- 1. CONFIGURATION ---
    const SB_URL = 'https://enqcujmzxtrbfkaungpm.supabase.co';
    const SB_KEY = 'sb_publishable_0jeCSzd3NkL-RlQn8X-eTA_-xH03xVd';

    // Use createClient exposed by the UMD bundle
    const supabase = supabaseJs.createClient ? supabaseJs.createClient(SB_URL, SB_KEY) : createClient(SB_URL, SB_KEY);

    let currentUser = null;
    let formData = { fullName: '', role: '', source: '', storeName: '', storeAddress: '', storeContact: '', category: '' };

    // helper to hide loader with fade
    function hideLoader() {
      const loader = document.getElementById('auth-loader');
      loader.style.opacity = '0';
      setTimeout(() => { loader.style.display = 'none'; }, 500);
    }

    async function init() {
        console.log("Initializing Onboarding...");

        // Safety Timeout: If loading takes >5 seconds, show reset button
        setTimeout(() => {
            if (!currentUser) {
                const st = document.getElementById('status-text');
                if (st) st.innerText = "Taking longer than usual...";
                const rb = document.getElementById('reset-btn');
                if (rb) rb.style.display = 'block';
            }
        }, 5000);

        // A. Check URL Hash for Access Token (Manual Override)
        const hash = window.location.hash || '';
        if (hash && hash.includes('access_token')) {
            try {
                const params = new URLSearchParams(hash.substring(1));
                const access_token = params.get('access_token');
                const refresh_token = params.get('refresh_token');

                if (access_token) {
                    const { data, error } = await supabase.auth.setSession({
                        access_token: access_token,
                        refresh_token: refresh_token || ''
                    });

                    if (!error && data && data.session) {
                        window.history.replaceState(null, null, window.location.pathname);
                        handleSessionFound(data.session);
                        return;
                    } else {
                        console.warn('setSession error', error);
                    }
                }
            } catch (e) {
                console.error('Hash parsing failed', e);
            }
        }

        // B. Standard Session Check
        try {
            const { data: { session }, error } = await supabase.auth.getSession();
            if (error) console.warn('getSession error', error);
            if (session) {
                handleSessionFound(session);
            } else {
                // C. Listener (Backup)
                supabase.auth.onAuthStateChange((event, session) => {
                    if (session) handleSessionFound(session);
                });
            }
        } catch (e) {
            console.error('Session check failed', e);
        }

        // initial validation for autofill
        validate(1);
    }

    async function handleSessionFound(session) {
        if (currentUser) return;
        currentUser = session.user;
        console.log("Session Active:", currentUser?.id);

        hideLoader();
        document.getElementById('wizard').style.display = 'block';
        gsap.to("#step1", { opacity: 1, x: 0, duration: 0.5 });

        // Gatekeeper: If already onboarded, go to Dashboard
        try {
            const { data, error } = await supabase.from('profiles').select('role').eq('id', currentUser.id).single();
            if (!error && data && data.role) {
                window.location.href = '/dashboard';
            } else {
                console.log('No profile role found or error', error);
            }
        } catch(e) { console.log("New user detected", e); }
    }

    // Safety Reset Function
    window.hardReset = async function() {
        try { await supabase.auth.signOut(); } catch(e){ console.warn(e); }
        localStorage.clear();
        window.location.href = '/';
    }

    init(); // Start logic

    // --- 3. UI & FORM LOGIC ---
    window.validate = function(step) {
      let isValid = false;
      const btn = document.getElementById(`btn${step}`);
      if(!btn) return;

      if (step === 1) isValid = (document.getElementById('fullName').value || '').trim().length > 2;
      if (step === 3) isValid = (document.getElementById('source').value || '') !== "";
      if (step === 4) {
        isValid = (document.getElementById('storeName').value || '').length > 2 &&
                  (document.getElementById('storeAddress').value || '').length > 5;
      }
      if (step === 5) {
        isValid = (document.getElementById('storeContact').value || '').length > 5 &&
                  (document.getElementById('category').value || '') !== "";
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

    window.handleRoleNext = function() { if(formData.role) nextStep(3); else alert('Please select a role'); }
    
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
      if(!current || !next) return;

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
      if(!current || !prev) return;

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
        if(!btn) return alert('Button not found');
        const originalText = btn.innerText;
        btn.innerText = "Saving...";

        formData.fullName = document.getElementById('fullName').value || '';
        if(formData.role === 'seller') {
            formData.storeName = document.getElementById('storeName').value || '';
            formData.storeAddress = document.getElementById('storeAddress').value || '';
            formData.storeContact = document.getElementById('storeContact').value || '';
            formData.category = document.getElementById('category').value || '';
        }

        try {
            const { error: pErr } = await supabase.from('profiles').update({
                full_name: formData.fullName,
                role: formData.role,
                referral_source: formData.source
            }).eq('id', currentUser.id);

            if(pErr) throw pErr;

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

            window.location.href = '/dashboard';

        } catch (err) {
            console.error(err);
            alert("Error: " + (err.message || JSON.stringify(err)));
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