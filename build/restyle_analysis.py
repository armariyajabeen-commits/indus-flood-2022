"""Patch for the analysis page: new palette, title and wording ('How we know')."""
import pathlib, sys
p = pathlib.Path(__file__).resolve().parent.parent / "analysis/index.html"
s = p.read_text(encoding="utf8")


def rep(old, new, all_=False):
    global s
    if s.count(old) < 1:
        print("MISSING:", old[:90]); sys.exit(1)
    s = s.replace(old, new) if all_ else s.replace(old, new, 1)


rep(":root{--ground:#F4F5F1;--panel:#FCFCFB;--ink:#16201F;--muted:#5B6664;--rule:#DCE0DA;--grid:#E9ECE7;--focus:#2A78D6;--ns:#D9DCD6;--a:#4A3AA7;--b:#EB6834;--obs:#2a78d6;--mod:#0f7b8a}",
    ":root{--ground:#F5EFE4;--panel:#FFFBF3;--ink:#2A2118;--muted:#6B5F52;--rule:#E3D8C6;--grid:#EDE3D2;--focus:#3F51B5;--ns:#E3D8C6;--a:#0E7C7B;--b:#C2185B;--obs:#3F51B5;--mod:#C97F00}")
rep("@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){--ground:#141817;--panel:#1B1F1E;--ink:#ECEFEC;--muted:#A3ADAA;--rule:#2F3634;--grid:#252B29;--focus:#86B6EF;--ns:#3A403E;--a:#9085E9;--b:#D95926;--mod:#3fb6c4}}",
    "@media (prefers-color-scheme:dark){:root:not([data-theme=\"light\"]){--ground:#17130F;--panel:#211B15;--ink:#F1E8DA;--muted:#B3A692;--rule:#3A3027;--grid:#2A231B;--focus:#9FA8DA;--ns:#3A3027;--a:#3FC1BF;--b:#F06292;--obs:#8C9EFF;--mod:#F2B134}}")
rep(":root[data-theme=\"dark\"]{--ground:#141817;--panel:#1B1F1E;--ink:#ECEFEC;--muted:#A3ADAA;--rule:#2F3634;--grid:#252B29;--focus:#86B6EF;--ns:#3A403E;--a:#9085E9;--b:#D95926;--mod:#3fb6c4}",
    ":root[data-theme=\"dark\"]{--ground:#17130F;--panel:#211B15;--ink:#F1E8DA;--muted:#B3A692;--rule:#3A3027;--grid:#2A231B;--focus:#9FA8DA;--ns:#3A3027;--a:#3FC1BF;--b:#F06292;--obs:#8C9EFF;--mod:#F2B134}")
rep("toLowerCase()==='#141817'", "toLowerCase()==='#17130f'")
rep("#1c5cab", "#2A3990", True)
rep("rgba(42,120,214,.5)", "rgba(63,81,181,.5)", True)
rep("#d62728", "#D32F2F", True)
rep("#f2c200", "#6D4C41", True)
rep("fill='%231b3a5c'/%3E%3Cpath d='M4 20q4-5 8 0t8 0 8 0v8H4z' fill='%232a78d6'", "fill='%232A2118'/%3E%3Cpath d='M4 20q4-5 8 0t8 0 8 0v8H4z' fill='%23C97F00'")
rep('<meta name="theme-color" content="#1b3a5c">', '<meta name="theme-color" content="#2A2118">')
rep("<title>Evidence and method, Pakistan 2022</title>", "<title>How we know: the Pakistan 2022 floods</title>")
rep("<h1>Evidence and method</h1>", "<h1>How we know</h1>")
rep("← Back to the map", "← Back to the map")
rep("Pakistan, monsoon floods of 2022. How ${f('n_study')} tehsils, a modelled population of ${f('wp_total').toLocaleString()}, ${f('osm_total').toLocaleString()} mapped buildings and two kinds of flood evidence were joined, what each step costs in accuracy, and where the method stops.",
    "The 2022 monsoon floods, step by step: how ${f('n_study')} tehsils, a modelled population of ${f('wp_total').toLocaleString()}, ${f('osm_total').toLocaleString()} mapped buildings and two different kinds of flood evidence were put together, what each step costs in accuracy, and where the method runs out.")
rep("<h2>Headline numbers, all from the project run</h2>", "<h2>The short version</h2>")
rep("Every figure on this page is read from <code>data/facts.json</code>, which was parsed from the run log and the output tables. The file named under each section shows where a number comes from.", "Nothing on this page is typed in by hand: each figure is read from <code>data/facts.json</code>, which was extracted from the run log and the output tables. The grey note under each block names its source file.")
rep("<h2>Observed flood versus modelled scenarios</h2>", "<h2>What satellites saw, and what a model computes</h2>")
rep("The two are different kinds of evidence and are never mixed. <b>Observed</b>: satellite-detected flood water for 1 July to 31 August 2022 (UNOSAT, VIIRS sensor, about 375 m pixels, preliminary). <b>Modelled</b>: river-flood design scenarios for 10, 100 and 500-year return periods (Copernicus GloFAS global hazard maps), which describe a flood of a given probability, not what happened in 2022.",
    "These are two kinds of evidence and the site keeps them apart. <b>Seen from space</b>: floodwater detected by satellite between 1 July and 31 August 2022 (UNOSAT, VIIRS, pixels of about 375 m, not checked on the ground). <b>Computed</b>: river floods of a chosen likelihood, once in 10, 100 or 500 years, from the Copernicus GloFAS global model. The model describes a flood of a given odds, not the one that happened.")
rep("Solid blue is observed; hatched teal is modelled.", "Solid indigo is what satellites saw; amber hatching is what the model computes.")
rep("observed extent</span>", "satellite water</span>")
rep("modelled scenario</span>", "model floodplain</span>")
rep("flooded building, caught by the scenario", "wet building the model also floods")
rep("flooded in 2022 but outside the scenario", "wet building the model misses")
rep("other residential-like building", "other home-like building")
rep("<h3>How much of the observed flood does each scenario reproduce?</h3>", "<h3>How well does each model flood match the satellite picture?</h3>")
rep("<h2>Provenance chain: raw data to the figures on the map</h2>", "<h2>From download to map: the nine steps</h2>")
rep("Nine scripted steps, in this order (<code>pk_verification/scripts</code>). Steps in teal handle the modelled hazard.", "Each step is a script in <code>pk_verification/scripts</code>, run in this order. Amber outlines mark the steps that deal with the flood model.")
rep("<h2>Three ways to count exposed people</h2>", "<h2>Three ways to count people in the water</h2>")
rep("<h2>How far the inputs can be trusted</h2>", "<h2>How much to trust each input</h2>")
rep("<h2>Is a regression on this sample defensible?</h2>", "<h2>Can a regression explain who was exposed?</h2>")
rep("<h2>What could not be obtained</h2>", "<h2>What we looked for and could not get</h2>")
rep("<h2>Limits you should know before using a number</h2>", "<h2>Before you quote a number</h2>")
rep("<h2>Data sources</h2>", "<h2>Where the data came from</h2>")
rep("<h3>Reproducibility frictions</h3>", "<h3>Things that make a re-run awkward</h3>")
rep("Hidden", "Hidden") if False else None
p.write_text(s, encoding="utf8")
print("analysis patched OK")
