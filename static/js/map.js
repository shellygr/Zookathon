var map;
var markers = [];

function getConservationStatus(endangerStatus) {
	if (endangerStatus == 0)
		return "Least concern";

	if (endangerStatus == 1)
		return "Near threatened";

	if (endangerStatus == 2)
		return "Vulnerable";

	if (endangerStatus == 3)
		return "Endangered";
	
        if (endangerStatus == 4)
                return "Critically endangered";

        if (endangerStatus == 5)
                return "Extinct in the wild";

        if (endangerStatus == 6)
                return "Extinct";

}

function getFromDb(map) {

	$.getJSON('getMethod', function(data) {



		var items = data.map(function (item) {
		    	      var contentString = '<div id="content">'+
                        '<h3>'+item['lables']+'</h3>'+
                        '<div id="bodyContent">'+
			'<i>Photo taken on: '+item['dateTaken'] + "</i><br/>" +
			(item['endangeredStatus'] >= 0 ? ('<i>Conservation status: '+getConservationStatus(item['endangeredStatus']) + "</i><br/>") : "")  +
                        '<img src="uploads/'+item['photopath']+'" ' +
                        'style="width:150px;float:right;margin:5px"/>' +
                        '</div>' +
                        '</div>';


            var iconImage = "../img/blueIcon.png"
			curMarker = new google.maps.Marker({
				map: map,
				position: {lat: item['latitude'], lng: item['longitude']},
				title: item['lables'],
				icon:iconImage
			}); /* item['photopath'] is the filename */
			curMarker.markedLables = item['lables'];
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });
	  infowindow.yourMarker = curMarker;
	  curMarker.addListener('click', function() {
                infowindow.open(map, infowindow.yourMarker);
                });
            markers.push(curMarker);
            return curMarker;
		});
	});

}

function filterTextDownKey()
{
    filterMarkers(document.getElementById('filterMarkers').value);
}

function filterMarkers(lable)
{
        for(var i=0;i<markers.length;i++)
        {
            if(markers[i].markedLables.includes(lable))
                markers[i].setMap(map);
            else
                markers[i].setMap(null);
        }
}

function initMap() {
  var myLatLng = {lat: 31.7, lng: 35.5};

  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 3
  });

    // Create the search box and link it to the UI element.
  var input = document.getElementById('search-input');
  var searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
	map.controls[google.maps.ControlPosition.TOP_LEFT].push(document.getElementById('filterMarkers'));

  // Bias the SearchBox results towards current map's viewport.
/*  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });
*/
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

  getFromDb(map);

  var contentString = '<div id="content">'+
    '<h1>Cat</h1>'+
    '<div id="bodyContent">'+
    '<p>The domestic cat (Latin: Felis catus) or the feral cat (Latin: Felis silvestris catus) ' +
    'is a small, typically furry, carnivorous mammal. </p>'+
    '<img src="https://pixabay.com/static/uploads/photo/2014/03/29/09/17/cat-300572_960_720.jpg" ' +
    'style="width:200px"/>' +
    '</div>' +
    '</div>';

  var infowindow = new google.maps.InfoWindow({
    content: contentString
  });

  var image = "../img/greenIcon.png"
/*
  var marker = new google.maps.Marker({
    map: map,
    position: myLatLng,
    title: 'cat',
    icon: image
  });

  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });
*/
 /* var marker2 = new google.maps.Marker({
    map: map,
    position: {lat: 33.081084, lng: 35.794388},
    title: 'dog'
  });*/
}

