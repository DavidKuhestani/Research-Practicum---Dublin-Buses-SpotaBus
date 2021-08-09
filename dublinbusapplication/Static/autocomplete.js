let step_distance;
let arrival_stop;
let arrival_time;
let departure_time;
let departure_time_text;
let transit_departure_time;
let walking_time_text;
let walking_time_value;

class AutocompleteDirectionsHandler {
    map;
    originPlaceId;
    destinationPlaceId;
    travelMode;
    directionsService;
    directionsRenderer;

    constructor(map) {
        this.map = map;
        this.originPlaceId = "";
        this.destinationPlaceId = "";
        this.travelMode = google.maps.TravelMode.TRANSIT;
        this.directionsService = new google.maps.DirectionsService();
        this.directionsRenderer = new google.maps.DirectionsRenderer();
        this.directionsRenderer.setMap(map);
        const options = {
            componentRestrictions: {country: "ie"}
        };
        const originInput = document.getElementById("origin-input");
        const destinationInput = document.getElementById("destination-input");
        const originAutocomplete = new google.maps.places.Autocomplete(originInput, options);
        // Specify just the place data fields that you need.
        originAutocomplete.setFields(["place_id"]);
        const destinationAutocomplete = new google.maps.places.Autocomplete(
            destinationInput, options
        );


        this.setupPlaceChangedListener(originAutocomplete, "ORIG");
        this.setupPlaceChangedListener(destinationAutocomplete, "DEST");
    }


    // provides the route between two given stops

    setupPlaceChangedListener(autocomplete, mode) {
        autocomplete.bindTo("bounds", this.map);
        autocomplete.addListener("place_changed", () => {
            const place = autocomplete.getPlace();

            if (!place.place_id) {
                window.alert("Please select an option from the dropdown list.");
                return;
            }

            if (mode === "ORIG") {
                this.originPlaceId = place.place_id;
            } else {
                this.destinationPlaceId = place.place_id;
            }
            this.route();
        });
    }

    route() {
        const input_date = getDateTime();
        if (!this.originPlaceId || !this.destinationPlaceId) {
            return;
        }
        const me = this;
        this.directionsService.route(
            {
                origin: {placeId: this.originPlaceId},
                destination: {placeId: this.destinationPlaceId},
                travelMode: 'TRANSIT',
                transitOptions: {
                    modes: ['BUS'],
                    routingPreference: 'FEWER_TRANSFERS',
                    departureTime: new Date(input_date)
                }
            },

            (response, status) => {
                googleResponse = response
                if (status === "OK") {
                    me.directionsRenderer.setDirections(response);

                    const Steps = response.routes[0].legs[0].steps.length;
                    steps_array = [];

                    for (let y = 0; y < Steps; y++) {
                        const route_dict = {};
                        const Transit_Type = response.routes[0].legs[0].steps[y].travel_mode;

                        Direction_Steps = [];
                        departure_time = [];
                        departure_time_text = [];
                        arrival_time = [];
                        step_distance = [];
                        walking_time_text = []
                        walking_time_value = []

                        Direction_Steps = response.routes[0].legs[0].steps[y].instructions;
                        departure_time = response.routes[0].legs[0].departure_time.value.getTime()
                        departure_time_text = response.routes[0].legs[0].departure_time['text'];
                        arrival_time = response.routes[0].legs[0].arrival_time['text'];

                        route_dict['instructions'] = Direction_Steps;
                        route_dict['departure_time'] = departure_time;
                        route_dict['departure_time_text'] = departure_time_text;
                        route_dict['arrival_time'] = arrival_time;

                        if (Transit_Type === "WALKING") {


                            step_distance = response.routes[0].legs[0].steps[y].distance['text'];
                            walking_time_text = response.routes[0].legs[0].steps[y].duration['text'];
                            walking_time_value = response.routes[0].legs[0].steps[y].duration['value'];

                            route_dict['step_distance'] = step_distance;
                            route_dict['walking_time_text'] = walking_time_text;
                            route_dict['walking_time_value'] = walking_time_value;
                            route_dict['transit_type'] = Transit_Type;

                        }

                        if (Transit_Type === "TRANSIT") {

                            // tripCO2Details(response.routes[0].legs[0].distance.value / 1000)

                            arrival_stop = []
                            RouteShortname = [];
                            start_stop_lat_lon = [];
                            end_stop_lat_lon = [];
                            transit_departure_time = []

                            arrival_stop = response.routes[0].legs[0].steps[y].transit.arrival_stop['name'];
                            step_distance = response.routes[0].legs[0].steps[y].distance['text'];
                            RouteShortname = response.routes[0].legs[0].steps[y].transit.line.short_name;
                            transit_departure_time = response.routes[0].legs[0].steps[y].transit.departure_time['text'];
                            start_stop_lat_lon = response.routes[0].legs[0].steps[y].start_location.lat() + ',' + response.routes[0].legs[0].steps[y].start_location.lng();
                            end_stop_lat_lon = response.routes[0].legs[0].steps[y].end_location.lat() + ',' + response.routes[0].legs[0].steps[y].end_location.lng();
                            Google_Journey_time = response.routes[0].legs[0].steps[y].duration['value'];

                            route_dict['arrival_stop'] = arrival_stop;
                            route_dict['step_distance'] = step_distance;
                            route_dict['departure_time'] = departure_time;
                            route_dict['route'] = RouteShortname;
                            route_dict['transit_departure_time'] = transit_departure_time;
                            route_dict['start_stop_lat_lon'] = start_stop_lat_lon;
                            route_dict['end_stop_lat_lon'] = end_stop_lat_lon;
                            route_dict['transit_type'] = Transit_Type;
                            route_dict['Google_Journey_time'] = Google_Journey_time;
                        }
                        steps_array.push(route_dict);
                    }
                    console.log(response)
                    console.log(steps_array)

                } else {
                    window.alert("Directions request failed due to " + status);
                }
                Journey_Steps = JSON.stringify(steps_array);
            }
        )
        this.directionsService.route(
            {
                origin: {placeId: this.originPlaceId},
                destination: {placeId: this.destinationPlaceId},
                travelMode: 'DRIVING',
            },

            (response, status) => {
                //passing response to the populator function to update html divs
                drivingComparatorInfoPopulator(response.routes[0].legs[0].duration.value, response.routes[0].legs[0].distance.value);
                if (status === "OK") {


                } else {
                    window.alert("Directions request failed due to " + status);
                }
            }
        )

        this.directionsService.route(
            {
                origin: {placeId: this.originPlaceId},
                destination: {placeId: this.destinationPlaceId},
                travelMode: 'BICYCLING',
            },

            (response, status) => {
                //passing response to the populator function to update html divs
                cyclingComparatorInfoPopulator(response.routes[0].legs[0].duration.value, response.routes[0].legs[0].distance.value);
                if (status === "OK") {


                } else {
                    window.alert("Directions request failed due to " + status);
                }
            }
        )

        this.directionsService.route(
            {
                origin: {placeId: this.originPlaceId},
                destination: {placeId: this.destinationPlaceId},
                travelMode: 'WALKING',
            },

            (response, status) => {
                if (status === "OK") {
                    walkingComparatorInfoPopulator(response.routes[0].legs[0].duration.value, response.routes[0].legs[0].distance.value);


                } else {
                    window.alert("Directions request failed due to " + status);
                }
            }
        )
        displayTransportComparator();
    }
}