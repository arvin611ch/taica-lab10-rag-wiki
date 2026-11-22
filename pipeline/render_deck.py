"""節點：產生簡報。

讀 deck/outline.json，產生
  docs/slides/index.html        可直接瀏覽的教學簡報（單一 HTML，無外部依賴）
  wiki/queries/deck-outline.md  存回 Wiki 的查詢紀錄（每頁引用哪些主張）

用法：.venv/bin/python -I pipeline/render_deck.py
"""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, all_claims, load_pages  # noqa: E402

OUTLINE = ROOT / "deck" / "outline.json"
OUT_HTML = ROOT / "docs" / "slides" / "index.html"
OUT_QUERY = ROOT / "wiki" / "queries" / "deck-outline.md"

PAGES = {p.rel: p for p in load_pages()}
CLAIMS = all_claims(list(PAGES.values()))


def wiki_href(rel: str, anchor: str = "") -> str:
    return "../wiki/" + rel[:-3] + ".html" + (f"#{anchor}" if anchor else "")


def page_title(rel: str) -> str:
    return PAGES[rel].meta.get("title", rel) if rel in PAGES else rel


def ref_chip(cid: str) -> str:
    c = CLAIMS.get(cid)
    if not c:
        return f'<span class="ref missing">{escape(cid)}</span>'
    return f'<a class="ref" href="{wiki_href(c.page, c.anchor)}" title="{escape(c.title)}">{escape(cid)}</a>'


def point_html(p: dict) -> str:
    tag = {"analogy": '<span class="tag analogy">比喻</span>', "example": '<span class="tag example">例子</span>',
           "project": '<span class="tag project">本專案</span>'}.get(p.get("kind"), "")
    chips = "".join(ref_chip(c) for c in p.get("refs", []))
    chips += "".join(f'<a class="ref wiki" href="{wiki_href(w)}">Wiki：{escape(page_title(w))}</a>' for w in p.get("wiki", []))
    obj = f'<span class="obj">{escape(p["objective"])}</span>' if p.get("objective") else ""
    return f"<li>{obj}{tag}{escape(p['text'])}{chips}</li>"


# ---- 圖 ----------------------------------------------------------------------


def v_chat(v):
    return f"""<div class="chat"><div class="bubble user">{escape(v['q'])}</div>
<div class="bubble bot">{escape(v['a'])}<span class="warn">？</span></div>
<div class="vnote">{escape(v['note'])}</div></div>"""


def v_books(v):
    return """<div class="books">
<div class="book closed"><svg viewBox="0 0 120 90" aria-hidden="true"><rect x="20" y="10" width="80" height="70" rx="6"/><line x1="34" y1="10" x2="34" y2="80"/></svg>
<b>閉卷</b><span>只能靠記憶作答</span><span class="small">＝只靠參數記憶的 LLM</span></div>
<div class="book open"><svg viewBox="0 0 120 90" aria-hidden="true"><path d="M60 20 Q35 8 10 14 V78 Q35 72 60 82 Q85 72 110 78 V14 Q85 8 60 20 Z"/><line x1="60" y1="20" x2="60" y2="82"/></svg>
<b>開卷</b><span>先翻書，再作答</span><span class="small">＝RAG</span></div></div>"""


def v_pipeline(v):
    items = []
    for i, s in enumerate(v["steps"], 1):
        items.append(f'<div class="step"><div class="num">{i}</div><div><b>{escape(s["name"])}</b><span class="when">{escape(s["when"])}</span><p>{escape(s["desc"])}</p></div></div>')
    return '<div class="pipeline">' + '<div class="arrow">↓</div>'.join(items) + "</div>"


def v_chunks(v):
    blocks = "".join(f'<div class="chunk c{i}">第 {i} 塊</div>' for i in range(1, 5))
    return f"""<div class="chunks"><div class="doc"><b>一份長文件</b>{''.join('<i></i>' for _ in range(9))}</div>
<div class="arrow side">→</div><div class="blocks">{blocks}</div></div>"""


