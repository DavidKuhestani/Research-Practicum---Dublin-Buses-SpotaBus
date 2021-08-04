from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from dublinbusapplication.predictive_model.get_prediction import *
from .models import Stop, Bikes, FavouriteJourney


def index(request):
    stops = Stop.objects.all().values()
    render_bike_stations = Bikes.objects.all().values()
    fave_routes = FavouriteJourney.objects.all().values()

    return render(request, 'index.html', {'stops': list(stops), 'stations': list(render_bike_stations),
                                          'fave_routes': list(fave_routes)})


# ajax_posting function
def predict(request):
    try:
        stop = Stop.objects.all().values()
        journey_steps = json.loads(request.POST["steps_array"])

        print(journey_steps)

        final_estimate = []
        for i in range(0, len(journey_steps)):
            if journey_steps[i]["transit_type"] == "TRANSIT":
                start_stop_lat_lon = (journey_steps[i]['start_stop_lat_lon'])
                end_stop_lat_lon = (journey_steps[i]['end_stop_lat_lon'])
                route = (journey_steps[i]['route'])

                start_stop_lat_lon_split = start_stop_lat_lon.split(",")
                end_stop_lat_lon_split = end_stop_lat_lon.split(",")

                data_list = []
                for item in stop:
                    adict = {'id': item['stop_id'], 'lat': item['stop_lat'], 'lon': item['stop_lon']}
                    data_list.append(adict)

                start_stop = {'lat': float(start_stop_lat_lon_split[0]), 'lon': float(start_stop_lat_lon_split[1])}
                end_stop = {'lat': float(end_stop_lat_lon_split[0]), 'lon': float(end_stop_lat_lon_split[1])}

                closest_start_id = (closest(data_list, start_stop))
                closest_end_id = (closest(data_list, end_stop))

                start_id_full = closest_start_id['id']
                end_id_full = closest_end_id['id']

                if request.is_ajax():
                    hour = int(float(request.POST.get('hour')))
                    day = int(float(request.POST.get('day')))
                    month = int(float(request.POST.get('month')))
                    wind_speed = int(float(request.POST.get('wind_speed')))
                    humidity = int(float(request.POST.get('humidity')))
                    temp = int(float(request.POST.get('temp')) - 273)
                    weather_main = (request.POST.get('weather_main'))

                    # converting the start and stop ids to the required format
                    start_stop_id = int(start_id_full[len(start_id_full) - 5:])
                    end_stop_id = int(end_id_full[len(end_id_full) - 5:])

                    print("ids", start_stop_id, end_stop_id)
                    stops_dict = get_route(stops_sequence, route)

                    result = int(
                        prediction(route, hour, day, month, start_stop_id, end_stop_id, wind_speed, temp, humidity,
                                   weather_main,
                                   stops_dict))

                    final_estimate.append(result)

        return JsonResponse(sum(final_estimate), safe=False)
        # return response as JSON

    except Exception as e:
        print(e)
        journey_steps = json.loads(request.POST["steps_array"])
        google_time_result = []

        for item in journey_steps:
            if item["transit_type"] == "TRANSIT":
                google_time = int(item["Google_Journey_time"] / 60)
                google_time_result.append(google_time)

        return JsonResponse(sum(google_time_result), safe=False)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# @login_required
def add_favourite_route(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    print('request is', request)
    if request.method == 'POST':
        if request.POST.get('users_origin_stop') and request.POST.get('users_dest_stop'):
            # user = User.objects.get(id=request.session['_auth_user_id'])
            fav_journey = FavouriteJourney()
            fav_journey.users_origin_stop = request.POST.get('users_origin_stop')
            fav_journey.users_dest_stop = request.POST.get('users_dest_stop')
            fav_journey.user_id = request.session['_auth_user_id']
            # fav_journey.user = request.user.username
            fav_journey.save()

        return JsonResponse({'message': 'Successfully saved you beautiful human being'})


def userPage(request):
    return render(request, 'userpage.html')

# stop = Stop.objects.all.values()
# v = {'lat': start_stop_lat, 'lon': start_stop_lon}
#
# print(JsonResponse(closest(stop, v)))
