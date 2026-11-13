// node mapgen.js '{"s":..,"tx":..,"ty":..,"w":1920,"h":1080}'
// -> {countries:{id:path}, provinces:[{name, d}], vn:path(outline)}
const topo = require('topojson-client');
const d3 = require('d3-geo');
const world = require('world-atlas/countries-50m.json');
const vn = require('./vn/vn34.topo.json');
const cfg = JSON.parse(process.argv[2]);
const pad = cfg.pad ?? 50;
const proj = d3.geoMercator().scale(cfg.s).translate([cfg.tx, cfg.ty]).clipExtent([[-pad, -pad], [cfg.w + pad, cfg.h + pad]]);
const path = d3.geoPath(proj);
const out = { countries: {}, provinces: [], vn: '' };
for (const f of topo.feature(world, world.objects.countries).features) {
  if (f.id === '704') continue; // Việt Nam vẽ bằng dữ liệu 34 tỉnh (có Hoàng Sa, Trường Sa)
  const p = path(f);
  if (p && p.length > 20) out.countries[f.id] = p;
}
for (const f of topo.feature(vn, vn.objects.provinces).features) {
  const p = path(f);
  if (p) out.provinces.push({ name: f.properties.TinhThanh, d: p });
}
out.vn = path(topo.merge(vn, vn.objects.provinces.geometries)) || '';
process.stdout.write(JSON.stringify(out));