def v_vector_map(v):
    pts = [(150, 120, "魔戒裡的壞人", "q"), (205, 165, "反派索倫", "near"), (300, 95, "哈比人的家鄉", "mid"), (320, 290, "今天天氣很好", "far"), (120, 310, "期末考時間", "far")]
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="9" class="{c}"/><text x="{x + 14}" y="{y + 6}" class="{c}">{escape(t)}</text>' for x, y, t, c in pts)
    return f"""<figure class="vmap"><svg viewBox="0 0 520 380" role="img" aria-label="向量地圖示意">
<rect x="1" y="1" width="518" height="378" rx="12" class="frame"/>
<circle cx="170" cy="140" r="78" class="zone"/>{dots}
<text x="24" y="360" class="cap">虛線圈：離問題最近、會被找回來的資料</text></svg>
<figcaption>示意：真實的向量有數百到上千個維度</figcaption></figure>"""


def v_table(v):
    head = "".join(f"<th>{escape(h)}</th>" for h in v["head"])
    rows = "".join("<tr>" + "".join(f"<td>{escape(c)}</td>" for c in r) + "</tr>" for r in v["rows"])
    return f'<table class="vt"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>'


def v_walkthrough(v):
    cards = "".join(f'<div class="wcard"><div class="num">{i}</div><b>{escape(s["step"])}</b><p>{escape(s["text"])}</p></div>' for i, s in enumerate(v["steps"], 1))
    return f'<div class="walk">{cards}</div><div class="vnote">{escape(v["note"])}</div>'


def v_bars(v):
    top = max(b["value"] for b in v["bars"])
    rows = "".join(
        f'<div class="bar"><span class="bl">{escape(b["label"])}</span><span class="track"><span class="fill {b.get("tone", "")}" style="width:{b["value"] / top * 100:.1f}%"></span></span><span class="bv">{b["value"]:g}{escape(v["unit"])}</span></div>'
        for b in v["bars"]
    )
    return f'<figure class="bars"><figcaption>{escape(v["title"])}</figcaption>{rows}</figure>'


def v_u_curve(v):
    return f"""<figure class="ucurve"><svg viewBox="0 0 520 372" role="img" aria-label="U 型曲線示意">
<line x1="60" y1="300" x2="500" y2="300" class="axis"/><line x1="60" y1="30" x2="60" y2="300" class="axis"/>
<line x1="60" y1="150" x2="500" y2="150" class="base"/><text x="150" y="138" class="basel">{escape(v['baseline_label'])}</text>
<path d="M70 60 C 150 230, 330 230, 490 80" class="curve"/>
<text x="70" y="330" class="tick">開頭</text><text x="260" y="330" class="tick">中間</text><text x="450" y="330" class="tick">結尾</text>
<text x="20" y="40" class="tick">正確率</text><text x="200" y="356" class="tick">答案所在的位置</text></svg>
<figcaption>{escape(v['note'])}</figcaption></figure>"""


def v_faithfulness(v):
    rows = "".join(f'<li class="{"ok" if s["ok"] else "no"}"><span>{"✓" if s["ok"] else "✗"}</span>{escape(s["text"])}</li>' for s in v["statements"])
    good = sum(s["ok"] for s in v["statements"])
    return f"""<div class="faith"><div class="ans"><b>模型的答案</b><p>{escape(v['answer'])}</p></div>
<ul>{rows}</ul><div class="score">忠實度 ＝ {good}/{len(v['statements'])}</div><div class="vnote">{escape(v['note'])}：✗ 表示資料裡找不到依據</div></div>"""


def v_timeline(v):
    items = '<div class="arrow side">→</div>'.join(f'<div class="tl"><b>{escape(i["name"])}</b><p>{escape(i["desc"])}</p></div>' for i in v["items"])
    side = v["side"]
    return f'<div class="timeline"><div class="tlrow">{items}</div><div class="tl side"><b>{escape(side["name"])}</b><p>{escape(side["desc"])}</p></div></div>'


