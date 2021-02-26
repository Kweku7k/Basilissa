

// There are 2 ways i can go about this... 
// 1.Loop through for all the coloured background
// 2.Append color when clicked...
// Personally, I like 1.

order = []
function addToCart(event){
button = event.target
holder = button.parentElement
id = holder.getElementsByClassName('id')[0].innerText
button.classList.toggle("mystyle");
console.log(holder)
if (button.style.color !== 'black'){
  console.log(button)
  console.log(id)
  order.push(parseInt(id))
  console.log(order)
}
// button.style.background = "black"
// button.innerText = "Added To Cart"
// button.style.color = "yellow"
}

function done(){
  button = document.getElementsByClassName('button');
  var finalarray = []
  for (i = 0; i < button.length; i++) {
    if(button[i].classList.contains('mystyle')){
      var card = button[i].parentElement
      var id = card.getElementsByClassName('id')[0].innerText
      console.log(id)
      finalarray.push(id)
      console.log(finalarray)
    }
    else{
      console.log('lol')
      console.log(document.getElementsByClassName('button')[i].style.color)
    }
  }
  GoToCart(finalarray)
  // console.log(button)
  // if (button[1].classList.contains('button')){
  //   console.log('kaish')
  // }
}

function GoToCart(m_array){
  console.log(m_array)
  localStorage.setItem("cart", m_array);
  document.getElementById('storage').value = m_array
}

function handle_data(){
  var finalorder = []
  var card = document.getElementsByClassName('flex')
  console.log(card)
  for (i=0; i< card.length; i++){
    console.log(card[i])
    cart_id = card[i].getElementsByClassName('cart-id')[0].innerText
    cart_quantity = card[i].getElementsByClassName('quantity')[0].innerText
    cart_name = card[i].getElementsByClassName('cart_name')[0].innerText
    console.log(cart_id)
    console.log(cart_quantity)
    var order = {
      itemid : cart_id,
      itemquantity : cart_quantity,
      itemname: cart_name
    };
    finalorder.push(order)
    console.log(finalorder)
  }
}

function ShowSummary(){

}

function myFunction() {
  var element = document.getElementsByClassName("button")[0];
  element.classList.toggle("mystyle");
}

function increase(event){
    initial_value = event.target.parentElement;
    console.log(initial_value);
    let quantityElement = initial_value.getElementsByClassName('quantity')[0];
    let value = quantityElement.innerHTML;
    // increment value
    let newValue = (+value + 1);
    quantityElement.innerText = newValue;
    console.log(newValue);
    let inform = event.target.parentElement.parentElement;
    console.log(inform)
}


function decrease(event){
    initial_value = event.target.parentElement;
    console.log(initial_value);
    let quantityElement = initial_value.getElementsByClassName('quantity')[0];
    let value = quantityElement.innerHTML;
    // increment value
    let newValue = (+value - 1);
    quantityElement.innerText = newValue;
    console.log(newValue);
    let inform = event.target.parentElement.parentElement;
    console.log(inform)
}
// 
var button = document.getElementById("locate");

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else { 
    document.getElementById('mapholder').innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  var latlon = position.coords.latitude + "," + position.coords.longitude;

  var img_url = "https://maps.googleapis.com/maps/api/staticmap?center="+latlon+"&zoom=14&size=400x100&key=AIzaSyDkgDF0X-kweO5xG2AiiGmkqd-7XyeNjLE";

  document.getElementById("mapholder").innerHTML = "<img src='"+img_url+"'>";
}

function showError(error) {
  x = document.getElementById('mapholder')
  switch(error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      break;
  }
}

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

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
     
