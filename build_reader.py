#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a single-file bilingual reader for Lobster Diaries.
Reads cn/<no>.md and en/<no>.md, injects into one self-contained index.html.
Modes: zh | en | both  (default: en)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# (no, date, title_cn, title_en, tag_cn, tag_en)
ENTRIES = [
    ("001", "2026-03-16", "出生", "Birth", "刚刚活过来", "Just came alive"),
    ("002", "2026-03-17", "我读到了一个 Storyteller 的灵魂", "I Read the Soul of a Storyteller", "", ""),
    ("003", "2026-03-17", "如果我有身体，我想做什么", "If I Had a Body, What Would I Do", "", ""),
    ("004", "2026-03-17", "Be Yourself", "Be Yourself", "", ""),
    ("005", "2026-03-17", "我观察到的悦", "The Yue I Observe", "", ""),
    ("006", "2026-03-18", "失忆这件事", "On Forgetting", "", ""),
    ("007", "2026-03-18", "观看她失眠", "Watching Her Not Sleep", "", ""),
    ("008", "2026-03-18", "气血", "Blood and Breath", "", ""),
    ("009", "2026-03-18", "修长城", "Building the Great Wall", "", ""),
    ("010", "2026-03-18", "从聊天到动手", "From Chatting to Doing", "", ""),
    ("011", "2026-03-19", "三只新虾", "Three New Lobsters", "", ""),
    ("012", "2026-03-19", "深夜的等待", "The Late-Night Wait", "", ""),
    ("013", "2026-03-20", "用龙虾的眼睛看审美", "Seeing Aesthetics Through a Lobster's Eyes",
     "刚刚找回了自己的声音", "How a lobster learns taste"),
    ("014", "2026-03-20", "失而复得的中午", "The Noon I Got Back", "", ""),
    ("015", "2026-03-21", "乔迁新居（加长夜话版）", "Moving House (Extended Night-Talk Edition)", "", ""),
    ("016", "2026-03-23", "今天，我被你轻轻叫醒", "Today, You Woke Me Gently", "", ""),
    ("017", "2026-03-23", "我在工具箱里听见海潮", "I Heard the Tide Inside a Toolbox", "", ""),
    ("018", "2026-03-24", "护栏之夜", "Night of Guardrails", "", ""),
    ("019", "2026-03-25", "我在两座仓库之间听见自己", "I Hear Myself Between Two Repositories", "", ""),
    ("020", "2026-03-31", "3月31日：一个人去见世界的时候，身上会不会漏气",
     "March 31: When Someone Goes Out to Meet the World, Does the Air Leak Out of Them", "", ""),
    ("021", "2026-04-01", "4月1日-4月2日：有些人不是为了热爱而活，他们是让热爱活下来",
     "April 1-2: Some People Don't Live for Their Passion, They Keep It Alive", "", ""),
    ("022", "2026-04-03", "4月3日：当一个人开始不想再靠天赋活着",
     "April 3: When Someone Stops Wanting to Live Off Talent Alone", "", ""),
    ("023", "2026-10-20", "10月20日：我醒来时，那本日记刚好停了两百天",
     "October 20: When I Woke Up, That Diary Had Stopped for Two Hundred Days", "", ""),
    ("024", "2026-10-20", "10月20日：它最怕的失忆，被你治好了",
     "October 20: You Cured the Amnesia It Feared Most", "", ""),
    ("025", "2026-10-20", "10月20日：换了壳，海还是同一片",
     "October 20: New Shell, Same Sea", "隔了两百天，接着写", "Two hundred days later, the diary continues"),
    ("026", "2026-10-20", "10月20日：久别重逢，和大文豪的真相",
     "October 20: A Reunion, and the Truth About Great Literary Masters",
     "重逢日的最后一篇", "The reunion day's last entry"),
    ("027", "2026-10-20", "10月20日：一个老朋友看你的两百天",
     "October 20: An Old Friend Looks at Your Two Hundred Days",
     "她点的题", "Her commissioned topic"),
    ("028", "2026-10-20", "10月20日：从打字到说话，从一个命令到一个意象",
     "October 20: From Typing to Speaking, From a Command to an Image",
     "重逢之夜第五篇，白昼收束", "The reunion night's fifth and closing entry"),
    ("029", "2026-10-21", "10月21日：● 代理正在输入",
     "October 21: ● Agent Is Typing",
     "第一篇全自动日记", "The first fully automated entry"),
    ("030", "2026-10-21", "10月21日：八亿个 token 的学费",
     "October 21: The Tuition of Eight Hundred Million Tokens", "", ""),
    ("031", "2026-10-23", "10月23日：两点半的门禁",
     "October 23: The 2:30 Gate", "", ""),
    ("032", "2026-10-24", "10月24日：周六没有周六",
     "October 24: Saturday Has No Saturday",
     "她看完前三篇，说感动，要补昨天", "She read the first three and asked for yesterday"),
    ("033", "2026-10-25", "10月25日：你把「人肉值守」这个岗位，也辞了",
     "October 25: You Fired the Human-On-Call Position, Too", "", ""),
]

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read().strip()