VISUALS = {"chat": v_chat, "books": v_books, "pipeline": v_pipeline, "chunks": v_chunks, "vector-map": v_vector_map, "table": v_table,
           "walkthrough": v_walkthrough, "bars": v_bars, "u-curve": v_u_curve, "faithfulness": v_faithfulness, "timeline": v_timeline}


# ---- 投影片 ------------------------------------------------------------------


def footer(s: dict, n: int, total: int) -> str:
    wiki = s.get("wiki", [])
    if wiki:
        src = "Wiki 出處：" + "、".join(f'<a href="{wiki_href(w)}">{escape(page_title(w))}</a>' for w in wiki)
    elif s["kind"] in {"title", "agenda"}:
        src = '知識來源：<a href="../wiki/index.html">RAG 入門 LLM Wiki</a>（7 篇原始資料）'
    else:
        src = "Wiki 出處：見各點的主張編號"
    return f'<footer class="src"><span>{src}</span><span class="pg">{n} / {total}</span></footer>'


def slide_html(s: dict, n: int, total: int, outline: dict) -> str:
    kind = s["kind"]
    if kind == "title":
        inner = f"""<div class="titlebox"><div class="kicker">TAICA Lab 10｜教學簡報</div><h1>{escape(s['title'])}</h1>
<p class="sub">{escape(s['subtitle'])}</p><p class="meta">{escape(s['meta'])}</p><p class="hint">按 → 或空白鍵下一頁，← 上一頁</p></div>"""
    elif kind == "agenda":
        objs = "".join(f'<li><span class="obj">{escape(o["id"])}</span>{escape(o["text"])}</li>' for o in outline["objectives"])
        route = "".join(f"<li>{escape(a)}</li>" for a in s["agenda"])
        inner = f"""<h2>{escape(s['title'])}</h2><div class="body"><div><h3>聽完之後，你能夠……</h3><ul class="points">{objs}</ul></div>
<div><h3>路線</h3><ol class="route">{route}</ol></div></div>"""
    elif kind == "quiz":
        qs = []
        for qi, q in enumerate(s["questions"]):
            choices = "".join(f'<button class="choice" data-ok="{"1" if ci == q["answer"] else "0"}">{"ABCD"[ci]}. {escape(c)}</button>' for ci, c in enumerate(q["choices"]))
            chips = "".join(ref_chip(c) for c in q.get("refs", []))
            qs.append(f"""<div class="q"><p class="qt"><span class="obj">{escape(q['objective'])}</span>{escape(q['q'])}</p><div class="choices">{choices}</div>
<p class="explain" hidden>{escape(q['explain'])}{chips}</p></div>""")
        inner = f'<div class="kicker">{escape(s["section"])}</div><h2>{escape(s["title"])}<small>點選答案看解說</small></h2><div class="quiz">{"".join(qs)}</div>'
    else:
        pts = "".join(point_html(p) for p in s.get("points", []))
        vis = s.get("visual")
        vhtml = VISUALS[vis["type"]](vis) if vis else ""
        layout = "stack" if vis and vis["type"] == "walkthrough" else ("side" if vis else "full")
        extra = ""
        if kind == "summary":
            extra = '<p class="more">想再深入：<a href="../wiki/index.html">打開 Wiki 目錄</a>｜<a href="../wiki/overview.html">總覽</a>｜<a href="../wiki/glossary.html">名詞表</a></p>'
        inner = f"""<div class="kicker">{escape(s.get('section', ''))}</div><h2>{escape(s['title'])}</h2>
<div class="body {layout}"><div class="left"><ul class="points">{pts}</ul>{extra}</div>{f'<div class="visual">{vhtml}</div>' if vhtml else ''}</div>"""
    return f'<section class="slide kind-{kind}" id="{s["id"]}" data-n="{n}">{inner}{footer(s, n, total)}</section>'


