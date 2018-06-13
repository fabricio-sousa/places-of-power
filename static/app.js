// Model Places array of 5 places with name and address.
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

// Global variables. Empty array for markers and infoWindow variable.
var markers = [];
var infoWindow;

// This function allows for the Google Map to be rendered as well as all markers to be created.
function initMap() {

    // Constructor creates a new map.
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      mapTypeControl: true,
      mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
          position: google.maps.ControlPosition.BOTTOM_CENTER
      }
    });
      
  
    // Declare a new geocoder object.
    var geocoder = new google.maps.Geocoder();
  
    // For each place in Places, call the geocodePlace function which geocodes the addresses.
    Places.forEach(function(place) {
      geocodePlace(geocoder, place, map);
    });
  
    // Declare a new infoWindow object.
    infoWindow = new google.maps.InfoWindow();
  
    // Apply all KnockOut Bindings.
    ko.applyBindings(new ViewModel());
  
  }

// This function allows each marker to be clicked triggering a google maps marker event.
function clickMarker(name) {
	markers.forEach(function(markerItem) {
		if (markerItem.name == name) {
			google.maps.event.trigger(markerItem.marker, 'click');
		}
	});
}