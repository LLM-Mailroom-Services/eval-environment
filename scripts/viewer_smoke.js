#!/usr/bin/env node
// Headless smoke test for web/index.html — stubs the DOM, feeds the real
// web/data/snapshot.json, and routes through every view to catch runtime
// errors (leaked undefined/NaN, empty renders, broken routes) without a
// browser. Run: node scripts/viewer_smoke.js   (requires node, no deps)
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = process.argv[2] || path.resolve(__dirname, "..");
const snapshot = JSON.parse(fs.readFileSync(path.join(ROOT, "web/data/snapshot.json"), "utf8"));
const html = fs.readFileSync(path.join(ROOT, "web/index.html"), "utf8");
const js = html.match(/<script>([\s\S]*?)<\/script>/)[1];

const elements = {};
function makeEl(id) {
    return {
        id, innerHTML: "", textContent: "", value: "", checked: false,
        dataset: {}, href: "",
        classList: { toggle() {}, add() {}, remove() {} },
        addEventListener() {}, listeners: {},
    };
}
// Pre-seed controls so filter/compare paths execute with real values:
// compare needs two runs of one task; runs filters get defaults.
const byTask = {};
snapshot.runs.forEach(r => (byTask[r.task] = byTask[r.task] || []).push(r));
const pairTask = Object.keys(byTask).find(t => byTask[t].length >= 2);
const seeded = { rq: "", rf: "", rm: "", tt: "", tm: "", to: "" };
if (pairTask) {
    seeded.ca = byTask[pairTask][0].run_id;
    seeded.cb = byTask[pairTask][byTask[pairTask].length - 1].run_id;
}
for (const [id, v] of Object.entries(seeded)) { elements[id] = makeEl(id); elements[id].value = v; }

global.document = {
    getElementById: id => elements[id] || (elements[id] = makeEl(id)),
    querySelectorAll: () => [],
};
const winListeners = {};
global.window = { addEventListener: (ev, fn) => { winListeners[ev] = fn; }, scrollTo() {} };
global.location = { hash: "#/dashboard" };
global.fetch = async () => ({ ok: true, json: async () => snapshot });

eval(js); // defines the viewer and calls load()

(async () => {
    await new Promise(r => setTimeout(r, 50)); // let load() resolve
    if (!elements.main || !elements.main.innerHTML.includes("Dashboard")) throw new Error("dashboard did not render");
    const views = ["#/dashboard", "#/runs", "#/trends", "#/compare", "#/tasks", "#/corpus", "#/prompts", "#/environment"];
    const detail = snapshot.runs[0];
    if (detail) views.push("#/run/" + detail.run_id);
    const cal = snapshot.runs.find(r => r.family === "calibration");
    if (cal) views.push("#/run/" + cal.run_id);
    const failed = snapshot.runs.find(r => r.error);
    if (failed) views.push("#/run/" + failed.run_id);

    for (const v of views) {
        global.location.hash = v;
        winListeners.hashchange();
        const out = elements.main.innerHTML;
        if (!out || out.length < 200) throw new Error("view " + v + " rendered nothing");
        if (/>\s*undefined\s*</.test(out) || />NaN</.test(out)) {
            const m = out.match(/.{80}(undefined|NaN).{80}/);
            throw new Error("view " + v + " leaked undefined/NaN: …" + (m ? m[0] : "?") + "…");
        }
        console.log("OK", v, "(" + out.length + " chars)");
    }
    if (pairTask && (!elements["cmp-out"] || !elements["cmp-out"].innerHTML.includes("Metric deltas"))) {
        throw new Error("compare output did not render");
    }
    if (elements.rbody && !(elements.rbody.innerHTML.match(/<tr/g) || []).length) {
        throw new Error("runs table body is empty");
    }
    console.log("ALL VIEWS PASS (" + snapshot.runs.length + " runs)");
})().catch(err => { console.error("FAIL:", err.message); process.exit(1); });
