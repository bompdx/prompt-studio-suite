#!/usr/bin/env python3
"""Build the local launcher for the ten standalone Prompt Studios."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
files = sorted(p for p in (ROOT / "data").glob("[0-9][0-9]-*.json") if not p.name.startswith("00-"))
studios = [json.loads(path.read_text(encoding="utf-8")) for path in files]

cards = "\n".join(
    f'''<a class="studio-card" href="{html.escape(s['slug'])}-prompt-studio.html" style="--studio:{html.escape(s['accent'])};--studio2:{html.escape(s['accent2'])}">
      <strong>{html.escape(s['title'].replace(' Prompt Studio', ''))}</strong>
      <span class="card-link">Open studio <i aria-hidden="true">→</i></span>
    </a>'''
    for i, s in enumerate(studios, 1)
)

doc = f'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Prompt Studio Suite</title>
  <style>
    :root {{ color-scheme:light; --ink:#16201c; --muted:#607068; --paper:#f2f0e9; --panel:#fffefa; --line:rgba(22,32,28,.14); --shadow:0 24px 70px rgba(20,31,26,.11); }}
    html[data-theme="dark"] {{ color-scheme:dark; --ink:#f5f1e8; --muted:#b8c4bd; --paper:#0d1310; --panel:#17201b; --line:rgba(245,241,232,.13); --shadow:0 28px 80px rgba(0,0,0,.38); }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; min-height:100vh; color:var(--ink); background:radial-gradient(circle at 10% 0,rgba(31,122,90,.15),transparent 28rem),radial-gradient(circle at 90% 10%,rgba(214,161,31,.14),transparent 25rem),var(--paper); font-family:Avenir Next,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    body::before {{ content:""; position:fixed; inset:0; pointer-events:none; z-index:-1; opacity:.3; background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px); background-size:64px 64px; mask-image:linear-gradient(black,transparent 75%); }}
    a {{ color:inherit; text-decoration:none; }} button {{ font:inherit; cursor:pointer; }} :focus-visible {{ outline:3px solid #1f7a5a; outline-offset:4px; }}
    .shell {{ width:min(100% - 40px,1240px); margin:auto; padding:18px 0 40px; }}
    .topbar {{ display:flex; justify-content:space-between; align-items:center; gap:16px; padding:8px; border:1px solid var(--line); border-radius:18px; background:var(--panel); box-shadow:0 8px 24px rgba(20,31,26,.08); }}
    .brand {{ display:flex; align-items:center; gap:11px; padding:4px 8px 4px 5px; font-weight:900; }}
    .mark {{ position:relative; width:34px; height:34px; border-radius:10px; background:#1f7a5a; }} .mark::before {{ content:""; position:absolute; left:8px; right:8px; top:10px; height:3px; border-radius:9px; background:white; box-shadow:0 6px 0 rgba(255,255,255,.72),0 12px 0 rgba(255,255,255,.45); }}
    .theme {{ display:flex; gap:4px; padding:4px; border:1px solid var(--line); border-radius:12px; }} .theme button {{ min-width:54px; min-height:36px; border:0; border-radius:9px; color:var(--muted); background:transparent; font-weight:800; }} .theme button.active {{ background:var(--ink); color:var(--paper); }}
    .hero {{ margin-top:18px; padding:clamp(30px,6vw,72px); border:1px solid var(--line); border-radius:30px; background:var(--panel); box-shadow:var(--shadow); overflow:hidden; position:relative; }}
    .hero::after {{ content:""; position:absolute; width:280px; height:280px; right:-140px; bottom:-165px; border:44px solid rgba(214,161,31,.22); border-radius:50%; }}
    .kicker {{ margin:0 0 12px; color:#1f7a5a; font:900 .72rem/1.2 ui-monospace,SFMono-Regular,Menlo,monospace; text-transform:uppercase; letter-spacing:.12em; }}
    h1 {{ margin:0; max-width:760px; font-size:clamp(3rem,8vw,6.5rem); line-height:.88; letter-spacing:-.065em; }}
    .intro {{ max-width:680px; margin:23px 0 0; color:var(--muted); font-size:clamp(1.05rem,2vw,1.24rem); font-weight:620; line-height:1.65; }}
    .section-head {{ margin:42px 0 16px; }} h2 {{ margin:0; font-size:clamp(1.8rem,4vw,2.8rem); letter-spacing:-.04em; }}
    .grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }}
    .studio-card {{ position:relative; min-height:160px; display:grid; align-content:space-between; gap:16px; padding:23px; border:1px solid var(--line); border-radius:20px; background:var(--panel); overflow:hidden; transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease; }}
    .studio-card::after {{ content:""; position:absolute; inset:auto 0 0; height:5px; background:linear-gradient(90deg,var(--studio),var(--studio2)); transform:scaleX(.18); transform-origin:left; transition:transform .22s ease; }}
    .studio-card:hover {{ transform:translateY(-4px); border-color:var(--studio); box-shadow:var(--shadow); }} .studio-card:hover::after {{ transform:scaleX(1); }}
    .studio-card strong {{ max-width:520px; font-size:clamp(1.6rem,3vw,2.45rem); line-height:1; letter-spacing:-.045em; }} .card-link {{ color:var(--studio); font-weight:900; }}
    footer {{ display:flex; justify-content:space-between; gap:16px; padding:28px 4px 0; color:var(--muted); font:700 .75rem/1.4 ui-monospace,SFMono-Regular,Menlo,monospace; }}
    @media(max-width:760px) {{ .shell {{ width:min(100% - 22px,1240px); padding-top:10px; }} .hero,.grid {{ grid-template-columns:1fr; }} .hero {{ padding:30px 22px; border-radius:22px; }} .section-head {{ display:block; }} .section-head p {{ margin-top:9px; }} .studio-card {{ min-height:230px; }} footer {{ display:block; text-align:center; }} footer span {{ display:block; margin:4px 0; }} }}
    @media(prefers-reduced-motion:reduce) {{ *,*::before,*::after {{ transition-duration:.001ms!important; }} }}
  </style>
</head>
<body><div class="shell">
  <header class="topbar"><div class="brand"><span class="mark" aria-hidden="true"></span><span>Prompt Studio Suite</span></div><div class="theme" role="group" aria-label="Theme selection"><button type="button" data-theme="light">Light</button><button type="button" data-theme="dark">Dark</button></div></header>
  <main><section class="hero"><div><h1>Prompt Studio</h1><p class="intro">Choose a studio to get started.</p></div></section>
  <div class="section-head"><h2>Choose your studio</h2></div><section class="grid" aria-label="Prompt studios">{cards}</section></main>
  <footer><span>Prompt Studio Suite</span></footer>
</div><script>
  const root=document.documentElement,buttons=document.querySelectorAll('[data-theme]');
  function setTheme(theme){{root.dataset.theme=theme;localStorage.setItem('prompt-suite-theme',theme);buttons.forEach(b=>b.classList.toggle('active',b.dataset.theme===theme));}}
  buttons.forEach(b=>b.addEventListener('click',()=>setTheme(b.dataset.theme)));
  setTheme(localStorage.getItem('prompt-suite-theme')||((matchMedia('(prefers-color-scheme:dark)').matches)?'dark':'light'));
</script></body></html>'''

(ROOT / "dist" / "index.html").write_text(doc, encoding="utf-8")
print(f"built {ROOT / 'dist' / 'index.html'}")
