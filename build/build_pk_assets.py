"""Derived WEB assets for the Pakistan research site. Reads the run outputs in ../../pk_verification and writes browser-sized files to ../data.
Nothing here changes research data or calculations; simplification is for DISPLAY only and is stated on the site.
    python build_pk_assets.py A     # tehsils, provinces, observed extent, 2 km cells, flooded-building points, relief, facts
    python build_pk_assets.py B     # analysis window around the most exposed tehsil
(the modelled JRC layers are written by pk_verification/scripts/08_web_hazard_layers.py)"""
import sys, json, re, math, pathlib, shutil
import numpy as np, pandas as pd, geopandas as gpd, shapely
from shapely.geometry import mapping, box
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent; PROJ = SITE.parent / "pk_verification"
PROC, OUT, LOG, RAW = PROJ / "data/processed", PROJ / "outputs", PROJ / "logs", PROJ / "data/raw"
DATA = SITE / "data"; DATA.mkdir(exist_ok=True)
AEA = "+proj=aea +lat_1=12.472955 +lat_2=35.172805 +lat_0=24 +lon_0=85 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"


def say(m): print(m, flush=True)
def rnd(o, nd=4):
    return [rnd(x, nd) for x in o] if isinstance(o, (list, tuple)) else round(o, nd)
def clean(v):
    if isinstance(v, (np.floating, float)): return None if (math.isnan(v) or math.isinf(v)) else float(v)
    if isinstance(v, np.integer): return int(v)
    return v
def fc(gdf, props, nd=4):
    g = gdf.to_crs(4326); feats = []
    for i, (geom, row) in enumerate(zip(g.geometry, gdf.drop(columns="geometry").to_dict("records"))):
        if geom is None or geom.is_empty: continue
        m = mapping(geom)
        feats.append({"type": "Feature", "id": i, "properties": {k: clean(row[k]) for k in props}, "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"], nd)}})
    return {"type": "FeatureCollection", "features": feats}
def write(name, obj):
    f = DATA / name; f.write_text(json.dumps(obj, separators=(",", ":"), allow_nan=False), encoding="utf8"); say(f"  {name}: {f.stat().st_size/1e6:.2f} MB")


