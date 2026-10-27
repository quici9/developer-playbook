// Locate a local Chrome/Chromium/Edge for the headless scripts, on macOS, Linux and Windows. No download, no network.
// Order: $CHROME, then the usual install paths, then the PATH. Exits with a clear message when nothing is found.
import { existsSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join } from "node:path";

const major = Number(process.versions.node.split(".")[0]);
if (major < 22) {
  console.error(`Node ${process.versions.node}: these scripts need Node >= 22 (built-in fetch and WebSocket).`);
  process.exit(2);
}

function onPath(names) {
  const finder = process.platform === "win32" ? "where" : "which";
  for (const n of names) {
    try {
      const hit = execFileSync(finder, [n], { stdio: ["ignore", "pipe", "ignore"] }).toString().split(/\r?\n/)[0].trim();
      if (hit) return hit;
    } catch { /* not found */ }
  }
  return null;
}

export function findChrome() {
  if (process.env.CHROME) return process.env.CHROME;
  const env = process.env;
  const candidates = {
    darwin: [
      "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
      "/Applications/Chromium.app/Contents/MacOS/Chromium",
      "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ],
    win32: [env.PROGRAMFILES, env["PROGRAMFILES(X86)"], env.LOCALAPPDATA].filter(Boolean).flatMap((d) => [
      join(d, "Google", "Chrome", "Application", "chrome.exe"),
      join(d, "Chromium", "Application", "chrome.exe"),
      join(d, "Microsoft", "Edge", "Application", "msedge.exe"),
    ]),
    linux: ["/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium", "/usr/bin/chromium-browser",
            "/snap/bin/chromium", "/usr/bin/microsoft-edge"],
  }[process.platform] || [];
  const hit = candidates.find((p) => existsSync(p))
    || onPath(["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"]);
  if (!hit) {
    console.error("No Chrome/Chromium/Edge found. Install one, or set CHROME=/path/to/chrome.");
    process.exit(2);
  }
  return hit;
}

// Flags that keep headless Chrome working in containers and CI-like Linux boxes (no sandbox user namespace, small /dev/shm).
export const CHROME_FLAGS = process.platform === "linux" ? ["--no-sandbox", "--disable-dev-shm-usage"] : [];
