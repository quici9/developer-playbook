// Research capture (designer tooling, not product code): for each "name|path" line in a list file, open the dev server
// in a local headless Chrome at the given width, wait for the page to render, save a first-screen PNG, a full-page PNG
// and the visible text of <main>. Usage: node capture.mjs <base> <listFile> <outDir> [width=1440] [height=900]
import { spawn } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [BASE, LIST, OUT, W = "1440", H = "900"] = process.argv.slice(2);
const width = Number(W), height = Number(H);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
mkdirSync(OUT, { recursive: true });
const jobs = readFileSync(LIST, "utf8").split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#")).map((l) => l.split("|"));
const PORT = 9700 + Math.floor(Math.random() * 200);
const profile = mkdtempSync(join(tmpdir(), "research-cap-"));
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, id = 0;
const pending = new Map();
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evalJs = async (expr) => (await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true }))?.result?.value;

try {
  let tab;
  for (let i = 0; i < 60 && !tab; i++) {
    try { tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json(); } catch { await sleep(250); }
  }
  if (!tab) throw new Error("Chrome did not start");
  ws = new WebSocket(tab.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data); if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result); pending.delete(d.id); } };
  await send("Page.enable"); await send("Runtime.enable");
  for (const [name, path, clickSel] of jobs) {
    await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: 1, mobile: false });
    await send("Page.navigate", { url: BASE + path });
    // rendered = some text in <main> (or body for login), no skeleton left
    for (let i = 0; i < 40; i++) {
      await sleep(400);
      const ok = await evalJs(`(() => { const m = document.querySelector('main') || document.body; return m && m.innerText.length > 120 && !document.querySelector('.animate-skeleton'); })()`);
      if (ok) break;
    }
    await sleep(1500);
    if (clickSel) {
      await evalJs(`(() => { const want = ${JSON.stringify(clickSel)}; const el = want.startsWith('text=') ? [...document.querySelectorAll('button,a,[role=button],[role=tab],tr,li,div')].reverse().find(e => e.innerText && e.innerText.trim().startsWith(want.slice(5))) : document.querySelector(want); if (el) el.click(); return !!el; })()`);
      await sleep(1800);
    }
    const first = await send("Page.captureScreenshot", { format: "png" });
    writeFileSync(join(OUT, `${name}-first.png`), Buffer.from(first.data, "base64"));
    const text = await evalJs(`(() => { const d = document.querySelector('[role=dialog]'); const m = document.querySelector('main') || document.body; return (d ? '[DIALOG]\\n' + d.innerText + '\\n[/DIALOG]\\n' : '') + m.innerText; })()`);
    writeFileSync(join(OUT, `${name}.txt`), text || "");
    const full = Math.min(Number(process.env.MAXH || 7000), (await evalJs(`Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)`)) || height);
    if (full > height + 40) {
      await send("Emulation.setDeviceMetricsOverride", { width, height: full, deviceScaleFactor: 1, mobile: false });
      await sleep(1200);
      const shot = await send("Page.captureScreenshot", { format: "png" });
      writeFileSync(join(OUT, `${name}-full.png`), Buffer.from(shot.data, "base64"));
    }
    console.log(`${name}\t${path}\tfull=${full}`);
  }
} finally {
  try { ws?.close(); } catch {}
  chrome.kill();
}
