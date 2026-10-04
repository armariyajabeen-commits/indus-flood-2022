# When the Indus rose: Pakistan 2022 (second edition)

A static research site (full-screen MapLibre map, top control bar, floating legend and layer cards, 430 px side panel, light/dark theme, phone layout) carrying the Pakistan run of the same data chain used for the Netherlands (`../pk_verification`).

## Run it

Browsers block `fetch` from `file://`, so serve the folder:

```bash
cd "D:/flood anaylsis/pk_site"
python -m http.server 8791
```

Open http://localhost:8791/ (map) and http://localhost:8791/analysis/ (evidence and method). Needs internet for MapLibre, D3, Public Sans and the CARTO basemap (plain background if the basemap cannot be reached in 6 s).

## What it shows

| Page | Content |
|---|---|
| `index.html` | Tehsil choropleth, province/tehsil filters, A/B circles over 2 km cells (summed from the WorldPop 100 m grid), observed UNOSAT/VIIRS flood extent, flooded OSM buildings (points), modelled JRC river-flood scenarios (hatched, separate legend group, 10/100/500 years) with depth classes, terrain relief. |
| `analysis/index.html` | Headline numbers, observed vs modelled, provenance chain, methods A/B/C, top tehsils, input quality, regression feasibility, what could not be obtained, limits, sources. |

## Where the numbers come from

`data/facts.json` is parsed from `pk_verification/logs/run.log` and the output tables by `build/build_pk_assets.py`; every value has a `src` field. The pages read it at load time.

## Rebuild

```bash
cd ../pk_verification
bash scripts/00_download.sh; bash scripts/00b_download_jrc.sh        # about 1 GB
python scripts/01_flood_and_study_area.py   # then 02, 03, 04, 06, 07, 08 in order
cd ../pk_site/build
python build_pk_assets.py A B
```

Display copies (simplified polygons, 2 km cells, building centroids, relief PNG) are for drawing only; no figure is computed from them.

## Known limits

- The observed extent is a satellite water detection (about 375 m, cumulative, preliminary).
- WorldPop is a modelled population (2020); census age data is tehsil level, 2017.
- OpenStreetMap buildings are incomplete in Pakistan; counts are lower bounds.
- The modelled layers are global river-flood scenarios, not the 2022 event.
- No land cover, soil, roads, health, income or deprivation data were obtained (see the audit).
