html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Finance Trace - Dashboard</title>
<script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 min-h-screen font-sans">

<nav class="bg-slate-900 text-white p-4 shadow-lg flex justify-between items-center">
  <h1 class="text-2xl font-bold tracking-tight">?? Finance Trace</h1>
  <span class="text-sm text-slate-400">Forensic Analysis Engine</span>
</nav>

<div class="container mx-auto p-6 max-w-6xl">
  
  <div id="view-cases">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-bold text-slate-800">Active Cases</h2>
      <button onclick="showCreateCase()" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md shadow font-medium transition">+ New Case</button>
    </div>

    <div id="create-case-form" class="hidden bg-white p-6 rounded-lg shadow-md mb-6 border-l-4 border-blue-500">
      <h3 class="font-bold text-lg mb-4">Create New Case</h3>
      <input type="text" id="new-case-number" placeholder="Case Number (e.g. CASE-002)" class="w-full border p-2 rounded mb-3">
      <input type="text" id="new-case-title" placeholder="Title" class="w-full border p-2 rounded mb-3">
      <textarea id="new-case-desc" placeholder="Description" class="w-full border p-2 rounded mb-3"></textarea>
      <div class="flex gap-2">
        <button onclick="createCase()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded">Save</button>
        <button onclick="hideCreateCase()" class="bg-slate-400 hover:bg-slate-500 text-white px-4 py-2 rounded">Cancel</button>
      </div>
    </div>

    <div id="cases-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div class="text-slate-500 p-4">Loading cases...</div>
    </div>
  </div>

  <div id="view-detail" class="hidden">
    <button onclick="backToCases()" class="text-blue-600 hover:underline mb-4 flex items-center gap-1 font-medium">&larr; Back to Cases</button>
    
    <div class="bg-white p-6 rounded-lg shadow-md mb-6 border-t-4 border-blue-600 flex justify-between items-center">
      <div>
        <h2 id="detail-title" class="text-2xl font-bold text-slate-800 mb-1">Case Title</h2>
        <p id="detail-number" class="text-slate-500 font-mono text-sm">CASE-XXX</p>
      </div>
      <div class="flex gap-3">
        <a id="btn-report" href="#" target="_blank" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded shadow font-medium transition">?? PDF Report</a>
        <a id="btn-graph" href="#" target="_blank" class="bg-teal-600 hover:bg-teal-700 text-white px-4 py-2 rounded shadow font-medium transition">??? View Graph</a>
      </div>
    </div>

    <!-- Entities Section -->
    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <h3 class="font-bold text-lg mb-4 border-b pb-2">?? Entities (Persons & Companies)</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="col-span-2" id="entities-list">Loading entities...</div>
        <div class="col-span-1 border-l pl-4">
          <h4 class="font-semibold text-sm mb-2">Quick Add</h4>
          <button onclick="showAddPerson()" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-2 rounded mb-2 text-sm text-left">+ Add Person (POI/Director)</button>
          <button onclick="showAddCompany()" class="w-full bg-slate-100 hover:bg-slate-200 text-slate-800 px-3 py-2 rounded text-sm text-left">+ Add Company</button>
          
          <div id="add-person-form" class="hidden mt-4 border p-3 rounded bg-slate-50 text-sm">
            <input type="text" id="p-name" placeholder="Full Name" class="w-full border p-1 mb-2 rounded">
            <input type="text" id="p-pan" placeholder="PAN (Optional)" class="w-full border p-1 mb-2 rounded">
            <input type="text" id="p-din" placeholder="DIN (Optional)" class="w-full border p-1 mb-2 rounded">
            <select id="p-role" class="w-full border p-1 mb-2 rounded">
              <option value="POI">Person of Interest (POI)</option>
              <option value="DIRECTOR">Director</option>
              <option value="ASSOCIATE">Associate</option>
              <option value="FAMILY">Family Member</option>
            </select>
            <button onclick="addPerson()" class="bg-blue-600 text-white w-full py-1 rounded">Save Person</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Link Entities Section -->
    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <h3 class="font-bold text-lg mb-4 border-b pb-2">?? Link Entities</h3>
      <div class="flex flex-wrap gap-4 items-end">
        <div class="flex-1 min-w-[200px]">
          <label class="block text-xs font-medium text-slate-700 mb-1">Source Entity</label>
          <select id="rel-source" class="w-full border p-2 rounded text-sm"></select>
        </div>
        <div class="flex-1 min-w-[150px]">
          <label class="block text-xs font-medium text-slate-700 mb-1">Relationship Type</label>
          <select id="rel-type" class="w-full border p-2 rounded text-sm">
            <option value="DIRECTOR_OF">Director Of</option>
            <option value="SHAREHOLDER_OF">Shareholder Of</option>
            <option value="ASSOCIATE">Associate of POI</option>
            <option value="FAMILY">Family Member of POI</option>
          </select>
        </div>
        <div class="flex-1 min-w-[200px]">
          <label class="block text-xs font-medium text-slate-700 mb-1">Target Entity</label>
          <select id="rel-target" class="w-full border p-2 rounded text-sm"></select>
        </div>
        <button onclick="linkEntities()" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm shadow">Link</button>
      </div>
      <div id="relationships-list" class="mt-4 text-sm text-slate-600">Loading links...</div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <h3 class="font-bold text-lg mb-4 border-b pb-2">?? Upload Document</h3>
      <div class="flex flex-col md:flex-row gap-4 items-end">
        <div class="flex-1">
          <select id="doc-type" class="w-full border p-2 rounded">
            <option value="BANK_STMT">Bank Statement</option>
            <option value="ITR">ITR</option>
            <option value="SALE_DEED">Sale Deed</option>
          </select>
        </div>
        <div class="flex-1">
          <input type="file" id="doc-file" accept=".pdf" class="w-full border p-1.5 rounded bg-slate-50">
        </div>
        <button onclick="uploadDocument()" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded shadow">Upload</button>
      </div>
      <p id="upload-status" class="text-sm mt-2 text-blue-600 hidden"></p>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <h3 class="font-bold text-lg mb-4 border-b pb-2">?? Documents</h3>
      <div id="docs-list" class="text-slate-500 text-sm">Loading...</div>
    </div>

    <div class="bg-white p-6 rounded-lg shadow-md mb-6">
      <h3 class="font-bold text-lg mb-4 border-b pb-2">?? Forensic Alerts</h3>
      <div id="alerts-list" class="space-y-2 text-sm">Loading...</div>
    </div>

  </div>
