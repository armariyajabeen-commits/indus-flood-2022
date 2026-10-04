"""One-off patch that turns the first Pakistan page into the 'When the Indus rose' edition: new palette, new wording, extra interactivity."""
import pathlib, re, sys
p = pathlib.Path(__file__).resolve().parent.parent / "index.html"
s = p.read_text(encoding="utf8")


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c < 1:
        print("MISSING:", old[:80]); sys.exit(1)
    s = s.replace(old, new) if n == 0 else s.replace(old, new, n)


# ---------- palette
rep("""  --ground:#F4F5F1; --panel:#FCFCFB; --ink:#16201F; --muted:#5B6664; --rule:#DCE0DA;
  --a:#4A3AA7; --b:#EB6834; --focus:#2A78D6; --shadow:0 1px 2px rgba(20,30,30,.08),0 4px 14px rgba(20,30,30,.10);
  --obs:#2a78d6; --mod:#0f7b8a;""", """  --ground:#F5EFE4; --panel:#FFFBF3; --ink:#2A2118; --muted:#6B5F52; --rule:#E3D8C6;
  --a:#0E7C7B; --b:#C2185B; --focus:#3F51B5; --shadow:0 1px 2px rgba(60,40,10,.10),0 4px 14px rgba(60,40,10,.12);
  --obs:#3F51B5; --mod:#C97F00;""")
rep("""  --ground:#141817; --panel:#1B1F1E; --ink:#ECEFEC; --muted:#A3ADAA; --rule:#2F3634;
  --a:#9085E9; --b:#D95926; --focus:#86B6EF; --mod:#3fb6c4; --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.45);}}""",
    """  --ground:#17130F; --panel:#211B15; --ink:#F1E8DA; --muted:#B3A692; --rule:#3A3027;
  --a:#3FC1BF; --b:#F06292; --focus:#9FA8DA; --obs:#8C9EFF; --mod:#F2B134; --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.45);}}""")
rep("""  --ground:#141817; --panel:#1B1F1E; --ink:#ECEFEC; --muted:#A3ADAA; --rule:#2F3634;
  --a:#9085E9; --b:#D95926; --focus:#86B6EF; --mod:#3fb6c4; --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.45);}""",
    """  --ground:#17130F; --panel:#211B15; --ink:#F1E8DA; --muted:#B3A692; --rule:#3A3027;
  --a:#3FC1BF; --b:#F06292; --focus:#9FA8DA; --obs:#8C9EFF; --mod:#F2B134; --shadow:0 1px 2px rgba(0,0,0,.4),0 4px 14px rgba(0,0,0,.45);}""")
rep("--ground').toLowerCase()==='#141817'", "--ground').toLowerCase()==='#17130f'")
rep(".legend .sw.obs{background:rgba(42,120,214,.5);border:1px solid #1c5cab}", ".legend .sw.obs{background:rgba(63,81,181,.5);border:1px solid #2A3990}")
rep("repeating-linear-gradient(45deg,rgba(15,123,138,.55) 0 2px,transparent 2px 5px)", "repeating-linear-gradient(45deg,rgba(201,127,0,.65) 0 2px,transparent 2px 5px)")
rep("const OBSCOL='#2a78d6', MODCOL=DARK?'#3fb6c4':'#0f7b8a';", "const OBSCOL='#3F51B5', MODCOL=DARK?'#F2B134':'#C97F00';")
rep("const DEPCOLS=['#d9f0e3','#6bc3a0','#1c7a78','#0f3f4f'];", "const DEPCOLS=['#FCE8B2','#F4C261','#C97F00','#7A3E00'];")
rep("'line-color':'#1c5cab','line-width':.6", "'line-color':'#2A3990','line-width':.6")
s = s.replace("['#d9f0e3','#a5dcc0','#6bc3a0','#35a08a','#0f4f5f']", "['#FCEFC8','#F7D486','#E8AE3C','#C97F00','#7A3E00']")
rep("r:'Blues',zero:true,none:'No flood water in the tehsil'", "r:['#E8EAF6','#C5CAE9','#7986CB','#3F51B5','#1A237E'],zero:true,none:'Dry: no flood water here'")
rep("r:['#dbe9f6','#9ec5ea','#5c9fdc','#2a78d6','#14457f'],zero:true,none:'No flood water in the tehsil'", "r:['#E8EAF6','#C5CAE9','#7986CB','#3F51B5','#1A237E'],zero:true,none:'Dry: no flood water here'")
rep("r:'GnBu',zero:true,none:'No mapped building in the extent'", "r:'PuRd',zero:true,none:'No mapped building in the water'")
rep("'#d62728'", "'#D32F2F'", 0)
rep("'#f2c200'", "'#6D4C41'", 0)
rep("'circle-color':'#14457f'", "'circle-color':'#1A237E'")
rep("row('#14457f','Circle size grows", "row('#1A237E','Circle size grows")
rep("row('#D32F2F','Flooded in 2022, inside the '+T+'-yr scenario');row('#6D4C41','Flooded in 2022, outside the scenario');", "row('#D32F2F','Flooded in 2022 and inside the '+T+'-year scenario');row('#6D4C41','Flooded in 2022 but outside the scenario');")
rep("<title>Who lived in the flood path, Pakistan 2022</title>", "<title>When the Indus rose: Pakistan, 2022</title>")
rep("fill='%231b3a5c'/%3E%3Cpath d='M4 20q4-5 8 0t8 0 8 0v8H4z' fill='%232a78d6'", "fill='%232A2118'/%3E%3Cpath d='M4 20q4-5 8 0t8 0 8 0v8H4z' fill='%23C97F00'")
rep('<meta name="theme-color" content="#1b3a5c">', '<meta name="theme-color" content="#2A2118">')

