// Designer tooling: screenshot every .frame mockup in a static HTML doc. Usage: node framecap.mjs <file> <outDir> [width]
import { spawn } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
const [FILE, OUT, W = "1680"] = process.argv.slice(2);
mkdirSync(OUT, { recursive: true });
const PORT = 9700 + Math.floor(Math.random() * 200);
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), "fc-"))}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, id = 0; const pending = new Map();
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await send("Runtime.evaluate", { expression: e, returnByValue: true }))?.result?.value;
try {
  let tab; for (let i = 0; i < 60 && !tab; i++) { try { tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json(); } catch { await sleep(250); } }
  ws = new WebSocket(tab.webSocketDebuggerUrl); await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result); pending.delete(d.id); } };
  await send("Page.enable");
  await send("Emulation.setDeviceMetricsOverride", { width: Number(W), height: 1000, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url: "file://" + resolve(FILE) }); await sleep(2000);
  const h = await ev("document.documentElement.scrollHeight");
  await send("Emulation.setDeviceMetricsOverride", { width: Number(W), height: h, deviceScaleFactor: 1, mobile: false }); await sleep(1000);
  const frames = await ev(`[...document.querySelectorAll('.frame')].map(f => { const r = f.getBoundingClientRect(); let h = f, t = ''; while (h && !t) { h = h.previousElementSibling || h.parentElement; if (h && /^H[234]$/.test(h.tagName)) t = h.innerText; } const s = [...document.querySelectorAll('h2')].filter(x => x.getBoundingClientRect().top < r.top).pop(); return { x: r.left, y: r.top + scrollY, w: r.width, h: r.height, t, s: s ? s.innerText : '' }; })`);
  let n = 0;
  for (const f of frames) {
    n++;
    const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: f.x - 8, y: f.y - 8, width: f.w + 16, height: f.h + 16, scale: 1 } });
    const name = `${String(n).padStart(2, "0")}.png`;
    writeFileSync(join(OUT, name), Buffer.from(shot.data, "base64"));
    console.log(`${name}\t${Math.round(f.w)}x${Math.round(f.h)}\t${f.s} | ${f.t}`);
  }
} finally { try { ws?.close(); } catch {} chrome.kill(); }