</div>

<script>
const API = ""; 
let currentCaseId = null;
let currentEntities = [];

window.onload = () => loadCases();

function showCreateCase() { document.getElementById('create-case-form').classList.remove('hidden'); }
function hideCreateCase() { document.getElementById('create-case-form').classList.add('hidden'); }

async function loadCases() {
  const res = await fetch(`${API}/cases`);
  const cases = await res.json();
  const list = document.getElementById('cases-list');
  list.innerHTML = cases.length === 0 ? `<div class="col-span-3 text-slate-500 p-4 bg-white rounded">No cases yet.</div>` : "";
  
  cases.forEach(c => {
    const card = document.createElement('div');
    card.className = "bg-white p-5 rounded-lg shadow-md border-l-4 border-blue-600 hover:shadow-lg transition cursor-pointer";
    card.onclick = () => openCase(c.id, c.title, c.case_number);
    card.innerHTML = `
      <h3 class="font-bold text-lg text-slate-800 truncate">${c.title}</h3>
      <p class="text-sm text-slate-500 mb-2">${c.case_number}</p>
      <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded font-medium">${c.status.toUpperCase()}</span>
    `;
    list.appendChild(card);
  });
}

async function createCase() {
  const num = document.getElementById('new-case-number').value;
  const title = document.getElementById('new-case-title').value;
  const desc = document.getElementById('new-case-desc').value;
  if (!num || !title) return alert("Number and Title required");

  const res = await fetch(`${API}/cases`, {
    method: 'POST', headers: {'Content-Type': 'application/json'}, 
    body: JSON.stringify({ case_number: num, title: title, description: desc, created_by: "00000000-0000-0000-0000-000000000001" })
  });
  if (res.ok) { hideCreateCase(); loadCases(); } else { alert("Error creating case"); }
}

function backToCases() {
  document.getElementById('view-detail').classList.add('hidden');
  document.getElementById('view-cases').classList.remove('hidden');
  currentCaseId = null;
  loadCases();
}

async function openCase(id, title, num) {
  currentCaseId = id;
  document.getElementById('view-cases').classList.add('hidden');
  document.getElementById('view-detail').classList.remove('hidden');
  document.getElementById('detail-title').innerText = title;
  document.getElementById('detail-number').innerText = num;
  document.getElementById('btn-report').href = `${API}/cases/${id}/report`;
  document.getElementById('btn-graph').href = `${API}/graph-ui?case=${id}`;

  loadEntities(id);
  loadRelationships(id);
  loadDocuments(id);
  loadAlerts(id);
}

// --- Entities ---
function showAddPerson() { document.getElementById('add-person-form').classList.remove('hidden'); }
function showAddCompany() { alert("To keep UI simple, please use Swagger for adding companies for now."); }