# ---------- wording: bar and layers
rep("<label>Show on map<select", "<label>Colour the map by<select")
rep("<label>Province<select", "<label>Region<select")
rep('<a class="btn" href="analysis/">Evidence &amp; method →</a>', '<a class="btn" href="analysis/">How we know →</a>')
rep("Observed (2022 monsoon)", "What satellites saw, 2022")
rep("Flood water extent, observed", "Floodwater seen from space")
rep("Flooded buildings (OSM) <span", "Buildings under water (OSM) <span")
rep("Modelled scenarios, not observed", "What models say, not 2022", 0)
rep("Flooded area, scenario <span", "Scenario floodplain <span")
rep("Water depth classes, scenario", "Scenario depth bands")
rep(">Return period <select", ">Flood odds <select")
rep('<option value="10">10 yr</option><option value="100" selected>100 yr</option><option value="500">500 yr</option>', '<option value="10">1-in-10-yr</option><option value="100" selected>1-in-100-yr</option><option value="500">1-in-500-yr</option>')
rep(">Exposure data<", ">People and buildings<")
rep("2 km cells, exposed people <span", "People per 2 km cell <span")
rep("Tehsil boundaries", "Tehsil lines")
rep("Province boundaries", "Region lines")
rep(">Context<", ">Backdrop<")
rep("Terrain relief", "Shaded terrain")
rep("Clear areas</button>", "Clear circles</button>")
rep("Click the map to place area A, then area B. Drag either pin to move it.", "Tap the map to drop circle A, then circle B. Drag a pin to move it.", 0)
rep("Two example areas are placed. Drag the pins, or click to move the nearer one.", "Two circles are already placed. Drag a pin, or tap to move the nearer one.")
rep("Now click to place area B.", "Now tap to drop circle B.")
rep(">Radius <input", ">Circle size <input")