def parse_logs():
    txt = (PROJ / "logs/run.log").read_text(encoding="utf8")
    F = {}
    def grab(key, rx, cast=float, src="logs/run.log"):
        m = re.findall(rx, txt)
        if not m:
            say(f"   !! fact not found: {key}"); return
        F[key] = {"v": cast(m[-1].replace(",", "")), "src": src}
    I = int
    grab("osm_total", r"OSM buildings read: ([\d,]+)", I, "logs/run.log (02_buildings)")
    grab("osm_res_pct", r"residential-likely [\d,]+ \(([\d.]+)%\)", float, "logs/run.log (02_buildings)")
    grab("osm_in_extent", r"in the observed extent: ([\d,]+) \(", I, "logs/run.log (02_buildings)")
    grab("osm_res_in_extent", r"in the observed extent: [\d,]+ \(([\d,]+) residential", I, "logs/run.log (02_buildings)")
    grab("extent_km2", r"extent area \(equal-area CRS\): ([\d,]+) km2", I, "logs/run.log (01_flood_and_study_area)")
    grab("n_tehsil", r"tehsil polygons (\d+);", I, "logs/run.log (01)")
    grab("n_study", r"tehsils intersecting the observed extent: (\d+) of", I, "logs/run.log (01)")
    grab("n_ge50", r">=50%: (\d+)", I, "logs/run.log (01)")
    grab("study_pop_census", r"study population \(2017 census, tehsils in study\): ([\d,]+)", I, "logs/run.log (01)")
    grab("wp_total", r"WorldPop total \(Pakistan raster\) ([\d,]+);", I, "logs/run.log (06_grid_exposure)")
    grab("exp_A", r"; exposed A ([\d,]+);", I, "logs/run.log (06_grid_exposure)")
    grab("exp_B", r"exposed A [\d,]+; B ([\d,]+); C", I, "logs/run.log (06_grid_exposure)")
    grab("exp_C", r"; C ([\d,]+) \(of which", I, "logs/run.log (06_grid_exposure)")
    grab("exp_fallback", r"fallback-to-centre ([\d,]+)\)", I, "logs/run.log (06_grid_exposure)")
    grab("mod_rp10", r"modelled exposed RP10 ([\d,]+),", I, "logs/run.log (06_grid_exposure)")
    grab("mod_rp100", r"exposed RP10 [\d,]+, RP100 ([\d,]+), RP500", I, "logs/run.log (06_grid_exposure)")
    grab("mod_rp500", r"exposed RP10 [\d,]+, RP100 [\d,]+, RP500 ([\d,]+)", I, "logs/run.log (06_grid_exposure)")
    grab("wp_over_census", r"= ([\d.]+); tehsil-level corr", float, "logs/run.log (07)")
    grab("wp_census_corr", r"tehsil-level corr \(log\) ([\d.]+)", float, "logs/run.log (07)")
    grab("osm_per1000_nat", r"national ([\d.]+); study tehsils median", float, "logs/run.log (07)")
    grab("osm_per1000_med", r"study tehsils median ([\d.]+); tehsils with zero", float, "logs/run.log (07)")
    grab("osm_zero_tehsils", r"tehsils with zero OSM buildings (\d+)", I, "logs/run.log (07)")
    grab("fallback_share", r"fallback in method C\): ([\d.]+)%", float, "logs/run.log (07)")
    grab("top5", r"hold ([\d.]+)% / ", float, "logs/run.log (07)")
    grab("top10share", r"% / ([\d.]+)% / [\d.]+% of A-exposed", float, "logs/run.log (07)")
    grab("zero_A", r"zero exposure \(A\): (\d+)", I, "logs/run.log (07)")
    grab("resp_zero", r"zeros (\d+) \(", I, "logs/run.log (07)")
    grab("resp_zero_pct", r"zeros \d+ \(([\d.]+)%\)", float, "logs/run.log (07)")
    grab("resp_skew", r"skew (-?[\d.]+), kurtosis", float, "logs/run.log (07)")
    grab("resp_kurt", r"kurtosis (-?[\d.]+)", float, "logs/run.log (07)")
    grab("n_complete", r"complete cases (\d+) of", I, "logs/run.log (07)")
    grab("ols_r2", r"OLS R2 ([\d.]+) adjR2", float, "logs/run.log (07)")
    grab("ols_adjr2", r"OLS R2 [\d.]+ adjR2 (-?[\d.]+)", float, "logs/run.log (07)")
    grab("fraclogit_dev", r"deviance share explained (-?[\d.]+)", float, "logs/run.log (07)")
    grab("logit_pseudo_r2", r"pseudo R2 (-?[\d.]+)", float, "logs/run.log (07)")
    grab("logit_events", r"events (\d+) of", I, "logs/run.log (07)")
    grab("moran_resp", r"Moran.s I of response \(kNN8\): (-?[\d.]+),", float, "logs/run.log (07)")
    grab("moran_resp_p", r"Moran.s I of response \(kNN8\): -?[\d.]+, p ([\d.]+)", float, "logs/run.log (07)")
    grab("moran_resid", r"Moran.s I of OLS residuals: (-?[\d.]+),", float, "logs/run.log (07)")
    grab("gwr_bw", r"GWR bandwidth (\d+) of", I, "logs/run.log (07)")
    grab("gwr_r2", r"GWR bandwidth \d+ of \d+ neighbours; R2 ([\d.]+)", float, "logs/run.log (07)")
    grab("gwr_adjr2", r"GWR bandwidth.*adjR2 (-?[\d.]+) AICc", float, "logs/run.log (07)")
    grab("gwr_aicc", r"GWR bandwidth.*AICc (-?[\d.]+)", float, "logs/run.log (07)")
    grab("mgwr_r2", r"MGWR bandwidths.*; R2 ([\d.]+)", float, "logs/run.log (07)")
    grab("mgwr_adjr2", r"MGWR bandwidths.*adjR2 (-?[\d.]+) AICc", float, "logs/run.log (07)")
    grab("mgwr_aicc", r"MGWR bandwidths.*AICc (-?[\d.]+)", float, "logs/run.log (07)")
    m = re.findall(r"WorldPop grid (\d+) x (\d+)", txt)
    if m: F["wp_grid"] = {"v": [int(m[-1][0]), int(m[-1][1])], "src": "logs/run.log (06)"}
    m = re.findall(r"2 km cells with >=1 person: ([\d,]+)", txt)
    if m: F["cells2km"] = {"v": int(m[-1].replace(",", "")), "src": "logs/run.log (06)"}
    return F


