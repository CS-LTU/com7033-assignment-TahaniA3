// App script: auth UI, page protection, CSV load, records and users management.

let patientData = [];
let dataStatus = null;

document.addEventListener('DOMContentLoaded', () => {
    dataStatus = document.getElementById('dataStatus');

    // nav button clicks (protection checked)
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const page = btn.dataset.page;
            if (!canOpenPage(page)) { alert('Access denied. Please login with appropriate account.'); return; }
            showPage(page);
        });
    });

    setupAuthForms();

    const fileInput = document.getElementById('csvFileInput');
    if (fileInput) fileInput.addEventListener('change', handleLocalCSV);

    const s = document.getElementById('recordSearch');
    if (s) s.addEventListener('input', () => renderRecordsTable(patientData));

    // try auto load CSV from likely locations
    (async () => {
        try { await loadCSVFromServer('../stroke.csv'); } catch(e1){ try{ await loadCSVFromServer('./stroke.csv'); }catch(e2){ if (dataStatus) dataStatus.textContent='No CSV loaded'; } }
    })();

    refreshAuthUI();
    showPage('home');
});

function canOpenPage(pageId) {
    const user = window.UserAPI.currentUser();
    if (!user) return pageId === 'home';
    if (pageId === 'records') return user.permissions.includes('view_records');
    if (pageId === 'userManagement') return user.permissions.includes('manage_users');
    return true;
}

function refreshAuthUI() {
    const user = window.UserAPI.currentUser();
    const loginBtn = document.getElementById('openLoginBtn');
    if (loginBtn) loginBtn.textContent = user ? `Logout (${user.fullName||user.email})` : 'Login';

    document.querySelectorAll('.admin-only').forEach(el => {
        el.style.display = (user && (user.permissions.includes('manage_users') || user.role==='admin')) ? '' : 'none';
    });
    document.querySelectorAll('.records-only').forEach(el => {
        el.style.display = (user && user.permissions.includes('view_records')) ? '' : 'none';
    });
}

function setupAuthForms() {
    const openBtn = document.getElementById('openLoginBtn');
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const loginErr = document.getElementById('loginError');

    function openLogin() { if (!loginModal) return; loginModal.style.display = 'flex'; loginModal.setAttribute('aria-hidden','false'); }
    function closeLogin(){ if (!loginModal) return; loginModal.style.display = 'none'; loginModal.setAttribute('aria-hidden','true'); if (loginErr) loginErr.textContent = ''; }

    openBtn && openBtn.addEventListener('click', () => {
        const user = window.UserAPI.currentUser();
        if (user) { window.UserAPI.signout(); refreshAuthUI(); showPage('home'); return; }
        openLogin();
    });

    document.getElementById('closeLoginBtn')?.addEventListener('click', closeLogin);
    document.getElementById('cancelLogin')?.addEventListener('click', closeLogin);

    loginForm && loginForm.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const fd = new FormData(loginForm);
        const email = fd.get('email'), pass = fd.get('password');
        try {
            window.UserAPI.authenticate(email, pass);
            closeLogin();
            refreshAuthUI();
            alert('Login successful');
            showPage('home');
        } catch (err) { if (loginErr) loginErr.textContent = err.message; }
    });

    // register modal
    const openRegisterBtn = document.getElementById('openRegisterBtn');
    const registerModal = document.getElementById('registerModal');
    const registerForm = document.getElementById('registerForm');
    const registerErr = document.getElementById('registerError');

    openRegisterBtn && openRegisterBtn.addEventListener('click', () => { if (!registerModal) return; registerModal.style.display = 'flex'; registerModal.setAttribute('aria-hidden','false'); });
    document.getElementById('closeRegisterBtn')?.addEventListener('click', () => { registerModal && (registerModal.style.display='none'); });
    document.getElementById('cancelRegister')?.addEventListener('click', () => { registerModal && (registerModal.style.display='none'); });

    registerForm && registerForm.addEventListener('submit', (ev) => {
        ev.preventDefault();
        const fd = new FormData(registerForm);
        const payload = { fullName: fd.get('fullName'), email: fd.get('email'), password: fd.get('password'), role: fd.get('role') };
        try {
            window.UserAPI.registerUser(payload);
            alert('Registered. You can now login.');
            registerModal && (registerModal.style.display='none');
            registerForm.reset();
        } catch (err) { if (registerErr) registerErr.textContent = err.message; }
    });
}

function showPage(id) {
    document.querySelectorAll('.page').forEach(p => {
        p.style.display = (p.id === id) ? '' : 'none';
        p.setAttribute('aria-hidden', p.id === id ? 'false' : 'true');
    });
    if (id === 'records') renderRecordsTable(patientData);
    if (id === 'userManagement') renderUsersTable();
}