# ---------- wording: side panel
rep("<h1>Who lived in the flood path</h1>", "<h1>When the Indus rose</h1>")
rep("<span>Area A</span><strong id=\"popA\">–</strong><span id=\"subA\">Click the map</span>", "<span>Circle A</span><strong id=\"popA\">–</strong><span id=\"subA\">Tap the map</span>")
rep("<span>Area B</span><strong id=\"popB\">–</strong><span id=\"subB\">then click again</span>", "<span>Circle B</span><strong id=\"popB\">–</strong><span id=\"subB\">then tap again</span>")
rep("<h2>Age profile, share of residents</h2>", "<h2>Who is inside the circles: ages</h2>")
rep("<span><i style=\"background:var(--a)\"></i>Area A</span><span><i style=\"border:2px solid var(--b);height:9px\"></i>Area B</span>", "<span><i style=\"background:var(--a)\"></i>Circle A</span><span><i style=\"border:2px solid var(--b);height:9px\"></i>Circle B</span>")
rep("Five age groups from the 2017 census tables at tehsil level (the smallest area with age data), weighted by the people each circle counts in each tehsil. This is a tehsil-level proxy (an ecological estimate) and the census is from 2017, five years before the flood.", "Five age bands taken from the 2017 census at tehsil level, the smallest area with public age data, and blended by how many people the circle holds in each tehsil. Treat it as an area average, not a head count, and remember it predates the flood by five years.")
rep("On the map, each tehsil a circle touches is shaded in that circle's colour. The darker the shade, the larger the share of its 2 km cells whose centre lies inside the circle.", "Tehsils a circle touches are tinted in its colour: the deeper the tint, the more of that tehsil's 2 km cells sit inside the circle.")
rep("<h2>Exposure and profile</h2>", "<h2>The numbers inside each circle</h2>")
rep("<b>Observed.</b> The blue extent is satellite-detected flood water for 1 July to 31 August 2022 (UNOSAT, VIIRS sensor, about 375 m pixels). It is preliminary and not validated in the field, and optical detection can miss water under cloud, trees or in dense settlements. \"Exposed\" means inside that extent.", "<b>Seen from space.</b> The indigo layer is floodwater detected by satellite between 1 July and 31 August 2022 (UNOSAT, VIIRS, pixels of about 375 m). It is a first pass that nobody has checked on the ground, and cloud, tree cover or dense housing can hide water. \"In the water\" below simply means inside this layer.")
rep("<b>Modelled.</b> The hatched teal layers and the depth classes are river-flood design scenarios (10, 100, 500-year return periods) from a global model. They are not a record of 2022 and the rows in teal are listed apart from the observed rows.", "<b>Computed, not observed.</b> The amber hatched layers and depth bands come from a global river-flood model run for 1-in-10, 1-in-100 and 1-in-500-year floods. They show what such a flood could do, not what 2022 did, and they sit in their own amber rows below.")
rep("<b>Data quality.</b> People per cell are WorldPop's modelled estimate for 2020, not a count. OpenStreetMap is incomplete in Pakistan, so building counts are lower bounds and method C falls back to the cell centre where a cell has no mapped building.", "<b>Handle with care.</b> People per cell are WorldPop's 2020 estimate, not a count. OpenStreetMap barely covers rural Pakistan, so building counts are minimums, and the building method falls back to the cell centre wherever no building is mapped.")
rep("<h2>Where the numbers come from</h2>", "<h2>Behind the numbers</h2>")
rep("<p>Observed extent: UNOSAT (HDX), CC BY-SA. Population:", "<p>Floodwater: UNOSAT (HDX), CC BY-SA. Population:")
rep("Circle figures count 2 km cells (summed from the 100 m grid) whose centre is inside the circle. Exposed people (A) weights each 100 m cell by the share of it inside the extent; (B) counts cells whose centre is inside; (C) allocates a cell's people to its flooded buildings where OSM has mapped buildings, else counts the cell if its centre is inside.", "A circle adds up every 2 km cell (built from the 100 m grid) whose centre falls inside it. Method A scales each 100 m cell by how much of it is under water; B counts a cell whole if its centre is wet; C shares a cell's people among its flooded mapped buildings, and uses B where none are mapped.")
rep("Details and limits: <a href=\"analysis/\">Evidence &amp; method</a>.", "Full detail and limits: <a href=\"analysis/\">How we know</a>.")
rep("Pakistan, monsoon floods of 2022. ${fv('n_study')} of ${fv('n_tehsil')} tehsils touch the observed flood water, covering about ${fv('extent_km2').toLocaleString()} km². Compare any two places instead of one average, and see the observed flood next to the modelled scenarios, which are kept apart.", "In the monsoon of 2022, satellites saw floodwater over about ${fv('extent_km2').toLocaleString()} km² of Pakistan, touching ${fv('n_study')} of ${fv('n_tehsil')} tehsils. Drop two circles anywhere and compare who lives inside them, or switch on the computed flood scenarios to see how far they agree with what was seen.")
rep("['Raw data','Study area','Buildings (OSM)','Modelled hazard','Terrain','Grid exposure','Tehsil dataset','Models','Map and summary']", "['Downloads','Study area','OSM buildings','Flood model','Terrain','People on the grid','Tehsil table','Statistics','This site']")

