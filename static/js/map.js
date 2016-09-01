var map;
function getFromDb(map) {

	$.getJSON('getMethod', function(data) {
		var items = data.map(function (item) { 
			return new google.maps.Marker({
				map: map,
				position: {lat: item['latitude'], lng: item['longitude']},
				title: item['lables']
			}); /* item['photopath'] is the filename */
		});
	});

}

function initMap() {
  var myLatLng = {lat: 31.7, lng: 35.5};

  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 7
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

  var image = "../img/icon.png"

  var marker = new google.maps.Marker({
    map: map,
    position: myLatLng,
    title: 'cat',
    icon: image
  });

  marker.addListener('click', function() {
    infowindow.open(map, marker);
  });

  var marker2 = new google.maps.Marker({
    map: map,
    position: {lat: 33.081084, lng: 35.794388},
    title: 'dog'
  });
}