function handleLocalCSV(e) {
    const f = e.target.files && e.target.files[0];
    if (!f) return;
    if (dataStatus) dataStatus.textContent = 'Parsing local CSV...';
    Papa.parse(f, { header:true, dynamicTyping:true, skipEmptyLines:true,
        error: (err) => { console.error(err); if (dataStatus) dataStatus.textContent='Error parsing CSV'; },
        complete: (res) => { patientData = (res.data||[]).filter(r=>Object.keys(r).length); if (dataStatus) dataStatus.textContent=`Loaded ${patientData.length} records`; renderRecordsTable(patientData); showPage('records'); }
    });
}

function loadCSVFromServer(url){
    return new Promise((resolve,reject)=>{
        if (dataStatus) dataStatus.textContent=`Loading ${url}...`;
        Papa.parse(url,{download:true,header:true,dynamicTyping:true,skipEmptyLines:true,
            error: err => reject(err),
            complete: res => {
                patientData = (res.data||[]).filter(r=>Object.keys(r).length);
                if (dataStatus) dataStatus.textContent = `Loaded ${patientData.length} records from ${url}`;
                renderRecordsTable(patientData);
                resolve();
            }
        });
    });
}

function renderRecordsTable(data){
    const head=document.getElementById('recordsHead'), body=document.getElementById('recordsBody');
    if(!head||!body) return;
    const search=(document.getElementById('recordSearch')||{value:''}).value.trim().toLowerCase();
    head.innerHTML=''; body.innerHTML='';
    if(!data||!data.length){ body.innerHTML='<tr><td colspan="99">No records loaded.</td></tr>'; return; }
    const cols = Object.keys(data[0]);
    const trh=document.createElement('tr');
    cols.forEach(c=>{ const th=document.createElement('th'); th.textContent=c; trh.appendChild(th); });
    head.appendChild(trh);
    const filtered = data.filter(row=> { if(!search) return true; return Object.values(row).some(v=>String(v).toLowerCase().includes(search)); });
    filtered.forEach(row=>{ const tr=document.createElement('tr'); cols.forEach(c=>{ const td=document.createElement('td'); let v=row[c]; if (v===null||v===undefined) v=''; td.textContent=String(v); tr.appendChild(td); }); body.appendChild(tr); });
}

function renderUsersTable(){
    const tbody = document.getElementById('usersTableBody');
    if(!tbody) return;
    const users = window.UserAPI.getAll();
    tbody.innerHTML = '';
    const current = window.UserAPI.currentUser();
    users.forEach(u=>{
        const perms = u.permissions || [];
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${u.fullName || ''}</td>
            <td>${u.email || ''}</td>
            <td>${u.role || ''}</td>
            <td>
                <label><input type="checkbox" data-uid="${u.id}" data-perm="view_records" ${perms.includes('view_records')?'checked':''}> View</label>
                <label><input type="checkbox" data-uid="${u.id}" data-perm="manage_users" ${perms.includes('manage_users')?'checked':''}> Manage Users</label>
                <label><input type="checkbox" data-uid="${u.id}" data-perm="grant_access" ${perms.includes('grant_access')?'checked':''}> Grant Access</label>
            </td>
            <td>
                ${ (current && (current.permissions.includes('manage_users')||current.role==='admin')) ? `<button data-action="save" data-uid="${u.id}">Save</button> <button data-action="delete" data-uid="${u.id}">Delete</button>` : '' }
            </td>
        `;
        tbody.appendChild(tr);
    });

    tbody.querySelectorAll('button[data-action="save"]').forEach(btn=>{
        btn.addEventListener('click', () => {
            const uid = btn.dataset.uid;
            const checkboxes = tbody.querySelectorAll(`input[data-uid="${uid}"]`);
            const newPerms = [];
            checkboxes.forEach(cb=> { if (cb.checked) newPerms.push(cb.dataset.perm); });
            try {
                window.UserAPI.updateUserPermissions(uid, newPerms);
                alert('Permissions updated');
                renderUsersTable();
            } catch(e){ alert('Update failed: '+e.message); }
        });
    });
    tbody.querySelectorAll('button[data-action="delete"]').forEach(btn=>{
        btn.addEventListener('click', () => {
            const uid = btn.dataset.uid;
            if (!confirm('Delete this user?')) return;
            try {
                window.UserAPI.deleteUser(uid);
                renderUsersTable();
            } catch(e){ alert('Delete failed: '+e.message); }
        });
    });
}