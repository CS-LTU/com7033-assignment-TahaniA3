// Simple frontend user store + auth (localStorage). DEMO ONLY — not secure for production.
(function(){
    const KEY = 'app_users_v1';
    const CURR = 'app_current_user_v1';

    function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch(e){ return []; } }
    function save(users){ localStorage.setItem(KEY, JSON.stringify(users)); }

    function seedIfEmpty() {
        const users = load();
        if (users.length === 0) {
            const admin = {
                id: Date.now().toString(),
                fullName: 'Site Admin',
                email: 'admin@example.com',
                password: 'AdminPass', // change immediately
                role: 'admin',
                permissions: ['manage_users','view_records','grant_access']
            };
            users.push(admin);
            save(users);
        }
    }

    function getAll(){ return load(); }
    function findByEmail(email){ return load().find(u => u.email && u.email.toLowerCase() === (email||'').toLowerCase()); }
    function findById(id){ return load().find(u => u.id === id); }

    function registerUser({ fullName, email, password, role }) {
        if (!email || !password) throw new Error('Email and password required');
        const users = load();
        if (users.find(u => u.email.toLowerCase() === email.toLowerCase())) throw new Error('Email already registered');
        const defaultPerms = role === 'admin' ? ['manage_users','view_records','grant_access'] :
                             ['view_records'];
        const user = { id: Date.now().toString(), fullName, email, password, role, permissions: defaultPerms };
        users.push(user);
        save(users);
        return user;
    }

    function authenticate(email, password) {
        const u = findByEmail(email);
        if (!u || u.password !== password) throw new Error('Invalid credentials');
        localStorage.setItem(CURR, JSON.stringify({ id: u.id, email: u.email }));
        return u;
    }

    function signout() { localStorage.removeItem(CURR); }

    function currentUser() {
        const obj = JSON.parse(localStorage.getItem(CURR) || 'null');
        if (!obj) return null;
        return findById(obj.id) || null;
    }

    function updateUserPermissions(userId, newPerms) {
        const users = load();
        const idx = users.findIndex(u=>u.id===userId);
        if (idx === -1) throw new Error('User not found');
        users[idx].permissions = Array.from(new Set(newPerms));
        save(users);
        return users[idx];
    }

    function deleteUser(userId) {
        let users = load();
        users = users.filter(u=>u.id!==userId);
        save(users);
    }

    window.UserAPI = {
        seedIfEmpty, getAll, registerUser, authenticate, signout, currentUser, updateUserPermissions, deleteUser, findById
    };

    seedIfEmpty();
})();