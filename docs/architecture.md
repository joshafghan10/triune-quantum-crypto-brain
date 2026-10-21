const canvas = document.getElementById('scene');
const ctx = canvas.getContext('2d');
const brainListEl = document.getElementById('brainList');
const messageListEl = document.getElementById('messageList');
const quantumPanel = document.getElementById('quantumPanel');

const brainPositions = {
  perception: { x: 0.22, y: 0.46 },
  research: { x: 0.5, y: 0.25 },
  decision: { x: 0.76, y: 0.58 },
  meta: { x: 0.5, y: 0.75 },
};

const brainPalette = {
  perception: '#6be7ff',
  research: '#7af7a7',
  decision: '#ffc857',
  meta: '#d58bff',
};

const messageColor = {
  neural_only: '#6be7ff',
  symbolic_only: '#7af7a7',
  hybrid: '#ffc857',
  quantum_assisted: '#d58bff',
  disagreement: '#ff7b7b',
  consensus: '#7af7a7',
};

const state = {
  messages: [],
  brains: [],
};

function resizeCanvas() {
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * window.devicePixelRatio;
  canvas.height = rect.height * window.devicePixelRatio;
  ctx.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
}

function updateBrainPanel() {
  const brains = state.brains;
  brainListEl.innerHTML = '';
  for (const brain of brains) {
    const color = brainPalette[brain.name] || '#a8d5ff';
    const row = document.createElement('div');
    row.className = 'brain-card';
    row.innerHTML = `
      <span><span class="status-dot" style="color:${color};background:${color};"></span>${brain.name}</span>
      <span class="meta">${brain.state}</span>
    `;
    brainListEl.appendChild(row);
  }
}

function renderMessagesPanel() {
  const items = state.messages.slice(-6).reverse();
  messageListEl.innerHTML = '';
  for (const item of items) {
    const li = document.createElement('li');
    const type = item.message_type || 'hybrid';
    const color = messageColor[type] || '#6be7ff';
    li.innerHTML = `<span class="tag" style="color:${color};border-color:${color};">${type}</span><strong>${item.sender}</strong> → <strong>${item.receiver}</strong><br>${item.metadata?.decision || item.metadata?.market_state || 'neuro-symbolic update'}`;
    messageListEl.appendChild(li);
  }
}

function drawBackground(width, height) {
  ctx.clearRect(0, 0, width, height);
  const g = ctx.createRadialGradient(width * 0.5, height * 0.35, 20, width * 0.5, height * 0.5, width * 0.7);
  g.addColorStop(0, 'rgba(20,40,60,0.8)');
  g.addColorStop(1, 'rgba(4,9,16,0.95)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, width, height);

  for (let i = 0; i < 35; i++) {
    ctx.fillStyle = 'rgba(255,255,255,0.08)';
    ctx.fillRect(Math.random() * width, Math.random() * height, 1.5, 1.5);
  }
}

function drawBrainClusters(width, height) {
  const nodes = Object.entries(brainPositions);
  for (const [name, pos] of nodes) {
    const x = pos.x * width;
    const y = pos.y * height;
    const radius = 88;
    const color = brainPalette[name] || '#a8d5ff';
    const glow = ctx.createRadialGradient(x, y, 10, x, y, radius);
    glow.addColorStop(0, color + '88');
    glow.addColorStop(0.45, color + '33');
    glow.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();

    ctx.strokeStyle = color;
    ctx.lineWidth = 1.2;
    ctx.beginPath();
    ctx.arc(x, y, 46, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = '#e8f4ff';
    ctx.font = '600 13px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(name, x, y + 4);
  }
}

function drawEdges(width, height) {
  const recent = state.messages.slice(-40);
  for (const msg of recent) {
    const from = brainPositions[msg.sender];
    const to = brainPositions[msg.receiver];
    if (!from || !to) continue;
    const x1 = from.x * width;
    const y1 = from.y * height;
    const x2 = to.x * width;
    const y2 = to.y * height;
    const color = messageColor[msg.message_type] || '#6be7ff';
    const alpha = 0.35 + (msg.priority || 1) * 0.08;

    ctx.strokeStyle = color.replace(')', `, ${alpha})`).replace('rgb', 'rgba');
    ctx.lineWidth = 1 + (msg.priority || 1) * 0.7;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();

    const progress = (performance.now() / 1000 + (msg.priority || 1)) % 1;
    const px = x1 + (x2 - x1) * progress;
    const py = y1 + (y2 - y1) * progress;
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(px, py, 3, 0, Math.PI * 2);
    ctx.fill();
  }
}

function render() {
  const width = canvas.clientWidth || 1200;
  const height = canvas.clientHeight || 800;
  drawBackground(width, height);
  drawEdges(width, height);
  drawBrainClusters(width, height);
}

function handleSocketMessage(payload) {
  if (!payload) return;
  if (payload.event === 'snapshot') {
    state.brains = payload.data.brains || [];
    updateBrainPanel();
  }
  if (payload.event === 'message') {
    const msg = payload.data;
    state.messages.push(msg);
    renderMessagesPanel();
    if (msg.quantum_summary && msg.quantum_summary.used) {
      quantumPanel.innerHTML = `objective: ${msg.quantum_summary.objective}<br>expected value: ${msg.quantum_summary.expected_value}<br>backend: ${msg.quantum_summary.backend}`;
    }
  }
}

async function connect() {
  const socket = new WebSocket(`ws://${location.host}/ws`);
  socket.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      handleSocketMessage(payload);
    } catch (err) {
      console.error('Message parse error', err);
    }
  };
  socket.onclose = () => {
    setTimeout(connect, 1500);
  };
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();
connect();
setInterval(render, 34);