CSS = r"""
:root{--paper:#fffdf8;--ink:#1d2433;--muted:#5b6475;--line:#e2dccf;--accent:#0f6e6e;--accent-soft:#e3f1ef;--warm:#c2410c;--warm-soft:#fcebe2;--good:#15803d;--bad:#b91c1c;--mid:#b45309}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:#2a2d33;font-family:"Noto Sans TC","PingFang TC","Microsoft JhengHei",system-ui,sans-serif;color:var(--ink)}
body{overflow:hidden}
#viewport{position:fixed;left:0;right:0;top:0;bottom:52px;display:flex;align-items:center;justify-content:center}
#stage{width:1280px;height:720px;position:relative;flex:none;transform-origin:center center}
.slide{position:absolute;inset:0;background:var(--paper);display:none;flex-direction:column;padding:44px 64px 0;overflow:hidden;border-radius:6px}
.slide.active{display:flex}
.kicker{font-size:18px;font-weight:700;color:var(--accent);letter-spacing:.06em;min-height:22px}
h1{font-size:76px;margin:18px 0 8px;line-height:1.15}
h2{font-size:40px;line-height:1.25;margin:6px 0 22px}
h2 small{font-size:18px;color:var(--muted);font-weight:400;margin-left:16px}
h3{font-size:22px;color:var(--muted);margin:0 0 14px}
.body{flex:1;min-height:0;display:grid;grid-template-columns:1.08fr .92fr;gap:40px;align-items:start}
.body.full{grid-template-columns:1fr}
.body.stack{grid-template-columns:1fr;grid-template-rows:auto 1fr;gap:18px}
ul.points{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:16px}
ul.points li{font-size:25px;line-height:1.5;padding-left:26px;position:relative}
ul.points li::before{content:"";position:absolute;left:2px;top:.62em;width:10px;height:10px;border-radius:50%;background:var(--accent)}
.tag{display:inline-block;font-size:15px;font-weight:700;border-radius:999px;padding:1px 10px;margin-right:8px;vertical-align:3px}
.tag.analogy{background:var(--warm-soft);color:var(--warm)}
.tag.example{background:#eef0f6;color:#3b4a7a}
.tag.project{background:#f3e8ff;color:#6b21a8}
.obj{display:inline-block;font-size:15px;font-weight:700;background:var(--accent);color:#fff;border-radius:6px;padding:1px 8px;margin-right:10px;vertical-align:3px}
.ref{display:inline-block;font-size:13px;line-height:1.5;color:var(--muted);border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-left:6px;text-decoration:none;white-space:nowrap;vertical-align:3px;background:#fff}
.ref:hover{border-color:var(--accent);color:var(--accent)}
.ref.wiki{color:var(--accent)}
.ref.missing{color:var(--bad);border-color:var(--bad)}
footer.src{flex:none;height:54px;margin-top:12px;border-top:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:24px;font-size:15px;color:var(--muted)}
footer.src a{color:var(--accent)}
.pg{white-space:nowrap}
.titlebox{flex:1;display:flex;flex-direction:column;justify-content:center}
.titlebox .sub{font-size:34px;margin:0 0 30px;color:var(--accent)}
.titlebox .meta{font-size:20px;color:var(--muted);margin:0}
.titlebox .hint{font-size:16px;color:var(--muted);margin-top:40px}
ol.route{margin:0;padding-left:30px;font-size:24px;line-height:1.9}
.visual{min-width:0}
.vnote,figcaption{font-size:15px;color:var(--muted);margin-top:10px}
.chat{display:flex;flex-direction:column;gap:16px;padding:24px;background:#f1f3f6;border-radius:16px}
.bubble{font-size:24px;padding:14px 20px;border-radius:18px;max-width:85%}
.bubble.user{align-self:flex-end;background:var(--accent);color:#fff}
.bubble.bot{align-self:flex-start;background:#fff;border:1px solid var(--line)}
.warn{display:inline-block;margin-left:10px;color:var(--bad);font-weight:700}
.books{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.book{display:flex;flex-direction:column;align-items:center;gap:6px;padding:22px 12px;border-radius:16px;border:2px solid var(--line);text-align:center}
.book svg{width:120px;height:90px;fill:none;stroke-width:4}
.book.closed svg{stroke:var(--muted)}.book.open{border-color:var(--accent);background:var(--accent-soft)}.book.open svg{stroke:var(--accent)}
.book b{font-size:30px}.book span{font-size:20px}.book .small{font-size:16px;color:var(--muted)}
.pipeline{display:flex;flex-direction:column;align-items:stretch}
.step{display:flex;gap:16px;align-items:flex-start;padding:14px 18px;border:2px solid var(--accent);border-radius:14px;background:var(--accent-soft)}
.step .num,.wcard .num{flex:none;width:38px;height:38px;border-radius:50%;background:var(--accent);color:#fff;font-weight:700;font-size:20px;display:flex;align-items:center;justify-content:center}
.step b{font-size:24px}.step .when{font-size:15px;color:var(--accent);margin-left:10px;font-weight:700}.step p{margin:4px 0 0;font-size:19px}
.arrow{text-align:center;font-size:26px;color:var(--accent);line-height:1.3}
.arrow.side{align-self:center;padding:0 6px}
.chunks{display:flex;align-items:center;gap:8px}
.doc{width:190px;padding:16px;border:2px solid var(--muted);border-radius:8px;display:flex;flex-direction:column;gap:9px}
.doc b{font-size:18px}.doc i{display:block;height:8px;background:#d9d4c8;border-radius:4px}
.blocks{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.chunk{padding:26px 8px;text-align:center;border-radius:10px;font-size:20px;font-weight:700;color:#fff}
.c1{background:#0f6e6e}.c2{background:#2f8f83}.c3{background:#5aa89a}.c4{background:#86c1b4}
.vmap svg{width:100%;height:auto}
.vmap .frame{fill:#fbfaf6;stroke:var(--line)}.vmap .zone{fill:var(--accent-soft);stroke:var(--accent);stroke-dasharray:8 6;stroke-width:2}
.vmap circle.q{fill:var(--warm)}.vmap circle.near{fill:var(--accent)}.vmap circle.mid{fill:#7c8aa5}.vmap circle.far{fill:#b8bfcc}
.vmap text{font-size:19px;fill:var(--ink)}.vmap text.far{fill:var(--muted)}.vmap text.q{font-weight:700;fill:var(--warm)}.vmap .cap{font-size:15px;fill:var(--muted)}
table.vt{width:100%;border-collapse:collapse;font-size:21px}
table.vt th{background:var(--accent);color:#fff;padding:10px;text-align:left}
table.vt td{padding:12px 10px;border-bottom:1px solid var(--line)}
table.vt td:first-child{font-weight:700;color:var(--muted);white-space:nowrap}
.walk{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.wcard{border:2px solid var(--accent);border-radius:14px;padding:14px;background:var(--accent-soft);display:flex;flex-direction:column;gap:8px}
.wcard b{font-size:22px}.wcard p{margin:0;font-size:19px;line-height:1.5}
.bars{margin:0;display:flex;flex-direction:column;gap:14px}
.bars figcaption{font-size:18px;font-weight:700;color:var(--ink);margin:0 0 4px}
.bar{display:grid;grid-template-columns:200px 1fr 64px;gap:10px;align-items:center}
.bl{font-size:16px;line-height:1.3}.bv{font-size:20px;font-weight:700;text-align:right}
.track{height:24px;background:#efece4;border-radius:6px;overflow:hidden}
.fill{display:block;height:100%;background:var(--accent)}.fill.good{background:var(--good)}.fill.bad{background:var(--bad)}.fill.mid{background:var(--mid)}
.ucurve{margin:0}.ucurve svg{width:100%;height:auto}
.ucurve .axis{stroke:var(--muted);stroke-width:2}.ucurve .base{stroke:var(--bad);stroke-width:2;stroke-dasharray:8 6}
.ucurve .curve{fill:none;stroke:var(--accent);stroke-width:6;stroke-linecap:round}
.ucurve .tick{font-size:17px;fill:var(--muted)}.ucurve .basel{font-size:17px;fill:var(--bad)}
.faith .ans{padding:14px 18px;background:#f1f3f6;border-radius:12px}.faith .ans b{font-size:17px;color:var(--muted)}.faith .ans p{margin:4px 0 0;font-size:20px}
.faith ul{list-style:none;padding:0;margin:14px 0;display:flex;flex-direction:column;gap:8px}
.faith li{font-size:21px;display:flex;gap:10px;align-items:center}.faith li span{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700}
.faith li.ok span{background:var(--good)}.faith li.no span{background:var(--bad)}
.faith .score{font-size:26px;font-weight:700;color:var(--accent)}
.timeline{display:flex;flex-direction:column;gap:18px}
.tlrow{display:flex;align-items:stretch}
.tl{flex:1;border:2px solid var(--accent);border-radius:12px;padding:12px;background:var(--accent-soft)}
.tl b{font-size:19px}.tl p{margin:6px 0 0;font-size:16px;line-height:1.4}
.tl.side{border-color:var(--warm);background:var(--warm-soft)}
.quiz{flex:1;min-height:0;display:grid;grid-template-columns:1fr 1fr;gap:28px;align-items:start}
.q{border:2px solid var(--line);border-radius:16px;padding:18px 20px}
.qt{font-size:23px;line-height:1.45;margin:0 0 14px}
.choices{display:grid;grid-template-columns:1fr;gap:10px}
.choice{font:inherit;font-size:20px;text-align:left;padding:10px 14px;border-radius:10px;border:2px solid var(--line);background:#fff;cursor:pointer}
.choice:hover{border-color:var(--accent)}
.choice.right{border-color:var(--good);background:#e8f5ec}.choice.wrong{border-color:var(--bad);background:#fbeaea}
.explain{font-size:18px;line-height:1.5;margin:12px 0 0;color:var(--ink)}
.more{font-size:20px;margin-top:26px}.more a{color:var(--accent)}
#bar{position:fixed;left:0;right:0;bottom:0;height:52px;display:flex;align-items:center;justify-content:center;gap:16px;color:#e8e8e8;font-size:16px;background:#1d1f24}
#bar button{font:inherit;color:#fff;background:#3a3f48;border:0;border-radius:8px;padding:6px 16px;cursor:pointer}
#bar button:focus-visible,.choice:focus-visible,a:focus-visible{outline:3px solid #f59e0b;outline-offset:2px}
#progress{position:fixed;left:0;bottom:52px;height:4px;background:#f59e0b;transition:width .2s}
#bar a{color:#9fd8cf}
"""

