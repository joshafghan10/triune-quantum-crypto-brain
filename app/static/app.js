<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{{ title }}</title>
    <style>
      :root {
        --bg: #050b16;
        --panel: rgba(16, 26, 38, 0.8);
        --cyan: #6be7ff;
        --green: #7af7a7;
        --purple: #d58bff;
        --red: #ff7b7b;
        --amber: #ffc857;
        --text: #e8f4ff;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: Inter, system-ui, sans-serif;
        background: radial-gradient(circle at top, #0d1830, #050b16 58%);
        color: var(--text);
        overflow: hidden;
      }
      .layout {
        display: grid;
        grid-template-columns: 1.6fr 340px;
        width: 100vw;
        height: 100vh;
      }
      .viewport {
        position: relative;
        border-right: 1px solid rgba(255,255,255,0.08);
      }
      canvas {
        display: block;
        width: 100%;
        height: 100%;
        background: linear-gradient(180deg, rgba(10,18,30,0.94), rgba(5,11,22,0.98));
      }
      .sidebar {
        padding: 16px 18px;
        background: rgba(11, 16, 25, 0.84);
        overflow: auto;
      }
      .panel {
        background: var(--panel);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 14px;
        box-shadow: 0 0 16px rgba(90, 180, 255, 0.08);
      }
      .panel h3 {
        margin: 0 0 10px 0;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #9dc9ff;
      }
      .brain-card {
        display: flex; justify-content: space-between; align-items: center;
        margin: 8px 0;
        font-size: 13px;
      }
      .status-dot {
        width: 9px; height: 9px; border-radius: 50%; display: inline-block; margin-right: 8px;
        box-shadow: 0 0 12px currentColor;
      }
      .meta {
        font-size: 12px;
        color: rgba(232,244,255,0.74);
      }
      .message-list {
        list-style: none; margin: 0; padding: 0;
      }
      .message-list li {
        border-bottom: 1px solid rgba(255,255,255,0.06);
        padding: 8px 0;
        font-size: 12px;
        line-height: 1.35;
      }
      .tag {
        display: inline-block; padding: 2px 6px; border-radius: 999px; font-size: 10px;
        border: 1px solid rgba(255,255,255,0.08); margin-right: 6px;
      }
      .cyan { color: var(--cyan); }
      .green { color: var(--green); }
      .purple { color: var(--purple); }
      .red { color: var(--red); }
      .amber { color: var(--amber); }
    </style>
  </head>
  <body>
    <div class="layout">
      <div class="viewport">
        <canvas id="scene"></canvas>
      </div>
      <aside class="sidebar">
        <div class="panel">
          <h3>Brains</h3>
          <div id="brainList"></div>
        </div>
        <div class="panel">
          <h3>Latest Messages</h3>
          <ul id="messageList" class="message-list"></ul>
        </div>
        <div class="panel">
          <h3>Quantum Jobs</h3>
          <div id="quantumPanel" class="meta">Waiting for quantum-assisted messages.</div>
        </div>
      </aside>
    </div>

    <script src="/static/app.js"></script>
  </body>
</html>
