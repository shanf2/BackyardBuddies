function initAddressMap() {
  const map = new google.maps.Map(document.getElementById("register_map"), {
    center: { lat: 43.2609, lng: -79.9192},
    zoom: 13,
    //mapTypeId: "roadmap",
  });
  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);

  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  let markers = [];

  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    //markers = [];

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      const houseMarker = new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        });
	  console.log(houseMarker.title);
	  console.log(houseMarker.position.lat());
	  document.getElementById('id_address').value = houseMarker.title;
	  var pos = {lat: houseMarker.position.lat(), lng: houseMarker.position.lng()};
	  document.getElementById('id_location').value = JSON.stringify(pos);
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}

function saveAddressLocation() {
	console.log(houseMarker.title)
	document.getElementById('id_address').value = houseMarker.title;
	document.getElementById('id_location').value = houseMarker.position;
}

window.initAddressMap = initAddressMap;