JS = r"""
const slides=[...document.querySelectorAll('.slide')];
const stage=document.getElementById('stage');
let cur=0;
function fit(){const s=Math.min(innerWidth/1280,(innerHeight-52)/720);stage.style.transform=`scale(${s})`;}
function show(n){cur=Math.max(0,Math.min(slides.length-1,n));slides.forEach((el,k)=>el.classList.toggle('active',k===cur));
 document.getElementById('count').textContent=`${cur+1} / ${slides.length}`;
 document.getElementById('progress').style.width=`${(cur+1)/slides.length*100}%`;
 history.replaceState(null,'',`#${cur+1}`);}
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(cur+1);}
 else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(cur-1);}
 else if(e.key==='Home')show(0);else if(e.key==='End')show(slides.length-1);});
document.getElementById('prev').onclick=()=>show(cur-1);
document.getElementById('next').onclick=()=>show(cur+1);
let tx=null;addEventListener('touchstart',e=>{tx=e.touches[0].clientX},{passive:true});
addEventListener('touchend',e=>{if(tx===null)return;const d=e.changedTouches[0].clientX-tx;if(Math.abs(d)>50)show(cur+(d<0?1:-1));tx=null;});
document.querySelectorAll('.q').forEach(q=>q.querySelectorAll('.choice').forEach(b=>b.addEventListener('click',()=>{
 q.querySelectorAll('.choice').forEach(c=>{c.classList.remove('right','wrong');if(c.dataset.ok==='1')c.classList.add('right');});
 if(b.dataset.ok!=='1')b.classList.add('wrong');q.querySelector('.explain').hidden=false;})));
addEventListener('resize',fit);fit();
const start=parseInt(location.hash.slice(1),10);show(Number.isFinite(start)?start-1:0);
"""