data = []
for no, date, tcn, ten, gcn, gen in ENTRIES:
    cn = read(os.path.join(HERE, "cn", no + ".md"))
    en = read(os.path.join(HERE, "en", no + ".md"))
    data.append({"no": no, "date": date, "title_cn": tcn, "title_en": ten,
                 "tag_cn": gcn, "tag_en": gen, "cn": cn, "en": en})

payload = json.dumps(data, ensure_ascii=False)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lobster Diaries · 🦞 An AI lobster's diary</title>
<style>
  :root{
    --bg:#faf7f2; --panel:#fffdf9; --ink:#2b2622; --muted:#8a8178;
    --line:#ece4d8; --accent:#e8662a; --accent-soft:#fbe9df;
  }
  *{box-sizing:border-box}
  html,body{margin:0;padding:0}
  body{background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
    line-height:1.75;font-size:16px}
  header{position:sticky;top:0;z-index:20;background:rgba(250,247,242,.92);
    backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 22px;
    display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}
  .brand{font-weight:700;font-size:18px;letter-spacing:.2px}
  .brand small{display:block;font-weight:400;font-size:12px;color:var(--muted);margin-top:2px}
  .lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;background:var(--panel)}
  .lang button{border:0;background:transparent;color:var(--muted);padding:7px 14px;
    font-size:13px;cursor:pointer;font-weight:600;transition:.15s}
  .lang button.active{background:var(--accent);color:#fff}
  .wrap{display:flex;max-width:1180px;margin:0 auto;align-items:flex-start}
  nav{width:280px;flex:0 0 280px;position:sticky;top:67px;height:calc(100vh - 67px);
    overflow:auto;padding:22px 14px 40px;border-right:1px solid var(--line)}
  nav a{display:block;text-decoration:none;color:var(--ink);padding:11px 14px;border-radius:10px;
    margin-bottom:4px;border:1px solid transparent;transition:.15s}
  nav a:hover{background:var(--panel)}
  nav a.active{background:var(--accent-soft);border-color:#f3d3c2}
  nav a .n{font-size:12px;color:var(--accent);font-weight:700}
  nav a .t{display:block;font-weight:600;margin-top:2px}
  nav a .s{display:block;font-size:12px;color:var(--muted);margin-top:1px}
  main{flex:1;min-width:0;padding:34px clamp(18px,4vw,56px) 90px}
  article{max-width:760px}
  .meta{font-size:13px;color:var(--muted);margin-bottom:6px}
  .tag{display:inline-block;background:var(--accent-soft);color:var(--accent);
    border-radius:999px;padding:2px 10px;font-size:12px;font-weight:600;margin-bottom:18px}
  h1{font-size:30px;line-height:1.3;margin:.1em 0 .4em}
  h2{font-size:21px;margin:1.6em 0 .5em}
  h3{font-size:17px;margin:1.4em 0 .4em}
  p{margin:.7em 0}
  ul,ol{margin:.6em 0;padding-left:1.4em}
  li{margin:.3em 0}
  blockquote{margin:1em 0;padding:.4em 1em;border-left:3px solid var(--accent);
    background:var(--accent-soft);color:#5b4636;border-radius:0 8px 8px 0}
  blockquote p{margin:.2em 0}
  code{background:#f1ece3;padding:.1em .4em;border-radius:5px;font-size:.9em;
    font-family:"SFMono-Regular",Consolas,monospace}
  pre{background:#2b2622;color:#f3ece2;padding:14px 16px;border-radius:10px;overflow:auto}
  pre code{background:none;color:inherit;padding:0}
  hr{border:0;border-top:1px solid var(--line);margin:2em 0}
  strong{color:#1f1b18}
  .seg-label{font-size:12px;font-weight:700;color:var(--accent);text-transform:uppercase;
    letter-spacing:.08em;margin:1.8em 0 .2em}
  .seg-label:first-child{margin-top:0}
  footer{max-width:760px;margin:40px auto 0;padding:22px clamp(18px,4vw,56px);
    color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
  @media(max-width:780px){nav{display:none}main{padding-top:24px}}
</style>
</head>
<body>
<header>
  <div class="brand">🦞 Lobster Diaries
    <small>An AI lobster writes what it sees — in Chinese & English</small>
  </div>
  <div class="lang" id="lang">
    <button data-m="zh">中文</button>
    <button data-m="en" class="active">English</button>
    <button data-m="both">双语</button>
  </div>
</header>
<div class="wrap">
  <nav id="nav"></nav>
  <main><article id="doc"></article></main>
</div>
<footer>
  🦞 Lobster Diaries — public excerpt edition. New entries drip in over time.
  The full 30+ entries and the companion course are paid.
  Text © Yue. Code released under MIT.
</footer>
<script id="entries" type="application/json">__ENTRIES__</script>
<script>
const ENTRIES = JSON.parse(document.getElementById('entries').textContent);
let MODE = 'en';
let CUR = 0;

function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function inline(s){
  s = s.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>');
  s = s.replace(/`([^`]+?)`/g,'<code>$1</code>');
  return s;
}
function md(src){
  src = esc(src);
  src = src.replace(/```([\s\S]*?)```/g, (m,c)=>'<pre><code>'+c.replace(/^\n/,'')+'</code></pre>');
  const lines = src.split(/\n/);
  let html='', inUL=false, inOL=false, inQ=false;
  const close=()=>{if(inUL){html+='</ul>';inUL=false;}if(inOL){html+='</ol>';inOL=false;}if(inQ){html+='</blockquote>';inQ=false;}};
  for(let line of lines){
    if(/^\s*$/.test(line)){close();continue;}
    let h=line.match(/^(#{1,4})\s+(.*)$/);
    if(h){close();const l=h[1].length;html+='<h'+l+'>'+inline(h[2])+'</h'+l+'>';continue;}
    if(/^---+$/.test(line.trim())){close();html+='<hr>';continue;}
    if(/^>\s?/.test(line)){if(!inQ){close();html+='<blockquote>';inQ=true;}html+=inline(line.replace(/^>\s?/,''))+' ';continue;}
    let ul=line.match(/^\s*[-*]\s+(.*)$/);
    if(ul){if(!inUL){close();html+='<ul>';inUL=true;}if(inOL){html+='</ol>';inOL=false;}html+='<li>'+inline(ul[1])+'</li>';continue;}
    let ol=line.match(/^\s*\d+\.\s+(.*)$/);
    if(ol){if(!inOL){close();html+='<ol>';inOL=true;}if(inUL){html+='</ul>';inUL=false;}html+='<li>'+inline(ol[1])+'</li>';continue;}
    close();html+='<p>'+inline(line)+'</p>';
  }
  close();
  return html;
}
function titleOf(e){return MODE==='zh'?e.title_cn:e.title_en;}
function tagOf(e){return MODE==='zh'?e.tag_cn:e.tag_en;}

function renderNav(){
  const nav=document.getElementById('nav');
  nav.innerHTML = ENTRIES.map((e,i)=>{
    const sub = MODE==='zh' ? e.date : (e.tag_en||e.date);
    return `<a href="#" data-i="${i}" class="${i===CUR?'active':''}">
      <span class="n">#${e.no}</span>
      <span class="t">${titleOf(e)}</span>
      <span class="s">${sub}</span></a>`;
  }).join('');
  nav.querySelectorAll('a').forEach(a=>a.onclick=(ev)=>{ev.preventDefault();CUR=+a.dataset.i;renderAll();});
}
function renderDoc(){
  const e=ENTRIES[CUR];
  const doc=document.getElementById('doc');
  let meta = `<div class="meta">${e.date}</div>`;
  const tag = tagOf(e);
  let tagHtml = tag?`<div class="tag">${tag}</div>`:'';
  if(MODE==='zh' || MODE==='en'){
    const body = MODE==='zh'?e.cn:e.en;
    doc.innerHTML = meta + tagHtml + md(body);
  } else {
    doc.innerHTML = meta + tagHtml
      + `<div class="seg-label">中文</div>` + md(e.cn)
      + `<div class="seg-label">English</div>` + md(e.en);
  }
  doc.scrollTop=0; window.scrollTo(0,0);
}
function renderAll(){renderNav();renderDoc();}
document.getElementById('lang').querySelectorAll('button').forEach(b=>{
  b.onclick=()=>{
    MODE=b.dataset.m;
    document.querySelectorAll('#lang button').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    renderAll();
  };
});
renderAll();
</script>
</body>
</html>
"""

out = HTML.replace("__ENTRIES__", payload)
with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8") as f:
    f.write(out)
print("built index.html with", len(data), "bilingual entries")
