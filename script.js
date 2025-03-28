// static/js/script.js

document.addEventListener('DOMContentLoaded', function () {
    // Check if the map element exists on the page
    const mapElement = document.getElementById('map');
    
    if (mapElement) {
        initMap();
    }

    // Example: Handling form validations or any additional interactivity
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            const name = document.getElementById('name');
            const phone = document.getElementById('phone');
            const vehicleType = document.getElementById('vehicle_type');
            const issueDescription = document.getElementById('issue_description');

            // Simple validation check
            if (!name.value || !phone.value || !vehicleType.value || !issueDescription.value) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    }
});

function initMap() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;

            document.getElementById('latitude').value = lat;
            document.getElementById('longitude').value = lng;

            const userLocation = { lat: lat, lng: lng };
            const map = new google.maps.Map(document.getElementById('map'), {
                center: userLocation,
                zoom: 15
            });

            new google.maps.Marker({
                position: userLocation,
                map: map
            });
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
