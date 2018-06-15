// Global variables. Empty array for markers and infoWindow variable.
var markers = [];
var infoWindow;

// This function allows for the Google Map to be rendered as well as all markers to be created.
function initMap() {

    // Constructor creates a new map.
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 29.976480,
            lng: 31.131302
        },
        zoom: 3,
        mapTypeControl: true,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
            position: google.maps.ControlPosition.BOTTOM_CENTER
        }
    });


    // Declare a new geocoder object.
    var geocoder = new google.maps.Geocoder();

    $(document).ready(function () {
        var Places;
        $.ajax({
            dataType: "json",
            url: 'http://ec2-18-220-254-32.us-east-2.compute.amazonaws.com/json/',
            data: Places,
            success: function (Places) {
                // begin accessing JSON data here
                // For each place in Places, call the geocodePlace function which geocodes the addresses.
                Places.forEach(function(place) {
                    geocodePlace(geocoder, place, map);
                });
                
                // Declare a new infoWindow object.
                infoWindow = new google.maps.InfoWindow();
            }
        });
    });
}

// This function allows each marker to be clicked triggering a google maps marker event.
function clickMarker(name) {
    markers.forEach(function(markerItem) {
        if (markerItem.name == name) {
            google.maps.event.trigger(markerItem.marker,
                'click');
        }
    });
}

// This function allows a marker to have a bounce animation.
function markerBounce(marker) {
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
        setTimeout(function() {
            marker.setAnimation(null);
        }, 1200);
    }
}

// geocodes the address passed from the forEach function, for each place in Places.
function geocodePlace(geocoder, place, placesMap) {

    var latlng = {
        lat: parseFloat(place.lat),
        lng: parseFloat(place.lng)
    };

    // Uses Google's geocode method to parse the latlng of the place.address then set it on map.
    geocoder.geocode({
        'location': latlng
    }, function(results, status) {
        if (status === 'OK') {
            placesMap.setCenter(results[0].geometry.location);

            // Create a new place marker object based on geocode latlng results.
            // Animate the marker.
            place.marker = new google.maps.Marker({
                map: placesMap,
                position: latlng,
                animation: google.maps.Animation.DROP,
            });

            // Add name and marker to marker object.
            markers.push({
                name: place.name,
                marker: place.marker
            });

            // Event listener for when user clicks on marker.
            // Clicking marker will show the Wikipedia info and bounce the marker.
            google.maps.event.addListener(place.marker,
                'click',
                function() {
                    placetext(place);
                    markerBounce(place.marker);
                    map.panTo(place.marker.position)
                });

            //Resize Function
            google.maps.event.addDomListener(window, "resize",
                function() {
                    var center = map.getCenter();
                    google.maps.event.trigger(map,
                        "resize");
                    map.setCenter(center);
                });

        } else {
            alert('This location has an invalid address.');
        }
    });
}

// This function generates infowindow content.
function placetext(place) {
    // If marker clicked, open; if open, and x closed, close.
    if (infoWindow.marker != place.marker) {
        infoWindow.marker = place.marker;
        infoWindow.open(map, place.marker);
        infoWindow.addListener('closeclick', function() {
            infoWindow.setMarker = null;
        });

        // Set the content of the ajax query to the infoWindow.
        infoWindow.setContent('<div class="infoWindow"><h5>' + place.name +
            '</h5><br><h6>' + place.description +
            '<br><br>Added by ' + place.creator + ' <br>on ' + place.date +
            '</h6)');
    };
}

// Google Maps API error handling.
function apiError() {
    alert("There was an issue loading the Google Maps API.");
}