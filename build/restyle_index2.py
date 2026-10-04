"""Second patch: extra interactivity (search, hotspot chips, tehsil spotlight, inspect mode, scenario strength, blink compare)."""
import pathlib, sys
p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf8")


def rep(old, new):
    global s
    if s.count(old) < 1:
        print("MISSING:", old[:90]); sys.exit(1)
    s = s.replace(old, new, 1)


# ---- CSS
rep(".maplibregl-ctrl-attrib{font-size:10.5px}", """.maplibregl-ctrl-attrib{font-size:10.5px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 4px}
.chips button,.pill{font:inherit;font-size:12px;color:var(--ink);background:var(--ground);border:1px solid var(--rule);border-radius:999px;padding:4px 10px;cursor:pointer;transition:background .15s,transform .1s}
.chips button:hover,.pill:hover{background:color-mix(in srgb,var(--obs) 14%,var(--ground))}
.chips button:active,.pill:active{transform:scale(.96)}
.chips button small{color:var(--muted);margin-left:4px}
.chips button.on{border-color:var(--obs);background:color-mix(in srgb,var(--obs) 16%,var(--ground))}
.spot{border:1px solid var(--rule);border-radius:12px;padding:12px 14px;background:var(--ground);margin-top:8px}
.spot h3{margin:0;font-size:15px}
.spot .where{color:var(--muted);font-size:12px;margin:0 0 8px}
.spot .big{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:8px}
.spot .big div{min-width:90px}
.spot .big strong{display:block;font-size:20px;line-height:1.1}
.spot .big span{font-size:11.5px;color:var(--muted)}
.bar2{height:10px;border-radius:5px;background:var(--rule);position:relative;overflow:hidden;margin:2px 0 8px}
.bar2 i{position:absolute;left:0;top:0;bottom:0;background:var(--obs);border-radius:5px;transition:width .35s}
.bar2 i.m{background:var(--mod)}
.spot dl{display:grid;grid-template-columns:1fr auto;gap:2px 10px;font-size:12.5px;margin:0}
.spot dt{color:var(--muted)} .spot dd{margin:0;text-align:right;font-weight:600}
.spot .rank{font-size:12px;color:var(--muted);margin:6px 0 0}
.ctrl select.mode{width:100%}
@keyframes pop{from{transform:scale(.97);opacity:.4}to{transform:none;opacity:1}}
.spot.anim{animation:pop .25s ease-out}""")

# ---- bar: search
rep("""      <span class="sp"></span>
      <a class="btn" href="analysis/">""", """      <label>Find a tehsil<input id="find" list="tlist" placeholder="Type a name" autocomplete="off" aria-label="Search for a tehsil"></label><datalist id="tlist"></datalist>
      <span class="sp"></span>
      <a class="btn" href="analysis/">""")

# ---- ctrl: mode, strength, blink
rep("""        <label class="keep">Circle size <input type="range" id="rad" min="4" max="40" step="1" value="15"> <span id="radv">15 km</span></label>""",
    """        <label class="keep">Circle size <input type="range" id="rad" min="4" max="40" step="1" value="15"> <span id="radv">15 km</span></label>
        <label class="keep">Tapping the map <select id="mode" class="mode" aria-label="What a tap on the map does"><option value="pin">moves a circle</option><option value="look">opens a tehsil</option></select></label>""")
rep("""        <label><input type="checkbox" id="dep"> Scenario depth bands""", """        <label class="keep">Strength <input type="range" id="mop" min="15" max="100" value="90" aria-label="Opacity of the scenario layers"></label>
        <button id="blink" type="button" title="Flash the scenario on and off over the satellite water to compare them">Blink: seen vs computed</button>
        <label><input type="checkbox" id="dep"> Scenario depth bands""")

# ---- aside: chips + spotlight
rep("""    <h2>Who is inside the circles: ages</h2>""", """    <h2>Jump to a hotspot</h2>
    <div class="chips" id="chips" aria-label="Most flooded tehsils"></div>
    <div class="spot" id="spot"><p class="where" style="margin:0">Tap a hotspot above, search for a tehsil, or set “Tapping the map” to “opens a tehsil” and tap any area to see its profile here.</p></div>
    <h2>Who is inside the circles: ages</h2>""")

