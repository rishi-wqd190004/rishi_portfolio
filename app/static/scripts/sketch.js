let visited;
let countries;
const mappa = new Mappa('Leaflet');
let visitmap;
let canvas;

let data = [];

const options = {
  lat: 0,
  lng: 0,
  zoom: 1.5,
  style: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'
};

function preload() {
  visited = loadTable('../static/data/visited.csv', 'header');
  countries = loadJSON('../static/data/places.json');
}

function setup() {
  canvas = createCanvas(window.outerWidth, 400);
  canvas.parent('canvas-container'); // matches your HTML!
  visitmap = mappa.tileMap(options);
  visitmap.overlay(canvas);

  for (let row of visited.rows) {
    let countryName = row.get('country');
    // Find the country object in the array, case-insensitive match
    let countryObj = countries.ref_country_codes.find(
      c => c.country.toLowerCase() === countryName.toLowerCase()
    );
    if (!countryObj) {
      console.warn(`No coordinates found for country: ${countryName}`);
      continue;
    }
    let latitude = countryObj.latitude;
    let longitude = countryObj.longitude;
    data.push({latitude, longitude});
  }

  console.log(data);
}

function draw() {
  clear();
  for (let country of data) {
    const pix = visitmap.latLngToPixel(country.latitude, country.longitude);
    fill(255, 0, 200, 100);
    const zoom = visitmap.zoom();
    const scl = pow(2, zoom);
    ellipse(pix.x, pix.y, 3 * scl);
  }
}
