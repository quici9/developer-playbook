// Generic page gate (headless local Chrome, no network beyond the dev server).
// Usage: node pages-check.mjs <baseUrl> <pagesFile> [widths=1280,1920] [themes=light] [themeStorageKey] [extraQuery]
// extraQuery (e.g. "fixture=demo") is appended to every URL, for dev servers whose mock/auth is switched on by a query param.
// pagesFile lines: "page|/path" (must render: no horizontal scroll, no console error, no 404 text)
//                  "redirect|/from?q=1|/to" (final pathname must equal /to and keep the query string)
import { spawn } from "node:child_process";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [BASE, FILE, W = "1280,1920", T = "light", THEME_KEY = "", EXTRA = ""] = process.argv.slice(2);
const withQ = (p) => (EXTRA ? p + (p.includes("?") ? "&" : "?") + EXTRA : p);
const widths = W.split(",").map(Number), themes = T.split(",");
const CHROME = process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const lines = readFileSync(FILE, "utf8").split("\n").map((l) => l.trim()).filter((l) => l && !l.startsWith("#")).map((l) => l.split("|"));
const PORT = 9500 + Math.floor(Math.random() * 300);
const chrome = spawn(CHROME, ["--headless=new", `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), "pc-"))}`, "--no-first-run", "--hide-scrollbars", "about:blank"], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let ws, id = 0; const pending = new Map(); let consoleErrors = [];
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (e) => (await send("Runtime.evaluate", { expression: e, returnByValue: true, awaitPromise: true }))?.result?.value;
let ok = 0, fail = 0;
const report = (good, msg) => { good ? ok++ : fail++; console.log(`${good ? "ok  " : "FAIL"} ${msg}`); };

async function load(url, width, theme) {
  consoleErrors = [];
  await send("Emulation.setDeviceMetricsOverride", { width, height: 900, deviceScaleFactor: 1, mobile: false });
  if (THEME_KEY) await send("Page.addScriptToEvaluateOnNewDocument", { source: `try{localStorage.setItem(${JSON.stringify(THEME_KEY)},${JSON.stringify(theme)})}catch(e){}` });
  await send("Page.navigate", { url });
  for (let i = 0; i < 30; i++) { await sleep(300); if (await ev("document.readyState==='complete' && document.body.innerText.length>40")) break; }
  await sleep(1200);
}
try {
  let tab; for (let i = 0; i < 60 && !tab; i++) { try { tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`, { method: "PUT" })).json(); } catch { await sleep(250); } }
  if (!tab) throw new Error("Chrome did not start");
  ws = new WebSocket(tab.webSocketDebuggerUrl); await new Promise((r) => (ws.onopen = r));
  ws.onmessage = (m) => { const d = JSON.parse(m.data);
    if (d.id && pending.has(d.id)) { pending.get(d.id)(d.result); pending.delete(d.id); }
    if (d.method === "Runtime.exceptionThrown") consoleErrors.push(d.params.exceptionDetails?.text || "exception");
    if (d.method === "Runtime.consoleAPICalled" && d.params.type === "error") consoleErrors.push((d.params.args || []).map((a) => a.value).join(" ")); };
  await send("Page.enable"); await send("Runtime.enable");
  for (const [kind, a, b] of lines) {
    if (kind === "redirect") {
      await load(BASE + withQ(a), widths[0], themes[0]);
      // SPAs may pass through /login or a loader before settling: wait until the URL is stable and off the auth page
      let loc = "", same = 0;
      for (let i = 0; i < 40 && same < 4; i++) {
        await sleep(250);
        const cur = await ev("location.pathname + location.search");
        same = cur === loc && !/\/login/.test(cur) ? same + 1 : 0; loc = cur;
      }
      const q = a.includes("?") ? a.slice(a.indexOf("?") + 1) : "";
      report(loc.startsWith(b) && (!q || loc.includes(q)), `redirect ${a} → ${loc} (want ${b})`);
      continue;
    }
    for (const theme of themes) for (const width of widths) {
      await load(BASE + withQ(a), width, theme);
      const m = await ev(`({sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth, nf:/\\b404\\b|không tìm thấy trang|page not found/i.test(document.body.innerText)})`);
      const probs = [];
      if (m.sw > m.cw + 1) probs.push(`hscroll ${m.sw}>${m.cw}`);
      if (m.nf) probs.push("404 text");
      if (consoleErrors.length) probs.push(`console: ${consoleErrors[0].slice(0, 120)}`);
      report(!probs.length, `${a} ${width} ${theme}${probs.length ? ": " + probs.join("; ") : ""}`);
    }
  }
} finally { try { ws?.close(); } catch {} chrome.kill(); }
console.log(`pages-check: ${ok} ok · ${fail} fail`);
process.exit(fail ? 1 : 0);
