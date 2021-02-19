
// Initialize and add the map
function initMap() {
    // The location of Uluru
    const uluru = { lat: 5.738548696970146, lng: 0.03265251065119554 };
  
  
    // The map, centered at Uluru
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 20,
      center: uluru,
    });
    // The marker, positioned at Uluru
    const marker = new google.maps.Marker({
      position: uluru,
      map: map,
      zoom: 4,
    });
  }