# ---- JS: spotlight, chips, search, mode, strength, blink
rep("const loaded={},busy={};", r"""let selIdx=null;
const spotEl=document.getElementById('spot');
function spotlight(i,fly){
  const b=B[i];selIdx=i;
  if(map.getLayer('sel-line'))map.setFilter('sel-line',['==',['get','code'],b.code]);
  if(fly){const bb=d3.geoBounds(BU.features[i]);map.fitBounds(bb,{padding:70,maxZoom:9,duration:900});}
  const st=B.filter(x=>x.st&&x.shA!=null),rank=1+st.filter(x=>x.shA>b.shA).length;
  const prov=st.filter(x=>x.prov===b.prov),pm=d3.median(prov,x=>x.shA);
  const pc=v=>v==null||!isFinite(v)?'–':(v*100).toFixed(1)+'%';
  spotEl.classList.remove('anim');void spotEl.offsetWidth;spotEl.classList.add('anim');
  spotEl.innerHTML=`<h3>${b.name}</h3><p class="where">${b.dist} district · ${b.prov}</p>
   <div class="big"><div><strong>${b.pop?N0(b.pop):'–'}</strong><span>people, census 2017</span></div><div><strong>${b.st?N0(b.popA):'0'}</strong><span>in the water (method A)</span></div><div><strong>${b.st?pc(b.shA):'–'}</strong><span>of the tehsil</span></div></div>
   <div class="bar2" title="share in the water"><i style="width:${Math.min(100,(b.shA||0)*100)}%"></i></div>
   <dl><dt>On the 1-in-10-year floodplain</dt><dd>${pc(b.sh10)}</dd><dt>On the 1-in-100-year floodplain</dt><dd>${pc(b.sh100)}</dd><dt>On the 1-in-500-year floodplain</dt><dd>${pc(b.sh500)}</dd>
   <dt>Aged 65+</dt><dd>${b.p65!=null?b.p65.toFixed(1)+'%':'–'}</dd><dt>Aged 0–14</dt><dd>${b.p014!=null?b.p014.toFixed(1)+'%':'–'}</dd><dt>Household size</dt><dd>${b.hhs!=null?b.hhs.toFixed(1):'–'}</dd>
   <dt>Mean elevation</dt><dd>${b.elev!=null?Math.round(b.elev)+' m':'–'}</dd><dt>Mapped buildings per 1,000 people</dt><dd>${b.bper!=null?b.bper.toFixed(1):'–'}</dd></dl>
   <p class="rank">${b.st&&b.shA>0?`Ranks ${rank} of ${st.length} flooded tehsils by share in the water; the median in ${b.prov} is ${pc(pm)}.`:'No floodwater was detected in this tehsil.'}</p>`;
  document.querySelectorAll('#chips button').forEach(x=>x.classList.toggle('on',+x.dataset.i===i));
}
{ // hotspot chips: the tehsils with the most people in the water
  const top=B.map((b,i)=>[b.popA||0,i]).sort((p,q)=>q[0]-p[0]).slice(0,8);
  d3.select('#chips').selectAll('button').data(top).join('button').attr('type','button').attr('data-i',d=>d[1]).html(d=>`${B[d[1]].name}<small>${d[0]>=1e6?(d[0]/1e6).toFixed(1)+' M':Math.round(d[0]/1000)+' k'}</small>`).on('click',(e,d)=>{
    const i=d[1],c=centroid(BU.features[i]);spotlight(i,true);
    const a=areas.find(x=>x.id==='a');if(a){a.lon=c[0];a.lat=c[1];a.marker.setLngLat(c);drawRings();update();}});
  d3.select('#tlist').selectAll('option').data(B.map((b,i)=>[b,i]).sort((p,q)=>d3.ascending(p[0].name,q[0].name))).join('option').attr('value',d=>`${d[0].name} (${d[0].dist})`);
  $('find').addEventListener('change',e=>{const v=e.target.value.trim().toLowerCase();
    let k=B.findIndex(b=>`${b.name} (${b.dist})`.toLowerCase()===v);if(k<0)k=B.findIndex(b=>b.name.toLowerCase()===v);
    if(k>=0&&map){spotlight(k,true);e.target.blur();}});
}
const loaded={},busy={};""")

# map click: inspect mode
rep("  map.on('click',e=>{\n    if(Date.now()-lastDrag<300)return;", "  map.on('click',e=>{\n    if(Date.now()-lastDrag<300)return;\n    if($('mode').value==='look'){const f=map.queryRenderedFeatures(e.point,{layers:['bu-fill']})[0];if(f)spotlight(f.id,false);return;}")
# strength + blink
rep("  $('rad').addEventListener('input',", """  const setStrength=()=>{const v=+$('mop').value/100;['ror-fill'].forEach(id=>map.setPaintProperty(id,'fill-opacity',Math.min(1,v)));map.setPaintProperty('dep-fill','fill-opacity',v*.8);map.setPaintProperty('ror-line','line-opacity',v);};
  $('mop').addEventListener('input',setStrength);
  let blinking=false;
  $('blink').addEventListener('click',async()=>{
    if(blinking)return;blinking=true;const was=$('ror').checked;
    if(!was){$('ror').checked=true;$('ror').dispatchEvent(new Event('change'));await new Promise(r=>setTimeout(r,1200));}
    for(let k=0;k<6;k++){const on=k%2===1;vis(['ror-fill','ror-line'],on);await new Promise(r=>setTimeout(r,650));}
    vis(['ror-fill','ror-line'],true);blinking=false;});
  $('rad').addEventListener('input',""")
p.write_text(s, encoding="utf8")
print("patched 2 OK")
