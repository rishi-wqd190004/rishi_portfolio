const sketch = (p) => {
  let visitedTable;
  let countryData;
  const mappa   = new Mappa('Leaflet');
  let leafletMap;
  let canvas;
  let dots = [];
  const mapOpts = {
    lat   : 0,
    lng   : 0,
    zoom  : 1.5,
    style : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  };

  p.preload = function() {
    visitedTable = p.loadTable('../static/data/visited.csv', 'header');
    countryData  = p.loadJSON('../static/data/places.json');
  };

  p.setup = function() {
    const holder = document.getElementById('canvas-container');
    if (!holder) return;
    canvas = p.createCanvas(holder.offsetWidth, 400);
    canvas.parent('canvas-container');
    leafletMap = mappa.tileMap({ ...mapOpts, parent: holder });
    leafletMap.overlay(canvas);

    visitedTable.rows.forEach(row => {
      const countryName = row.get('country').trim().toLowerCase();
      const match = countryData.ref_country_codes.find(
        c => c.country.toLowerCase() === countryName
      );
      if (match) {
        dots.push({ lat: match.latitude, lng: match.longitude });
      } else {
        console.warn(`No coords for ${countryName}`);
      }
    });
  };

  p.windowResized = function() {
    const holder = document.getElementById('canvas-container');
    if (holder && canvas) {
      p.resizeCanvas(holder.offsetWidth, 400);
    }
  };

  p.draw = function() {
    if (!canvas) return;
    p.clear();
    const zoomFactor = p.pow(2, leafletMap.zoom());
    dots.forEach(pt => {
      const pos = leafletMap.latLngToPixel(pt.lat, pt.lng);
      p.fill(255, 0, 200, 120);
      p.noStroke();
      p.ellipse(pos.x, pos.y, 3 * zoomFactor);
    });
  };
};

// Only create the sketch if the container exists
window.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('canvas-container')) {
    new p5(sketch);
  }
});