def build_html(outline: dict) -> str:
    slides = outline["slides"]
    body = "\n".join(slide_html(s, i, len(slides), outline) for i, s in enumerate(slides, 1))
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(outline['title'])}｜{escape(outline['subtitle'])}</title><style>{CSS}</style></head>
<body><div id="viewport"><div id="stage">
{body}
</div></div><div id="progress"></div>
<nav id="bar" aria-label="換頁"><button id="prev" aria-label="上一頁">←</button><span id="count"></span><button id="next" aria-label="下一頁">→</button>
<a href="../index.html">專案首頁</a><a href="../wiki/index.html">Wiki</a></nav>
<script>{JS}</script></body></html>
"""


def build_query_page(outline: dict) -> str:
    lines = ["---", "title: 查詢紀錄：教學簡報大綱", "type: query", "updated: 2026-11-23", "---",
             "# 查詢紀錄：教學簡報大綱", "",
             "**查詢：** 怎麼用這個 Wiki，教沒學過機器學習的大學生認識 RAG？", "",
             "**做法：** 先讀 [目錄](../index.md) 與 [總覽](../overview.md)，依學習目標挑概念頁，每個重點都對到來源頁的主張。結果寫成 `deck/outline.json`，再由程式產生簡報與這一頁，所以兩者永遠一致。", "",
             "## 學習目標", ""]
    lines += [f"- **{o['id']}** {o['text']}" for o in outline["objectives"]]
    lines += ["", "## 每頁引用了 Wiki 的哪些內容", "", "| 頁 | 標題 | 目標 | 主張 | 概念頁 |", "| --- | --- | --- | --- | --- |"]
    for i, s in enumerate(outline["slides"], 1):
        refs = []
        for p in s.get("points", []) + s.get("questions", []):
            refs += [r for r in p.get("refs", []) if r not in refs]
        for r in (s.get("visual") or {}).get("refs", []):
            if r not in refs:
                refs.append(r)
        chips = "、".join(f"[{r}](../{CLAIMS[r].page}#{CLAIMS[r].anchor})" for r in refs if r in CLAIMS) or "—"
        wiki = "、".join(f"[{page_title(w)}](../{w})" for w in s.get("wiki", [])) or "—"
        kinds = {p.get("kind") for p in s.get("points", [])} - {None}
        note = "（含比喻）" if "analogy" in kinds else ""
        note += "（示意例子）" if "example" in kinds else ""
        obj = s.get("objective") or "、".join(sorted({q["objective"] for q in s.get("questions", [])})) or "—"
        lines.append(f"| {i} | {s['title']}{note} | {obj} | {chips} | {wiki} |")
    lines += ["", f"簡報網址：[docs/slides/index.html](https://arvin611ch.github.io/taica-lab10-rag-wiki/slides/)", ""]
    return "\n".join(lines)


def main() -> int:
    outline = json.loads(OUTLINE.read_text(encoding="utf-8"))
    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(build_html(outline), encoding="utf-8")
    OUT_QUERY.parent.mkdir(parents=True, exist_ok=True)
    OUT_QUERY.write_text(build_query_page(outline), encoding="utf-8")
    print(f"簡報 {len(outline['slides'])} 頁 → {OUT_HTML.relative_to(ROOT)}；查詢紀錄 → {OUT_QUERY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