async function loadEntities(caseId) {
  const res = await fetch(`${API}/cases/${caseId}/entities`);
  const data = await res.json();
  currentEntities = [...data.persons.map(p => ({...p, type: 'PERSON'})), ...data.companies.map(c => ({...c, type: 'COMPANY'}))];
  
  const div = document.getElementById('entities-list');
  if (currentEntities.length === 0) { div.innerHTML = "No entities added yet."; return; }
  
  div.innerHTML = currentEntities.map(e => `
    <div class="border-b py-2 flex justify-between">
      <span class="font-medium">${e.type === 'PERSON' ? e.full_name : e.name}</span>
      <span class="text-xs bg-slate-200 px-2 py-1 rounded">${e.type}</span>
    </div>
  `).join('');

  // Populate link dropdowns
  const src = document.getElementById('rel-source');
  const tgt = document.getElementById('rel-target');
  src.innerHTML = currentEntities.map(e => `<option value="${e.id}|${e.type}">${e.type === 'PERSON' ? e.full_name : e.name}</option>`).join('');
  tgt.innerHTML = src.innerHTML;
}

async function addPerson() {
  const name = document.getElementById('p-name').value;
  const pan = document.getElementById('p-pan').value || null;
  const din = document.getElementById('p-din').value || null;
  const role = document.getElementById('p-role').value;
  if (!name) return alert("Name required");

  const res = await fetch(`${API}/cases/${currentCaseId}/persons`, {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ full_name: name, role: role, pan: pan, din: din })
  });
  if (res.ok) { document.getElementById('add-person-form').classList.add('hidden'); loadEntities(currentCaseId); }
  else { alert("Error adding person"); }
}

// --- Relationships ---
async function loadRelationships(caseId) {
  const res = await fetch(`${API}/cases/${caseId}/relationships`);
  const rels = await res.json();
  const div = document.getElementById('relationships-list');
  if (rels.length === 0) { div.innerHTML = "No links yet."; return; }
  
  // Map IDs to names for display
  const getName = (id) => {
    const ent = currentEntities.find(e => e.id === id);
    return ent ? (ent.type === 'PERSON' ? ent.full_name : ent.name) : id;
  };

  div.innerHTML = rels.map(r => `
    <div class="text-xs bg-green-50 text-green-800 p-2 rounded mb-1 border border-green-200">
      ${getName(r.source_id)} <strong>${r.rel_type}</strong> ${getName(r.target_id)}
    </div>
  `).join('');
}

async function linkEntities() {
  const [srcId, srcType] = document.getElementById('rel-source').value.split('|');
  const [tgtId, tgtType] = document.getElementById('rel-target').value.split('|');
  const type = document.getElementById('rel-type').value;

  const body = {
    source_type: srcType, source_id: srcId,
    target_type: tgtType, target_id: tgtId,
    rel_type: type
  };

  const res = await fetch(`${API}/cases/${currentCaseId}/relationships`, {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)
  });
  if (res.ok) { loadRelationships(currentCaseId); } else { alert("Error linking entities"); }
}

// --- Documents & Alerts ---
async function loadDocuments(caseId) {
  const res = await fetch(`${API}/cases/${caseId}/documents`);
  const docs = await res.json();
  const div = document.getElementById('docs-list');
  div.innerHTML = docs.map(d => `
    <div class="flex justify-between items-center border-b py-2">
      <div>
        <span class="font-medium text-slate-800">${d.file_name}</span>
        <span class="text-xs text-slate-500 block font-mono mt-1">Hash: ${d.file_hash.substring(0, 16)}...</span>
      </div>
      <span class="text-xs ${d.parse_status === 'PARSED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'} px-2 py-1 rounded">${d.parse_status}</span>
    </div>
  `).join('') || "No docs.";
}

async function uploadDocument() {
  const fileInput = document.getElementById('doc-file');
  const type = document.getElementById('doc-type').value;
  const status = document.getElementById('upload-status');
  if (fileInput.files.length === 0) return alert("Select a file");

  const formData = new FormData();
  formData.append("doc_type", type);
  formData.append("uploaded_by", "00000000-0000-0000-0000-000000000001");
  formData.append("file", fileInput.files[0]);

  status.classList.remove('hidden');
  status.innerText = "Uploading...";

  const res = await fetch(`${API}/cases/${currentCaseId}/documents`, { method: 'POST', body: formData });
  if (res.ok) { status.innerText = "Success"; fileInput.value = ""; setTimeout(()=>status.classList.add('hidden'), 2000); loadDocuments(currentCaseId); }
}

async function loadAlerts(caseId) {
  const res = await fetch(`${API}/cases/${caseId}/alerts`);
  const alerts = await res.json();
  const div = document.getElementById('alerts-list');
  div.innerHTML = alerts.length === 0 ? `<span class="text-green-600">? No suspicious patterns detected.</span>` : "";
  alerts.forEach(a => {
    const color = a.severity === 'HIGH' ? 'bg-red-50 text-red-800 border-red-200' : 'bg-yellow-50 text-yellow-800 border-yellow-200';
    div.innerHTML += `<div class="p-3 border rounded ${color} font-medium text-sm">${a.message}</div>`;
  });
}
</script>
</body>
</html>"""

with open('backend/app/static/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Dashboard updated with Entities and Relationships!')
