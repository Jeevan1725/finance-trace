html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Finance Trace - Network Graph</title>
<script src="https://unpkg.com/cytoscape@3.29.2/dist/cytoscape.min.js"></script>
<script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>
<style>
  body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #e2e8f0; }
  #topbar { padding: 16px 24px; background: #1e293b; border-bottom: 1px solid #334155; display: flex; gap: 16px; align-items: center; }
  #topbar h1 { margin: 0; font-size: 18px; font-weight: 600; }
  #topbar input { flex: 1; padding: 8px 12px; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #e2e8f0; font-size: 13px; max-width: 480px; }
  #topbar button { padding: 8px 16px; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; }
  #cy { width: 100%; height: calc(100vh - 65px); }
  #tooltip { position: fixed; pointer-events: none; background: #0f172a; border: 1px solid #475569; padding: 8px 12px; border-radius: 6px; font-size: 12px; color: #e2e8f0; display: none; z-index: 1000; max-width: 300px; }
</style>
</head>
<body>
<div id="topbar">
  <h1>??? Forensic Network Graph</h1>
  <input id="caseId" placeholder="Paste Case UUID..." />
  <button onclick="loadGraph()">Load Graph</button>
  <button onclick="cy.fit()" style="background:#475569">Fit</button>
</div>
<div id="cy"></div>
<div id="tooltip"></div>
<script>
let cy = null;
let currentCaseId = "";

function loadGraph() {
  const caseId = document.getElementById("caseId").value.trim();
  if (!caseId) return alert("Paste a case UUID first");
  currentCaseId = caseId;
  fetch(`/cases/${caseId}/graph`).then(r => r.json()).then(data => renderGraph(data));
}

function renderGraph(data) {
  if (!data.nodes.length) { alert("No graph data yet"); return; }
  const elements = [];
  
  data.nodes.forEach(n => {
    elements.push({ data: { id: n.id, label: n.label, type: n.type, role: n.role } });
  });
  
  data.edges.forEach(e => {
    let width = 1;
    if (e.type === "TRANSACTION") {
      width = Math.max(1, Math.min(10, Math.log10(e.total + 1) * 2));
    }
    elements.push({ data: { id: e.id, source: e.source, target: e.target, label: e.label || "", type: e.type, width: width } });
  });

  if (cy) cy.destroy();
  cy = cytoscape({
    container: document.getElementById("cy"),
    elements,
    style: [
      {
        selector: "node",
        style: {
          "background-color": n => {
            if (n.data("type") === "PERSON") return "#ef4444"; // Red
            if (n.data("type") === "COMPANY") return "#22c55e"; // Green
            return "#3b82f6"; // Blue (Account)
          },
          "label": "data(label)", "color": "#fff", "text-valign": "center", "text-halign": "center",
          "font-size": 12, "font-weight": 600, "width": 60, "height": 60,
          "border-width": 3, "border-color": "#0f172a",
        }
      },
      {
        selector: "edge",
        style: {
          "width": "data(width)", "line-color": "#64748b", "target-arrow-color": "#64748b",
          "target-arrow-shape": "triangle", "curve-style": "bezier", "arrow-scale": 1.5,
        }
      },
      {
        selector: "edge[type='RELATIONSHIP']",
        style: {
          "line-style": "dashed", "line-color": "#a855f7", "target-arrow-color": "#a855f7",
          "width": 2, "label": "data(label)", "font-size": 10, "color": "#d8b4fe", "text-rotation": "autorotate"
        }
      },
      {
        selector: "edge[type='TRANSACTION']",
        style: {
          "label": "data(label)", "font-size": 9, "color": "#94a3b8", "text-rotation": "autorotate"
        }
      }
    ],
    layout: { name: "dagre", rankDir: "LR", nodeSep: 100, rankSep: 150, padding: 40 },
    wheelSensitivity: 0.2
  });
}

const params = new URLSearchParams(window.location.search);
if (params.get("case")) {
  document.getElementById("caseId").value = params.get("case");
  loadGraph();
}
</script>
</body>
</html>"""

with open('backend/app/static/graph.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print('Graph UI updated!')
