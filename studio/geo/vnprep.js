// Tiền xử lý 1 lần: 34 tỉnh (GeoJSON 16MB) -> TopoJSON rút gọn (vn34.topo.json)
const fs = require('fs');
const { topology } = require('topojson-server');
const { presimplify, simplify, quantile } = require('topojson-simplify');
const gj = JSON.parse(fs.readFileSync(__dirname + '/vn/provinces34.geojson', 'utf8'));
let topo = topology({ provinces: gj }, 1e6);
topo = presimplify(topo);
topo = simplify(topo, quantile(topo, 0.12));
fs.writeFileSync(__dirname + '/vn/vn34.topo.json', JSON.stringify(topo));
console.log('ok', (JSON.stringify(topo).length / 1e6).toFixed(2), 'MB');
