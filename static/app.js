// Model Places of Power array of 5 places with name and address.
var Places = [
	{
		name: 'Machu Picchu', 
		lat: '-13.16333',
		lng: '-72.54556', 
		description: 'To me it evokes feelings of mystery and wonder. How could a civilization so old build something so grand?',
		picture_url: 'https://i.imgur.com/vNjaWP4.jpg'
	},
	
	{
		name: 'Stonehenge', 
		lat: '51.1789', 
		lng: '-1.8262', 
		description: 'Stonehenge is a prehistoric monument in Wiltshire, England, 2 miles (3 km) west of Amesbury. It consists of a ring of standing stones, with each standing stone around 13 feet (4.0 m) high, 7 feet (2.1 m) wide and weighing around 25 tons.',
		picture_url: 'https://upload.wikimedia.org/wikipedia/commons/3/3c/Stonehenge2007_07_30.jpg'
	},
	
	{
		name: 'The Great Pyramid of Giza', 
		lat: '29.976480', 
		lng: '31.131302', 
		description: 'One of the 7 Wonders of the Ancient World. A place of magic and mystery.',
		picture_url: 'https://i.imgur.com/E4DZ4nH.jpg'
	}
];

var map;
// Create a new blank array for all Places of Power.
var markers = [];

function initMap() {
	// Create a styles array to use with the map.
	var styles = [
	  {
		featureType: 'water',
		stylers: [
		  { color: '#19a0d8' }
		]
	  },{
		featureType: 'administrative',
		elementType: 'labels.text.stroke',
		stylers: [
		  { color: '#ffffff' },
		  { weight: 6 }
		]
	  },{
		featureType: 'administrative',
		elementType: 'labels.text.fill',
		stylers: [
		  { color: '#e85113' }
		]
	  },{
		featureType: 'road.highway',
		elementType: 'geometry.stroke',
		stylers: [
		  { color: '#efe9e4' },
		  { lightness: -40 }
		]
	  },{
		featureType: 'transit.station',
		stylers: [
		  { weight: 9 },
		  { hue: '#e85113' }
		]
	  },{
		featureType: 'road.highway',
		elementType: 'labels.icon',
		stylers: [
		  { visibility: 'off' }
		]
	  },{
		featureType: 'water',
		elementType: 'labels.text.stroke',
		stylers: [
		  { lightness: 100 }
		]
	  },{
		featureType: 'water',
		elementType: 'labels.text.fill',
		stylers: [
		  { lightness: -100 }
		]
	  },{
		featureType: 'poi',
		elementType: 'geometry',
		stylers: [
		  { visibility: 'on' },
		  { color: '#f0e4d3' }
		]
	  },{
		featureType: 'road.highway',
		elementType: 'geometry.fill',
		stylers: [
		  { color: '#efe9e4' },
		  { lightness: -25 }
		]
	  }
	];
	// Constructor creates a new map - only center and zoom are required.
	map = new google.maps.Map(document.getElementById('map'), {
	  center: {lat: 29.976480, lng: 31.131302},
	  zoom: 3,
	  styles: styles,
	  mapTypeControl: false
	});

	var largeInfowindow = new google.maps.InfoWindow();
	// Style the markers a bit. This will be our listing marker icon.
	var defaultIcon = makeMarkerIcon('0091ff');
	// Create a "highlighted location" marker color for when the user
	// mouses over the marker.
	var highlightedIcon = makeMarkerIcon('FFFF24');
	var largeInfowindow = new google.maps.InfoWindow();
	// The following group uses the location array to create an array of markers on initialize.
	for (var i = 0; i < Places.length; i++) {
	  // Get the position from the location array.
	  var position = Places[i].lat + Places[i].lng;
	  var title = Places[i].name;
	  // Create a marker per location, and put into markers array.
	  var marker = new google.maps.Marker({
		position: position,
		title: title,
		animation: google.maps.Animation.DROP,
		icon: defaultIcon,
		id: i
	  });
	  // Push the marker to our array of markers.
	  markers.push(marker);
	  // Create an onclick event to open the large infowindow at each marker.
	  marker.addListener('click', function() {
		populateInfoWindow(this, largeInfowindow);
	  });
	  // Two event listeners - one for mouseover, one for mouseout,
	  // to change the colors back and forth.
	  marker.addListener('mouseover', function() {
		this.setIcon(highlightedIcon);
	  });
	  marker.addListener('mouseout', function() {
		this.setIcon(defaultIcon);
	  });
	}
	document.getElementById('show-listings').addEventListener('click', showListings);
	document.getElementById('hide-listings').addEventListener('click', hideListings);
  }
  // This function populates the infowindow when the marker is clicked. We'll only allow
  // one infowindow which will open at the marker that is clicked, and populate based
  // on that markers position.
  function populateInfoWindow(marker, infowindow) {
	// Check to make sure the infowindow is not already opened on this marker.
	if (infowindow.marker != marker) {
	  infowindow.marker = marker;
	  infowindow.setContent('<div>' + marker.title + '</div>');
	  infowindow.open(map, marker);
	  // Make sure the marker property is cleared if the infowindow is closed.
	  infowindow.addListener('closeclick', function() {
		infowindow.marker = null;
	  });
	}
  }
  // This function will loop through the markers array and display them all.
  function showListings() {
	var bounds = new google.maps.LatLngBounds();
	// Extend the boundaries of the map for each marker and display the marker
	for (var i = 0; i < markers.length; i++) {
	  markers[i].setMap(map);
	  bounds.extend(markers[i].position);
	}
	map.fitBounds(bounds);
  }
  // This function will loop through the listings and hide them all.
  function hideListings() {
	for (var i = 0; i < markers.length; i++) {
	  markers[i].setMap(null);
	}
  }
  // This function takes in a COLOR, and then creates a new marker
  // icon of that color. The icon will be 21 px wide by 34 high, have an origin
  // of 0, 0 and be anchored at 10, 34).
  function makeMarkerIcon(markerColor) {
	var markerImage = new google.maps.MarkerImage(
	  'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|'+ markerColor +
	  '|40|_|%E2%80%A2',
	  new google.maps.Size(21, 34),
	  new google.maps.Point(0, 0),
	  new google.maps.Point(10, 34),
	  new google.maps.Size(21,34));
	return markerImage;
  }