def stage_A():
    say("[A] tehsils / provinces / observed / cells / buildings / relief / facts")
    t = gpd.read_file(PROC / "tehsil_dataset.gpkg").reset_index(drop=True)
    t["geometry"] = t.geometry.simplify(400, preserve_topology=True)
    t["prov"] = t.ADM1_NAME.str.title(); t["dist"] = t.ADM3_NAME.str.replace(" DISTRICT", "", regex=False).str.title()
    t["tname"] = t["name"].str.replace(" SUB-TEHSIL", " (sub-tehsil)", regex=False).str.replace(" TEHSIL", "", regex=False).str.title()
    keep = {"GEO_MATCH": "code", "tname": "name", "prov": "prov", "dist": "dist", "pop_census2017": "pop", "pop_wp": "popwp", "popA": "popA", "popB": "popB", "popC": "popC", "share_A": "shA", "share_C": "shC",
            "pct_65p": "p65", "pct_0_14": "p014", "pct_15_24": "p1524", "pct_25_44": "p2544", "pct_45_64": "p4564", "pct_female": "fem", "hh_size": "hhs", "density": "dens", "elev_mean": "elev",
            "osm_bldg_per_1000pop": "bper", "area_km2": "km2", "in_study": "st", "rp100": "mod100", "rp10": "mod10", "rp500": "mod500", "nb": "nb", "nbf": "nbf"}
    d = t[list(keep)].rename(columns=keep)
    d["sh100"] = np.where(d.popwp > 0, d.mod100 / d.popwp, np.nan); d["sh10"] = np.where(d.popwp > 0, d.mod10 / d.popwp, np.nan); d["sh500"] = np.where(d.popwp > 0, d.mod500 / d.popwp, np.nan)
    d = d.drop(columns=["mod100", "mod10", "mod500"])
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].round(4 if c in ("shA", "shC", "sh10", "sh100", "sh500") else 1)
    d["st"] = d.st.astype(int)
    write("tehsils.json", fc(gpd.GeoDataFrame(d, geometry=t.geometry.values, crs=AEA), list(d.columns), 3))
    prov = gpd.read_file(RAW / "admin/pak_admin1.shp")
    prov = prov.assign(name=prov.adm1_name.str.title())[["name", "geometry"]].to_crs(AEA)
    prov["geometry"] = prov.geometry.simplify(1500, preserve_topology=True)
    write("provinces.json", fc(prov, ["name"], 3))
    ex = gpd.read_file(PROC / "flood_obs_2022.gpkg"); ex["geometry"] = ex.geometry.simplify(500, preserve_topology=True)
    write("observed.json", fc(ex.assign(src="UNOSAT VIIRS"), ["src"], 3))
    c = pd.read_csv(PROC / "cells_2km.csv"); c = c[c.t > 0]
    cols = ["lon", "lat", "pop", "popA", "popB", "popC", "nb", "nbf", "r10", "r100", "r500", "t"]
    rows = [[round(r.lon, 3), round(r.lat, 3), int(round(r.pop)), int(round(r.popA)), int(round(r.popB)), int(round(r.popC)), int(r.nb), int(r.nbf), int(round(r.r10)), int(round(r.r100)), int(round(r.r500)), int(r.t) - 1] for r in c.itertuples()]
    write("cells.json", {"cols": cols, "rows": rows})
    b = gpd.read_file(PROC / "osm_buildings.gpkg", where="flood_obs = 1 AND residential = 1")
    caps = pd.read_csv(PROC / "bldg_capture_flags.csv").set_index("osm_id")
    cen = gpd.GeoSeries(b.geometry.centroid, crs=AEA).to_crs(4326)
    cf = caps.reindex(b.osm_id.values)
    pts = [[round(x, 4), round(y, 4), int(a), int(bb), int(cc)] for x, y, a, bb, cc in zip(cen.x, cen.y, cf.rp10.fillna(0), cf.rp100.fillna(0), cf.rp500.fillna(0))]
    write("bldg_flooded.json", {"cols": ["lon", "lat", "rp10", "rp100", "rp500"], "rows": pts})
    shutil.copy(PROC / "hillshade_z8.png", SITE / "assets/relief.png")
    w, s, e, n = map(float, (PROC / "hillshade_bounds.txt").read_text().split())
    (DATA / "relief.json").write_text(json.dumps({"bounds": [w, s, e, n]}), encoding="utf8")
    say(f"  relief.png {(SITE/'assets/relief.png').stat().st_size/1e6:.2f} MB")
    F = parse_logs()
    F["tehsil_dataset_n"] = {"v": len(d), "src": "outputs/tehsil_dataset.csv"}
    F["jrc"] = {"v": pd.read_csv(OUT / "modelled_vs_observed.csv").round(4).to_dict("records"), "src": "outputs/modelled_vs_observed.csv"}
    F["top10"] = {"v": pd.read_csv(OUT / "top10_exposed_tehsils.csv").round(3).to_dict("records"), "src": "outputs/top10_exposed_tehsils.csv"}
    F["vif"] = {"v": pd.read_csv(OUT / "vif.csv").rename(columns={"Unnamed: 0": "name"}).to_dict("records"), "src": "outputs/vif.csv"}
    F["logit"] = {"v": pd.read_csv(OUT / "logit_any_exposure.csv").rename(columns={"Unnamed: 0": "name"}).to_dict("records"), "src": "outputs/logit_any_exposure.csv"}
    ds = pd.read_csv(OUT / "regression_sample.csv")
    PRED = ["pct_65p", "pct_0_14", "pct_15_24", "pct_female", "hh_size", "density", "elev_mean"]
    F["spearman"] = {"v": {p: round(float(ds.share_A.corr(ds[p], method="spearman")), 3) for p in PRED}, "src": "recomputed from outputs/regression_sample.csv"}
    F["hist"] = {"v": [round(float(v), 4) for v in ds.share_A], "src": "outputs/regression_sample.csv (share_A)"}
    S = pd.read_csv(OUT / "tehsil_dataset.csv"); S = S[S.in_study]
    F["by_province"] = {"v": S.groupby("ADM1_NAME").agg(tehsils=("name", "size"), pop_wp=("pop_wp", "sum"), popA=("popA", "sum"), popB=("popB", "sum"), popC=("popC", "sum")).round(0).reset_index().to_dict("records"), "src": "outputs/tehsil_dataset.csv"}
    invf = SITE / "build/inventory.json"
    F["inventory"] = {"v": json.loads(invf.read_text(encoding="utf8")) if invf.exists() else [], "src": "build/inventory.json (from scripts/00_download*.sh and the HDX catalogue)"}
    write("facts.json", F)


