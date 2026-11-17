path = 'backend/app/static/dashboard.html'
with open(path, encoding='utf-8') as f:
    html = f.read()

# 1. Add auth check and API helper inside <script>
auth_script = """
// --- AUTHENTICATION ---
const token = localStorage.getItem('token');
if (!token) { window.location.href = '/login'; }

function getHeaders() {
    return { 'Authorization': 'Bearer ' + token };
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

// Wrap fetch to always include token
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
    if (!options.headers) options.headers = {};
    if (url.startsWith('/')) options.headers['Authorization'] = 'Bearer ' + token;
    return originalFetch(url, options);
};
// -----------------------

const API = ""; 
let currentCaseId = null;
"""
html = html.replace('const API = ""; \nlet currentCaseId = null;', auth_script)

# 2. Add Logout button to navbar
navbar_logout = """
  <div class="flex items-center gap-4">
    <span class="text-sm text-slate-300">Welcome, <strong id="nav-user"></strong></span>
    <button onclick="logout()" class="text-sm bg-slate-700 hover:bg-slate-600 px-3 py-1 rounded">Logout</button>
  </div>
"""
html = html.replace('<span class="text-sm text-slate-400">Forensic Analysis Engine</span>', navbar_logout)

# 3. Set username on load
html = html.replace('window.onload = () => loadCases();', 'window.onload = () => { document.getElementById("nav-user").innerText = localStorage.getItem("user_name") || "User"; loadCases(); }')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Dashboard secured!")