# ---------- wording: metrics and table rows
rep("l:'Share of tehsil people in the flood extent'", "l:'Share of a tehsil's people in the water'".replace("'s", "\\'s"))
rep("unit:'area-weighted (A), WorldPop people'", "unit:'method A, WorldPop people'")
rep("l:'People in the flood extent'", "l:'People in the water'")
rep("l:'OSM buildings in the flood extent'", "l:'Mapped buildings in the water'")
rep("unit:'lower bound: OSM is incomplete'", "unit:'a minimum: OSM is patchy'")
rep("'Modelled scenario, not observed',k:'sh100'", "'What models say, not 2022',k:'sh100'")
rep("'Modelled scenario, not observed',k:'sh10'", "'What models say, not 2022',k:'sh10'")
rep("'Modelled scenario, not observed',k:'sh500'", "'What models say, not 2022',k:'sh500'")
rep("l:'Share of people in the 100-year scenario area'", "l:'People on the 1-in-100-year floodplain'")
rep("l:'Share of people in the 10-year scenario area'", "l:'People on the 1-in-10-year floodplain'")
rep("l:'Share of people in the 500-year scenario area'", "l:'People on the 1-in-500-year floodplain'")
rep("'Exposure to the observed 2022 flood'", "'Hit by the 2022 flood'", 0)
rep("'People (census 2017)'", "'Who lives there (census 2017)'", 0)
rep("{g:'Data quality',k:'bper',l:'OSM buildings per 1,000 people'", "{g:'Data gaps',k:'bper',l:'Mapped buildings per 1,000 people'")
rep("unit:'completeness check, not a vulnerability measure'", "unit:'shows how thin OSM is, not vulnerability'")
rep("['sec','Observed flood, 2022']", "['sec','Seen from space, 2022']")
rep("['People in the extent (A)',o=>o.popA,'n','Area-weighted: share of each 100 m cell inside the extent']", "['In the water (method A)',o=>o.popA,'n','Each 100 m cell scaled by how much of it is wet']")
rep("['People in the extent (B)',o=>o.popB,'n','Cells whose centre is inside the extent']", "['In the water (method B)',o=>o.popB,'n','Whole cell counted if its centre is wet']")
rep("['People in the extent (C)',o=>o.popC,'n','Allocated to flooded OSM buildings where mapped, else as (B)']", "['In the water (method C)',o=>o.popC,'n','Shared among flooded mapped buildings, else as B']")
rep("['Share of people in the extent (A)',o=>pct(o.popA,o.pop),'p']", "['Share of people in the water',o=>pct(o.popA,o.pop),'p']")
rep("['OSM residential-like buildings',o=>o.nb,'n','Lower bound: OSM is incomplete']", "['Mapped homes (OSM)',o=>o.nb,'n','A minimum: OSM is patchy here']")
rep("['…of them inside the extent',o=>o.nbf,'n']", "['…of them in the water',o=>o.nbf,'n']")
rep("['sec','Tehsil profile (census 2017, proxy)']", "['sec','Who lives there (2017 census, tehsil average)']")
rep("['People in the 10-year scenario area',", "['On the 1-in-10-year floodplain',")
rep("['People in the 100-year scenario area',", "['On the 1-in-100-year floodplain',")
rep("['People in the 500-year scenario area',", "['On the 1-in-500-year floodplain',")
rep("'JRC river-flood scenario','mod'", "'JRC river-flood model','mod'")
rep("'<strong>${b.name}</strong> · ${b.dist}, ${b.prov}", "'<strong>${b.name}</strong> · ${b.dist}, ${b.prov}") if False else None
rep("people in the observed extent (${(b.shA*100).toFixed(1)}%)", "people in the water (${(b.shA*100).toFixed(1)}%)")
rep("Counted in ${n}: ${share(w,i)} of its 2 km cells", "Inside circle ${n}: ${share(w,i)} of its 2 km cells")
rep("'people, near '+near(A):'Click the map'", "'people, near '+near(A):'Tap the map'")
rep("(oa?'Click to place':'then click again')", "(oa?'Tap to place':'then tap again')")
rep("if(areas.length===1)h.textContent", "if(areas.length===1)h.textContent")
rep("'Observed, 2022 monsoon';row(null,'Flood water extent (UNOSAT, VIIRS, preliminary)','obs')", "'Seen from space, 2022';row(null,'Floodwater (UNOSAT, VIIRS, unchecked)','obs')") if False else None
rep("sec('obs','Observed, 2022 monsoon');row(null,'Flood water extent (UNOSAT, VIIRS, preliminary)','obs');", "sec('obs','Seen from space, 2022');row(null,'Floodwater (UNOSAT, VIIRS, unchecked on the ground)','obs');")
rep("sec('mod','Modelled scenario, not observed');if($('ror').checked)row(null,'Flooded area, river-flood scenario, '+T+'-year','mod');", "sec('mod','What a model says, not 2022');if($('ror').checked)row(null,'Floodplain of a 1-in-'+T+'-year river flood','mod');")
rep("if($('dep').checked){DEPCOLS.forEach((c,i)=>row(c,'Depth '+DEPLAB[i]));}", "if($('dep').checked){DEPCOLS.forEach((c,i)=>row(c,'Water '+DEPLAB[i]+' deep'));}")
rep("sec('','Buildings (OSM, lower bound)');", "sec('','Buildings under water (OSM, a minimum)');")
rep("else row('#D32F2F','Residential-like building in the extent');", "else row('#D32F2F','Home-like building in the water');")
rep("'Points, drawn only for buildings inside the observed extent'", "'One dot per building, only where satellites saw water'")
rep("sec('','2 km cells');row", "sec('','People per 2 km cell');row")
rep("Circle size grows with zoom; darker = more people in the extent", "Darker dot = more people in the water")

p.write_text(s, encoding="utf8")
print("patched OK")