def stage_B():
    say("[B] analysis window")
    t = pd.read_csv(OUT / "tehsil_dataset.csv"); top = t.sort_values("nbf", ascending=False).iloc[0]
    g = gpd.read_file(PROC / "tehsil_dataset.gpkg"); row = g[g.GEO_MATCH == top.GEO_MATCH].iloc[0]
    c = row.geometry.representative_point(); R = 8000
    wb = box(c.x - R, c.y - R, c.x + R, c.y + R)
    ex = gpd.read_file(PROC / "flood_obs_2022.gpkg"); ex = ex[ex.intersects(wb)]
    obs = ex.geometry.intersection(wb).union_all()
    wbb = tuple(gpd.GeoSeries([wb], crs=AEA).to_crs(4326).total_bounds)
    b = gpd.read_file(PROC / "osm_buildings.gpkg", bbox=tuple(wb.bounds))
    b = b[b.intersects(wb)].reset_index(drop=True)
    caps = pd.read_csv(PROC / "bldg_capture_flags.csv").set_index("osm_id")

    def poly(g_, nd=1):
        m = mapping(g_); return {"t": m["type"], "c": rnd(m["coordinates"], nd)}
    bl = []
    for r in b.itertuples():
        k = 2 if (r.flood_obs and r.residential) else 3 if r.flood_obs else 1 if r.residential else 0
        o = {"k": k, "g": poly(r.geometry.simplify(0.5))}
        if k == 2:
            o["cap"] = [int(caps.loc[r.osm_id, f"rp{x}"]) if r.osm_id in caps.index else 0 for x in (10, 100, 500)]
        bl.append(o)
    win = {"center": [c.x, c.y], "R": R, "name": str(row["name"]).replace(" TEHSIL", "").title(), "prov": str(row.ADM1_NAME).title(), "obs": [poly(obs, 0)] if not obs.is_empty else [], "bld": bl}
    for rp in (10, 100, 500):
        z = gpd.read_file(DATA / f"ror_rp{rp}.json").set_crs(4326).to_crs(AEA)
        gg = [shapely.make_valid(g_) for g_ in z.geometry if g_.intersects(wb)]
        zz = shapely.union_all([g_.intersection(wb) for g_ in gg]).simplify(30) if gg else shapely.Polygon()
        win[f"ror{rp}"] = [] if zz.is_empty else [poly(zz, 0)]
    (DATA / "window.json").write_text(json.dumps(win, separators=(",", ":")), encoding="utf8")
    say(f"  window.json {(DATA/'window.json').stat().st_size/1e6:.2f} MB; {win['name']} ({win['prov']}); buildings {len(bl)}; flooded residential {sum(1 for x in bl if x['k']==2)}")


if __name__ == "__main__":
    for st in sys.argv[1:] or ["A"]:
        globals()["stage_" + st]()
