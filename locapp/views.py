from django.shortcuts import render, HttpResponse, redirect
from .models import Destination, Tourist, DestinationDetails, DestinationMetaDetails
from locapp.forms import DestinationForm, TouristForm
from geopy.geocoders import Nominatim
from .utils import get_center_coordinates, get_zoom
from geopy.distance import geodesic
from django.contrib.auth import logout
import geocoder
import folium

# Create your views here.
def soclogin(request):
    return render(request, 'locapp/login.html')


def DestinationView(request):

    uname = request.user.username
    
    geolocator = Nominatim(user_agent='syedarfa')
    
    touristloc = geocoder.ip('me')
    # print("yahan", ip)
    # print("or yahan", ip.latlng)
    tourist_lat, tourist_lon = touristloc.latlng
    print("yahan", tourist_lat)
    touristLocation = (tourist_lat, tourist_lon)
    #to get the location details of the tourist
    touristlocdetails = geolocator.reverse(str(tourist_lat) + ',' + str(tourist_lon))
    touristaddress = touristlocdetails.raw['address']
    # print(touristaddress)
    tourist_state = touristaddress.get('state', '')
    tourist_country = touristaddress.get('country', '')
    tourist_locdetails = tourist_state + tourist_country 
    # print('Details are ' + tourist_locdetails)

    #Map using folium library
    #the map will point to the location of tourist
    mapobj = folium.Map(width=800, height=650, location=touristLocation, zoom_start=15)
    #adding marker at tourist location
    folium.Marker([tourist_lat, tourist_lon], tooltip= 'Click to get the name of city', popup=touristloc,
                        icon=folium.Icon(color='green')).add_to(mapobj)

    if request.method == "POST":
        fm = DestinationForm(request.POST)
        # tfm = TouristForm(request.POST)
        btn_City=""
        btn_City = request.POST.get('city')
        if fm.is_valid():
            print("Yeh dekho", tourist_lat)
            fmwait = fm.save(commit=False)
            destination_ = request.POST.get('destination')
            city=destination_
            dest_details = DestinationDetails.objects.filter(destination_name__icontains = city)
            for m in dest_details:
                destination_=m.destination_name

            dest_meta_details = DestinationMetaDetails.objects.filter(meta_destination__in = DestinationDetails.objects.filter(destination_name = destination_))

            destination = geolocator.geocode(destination_)
            # print(destination.address)
            # print(destination.latitude)
            dest_lat = destination.latitude
            # print(destination.longitude)
            dest_long = destination.longitude

            destinationLocation = (dest_lat, dest_long)

            #Now calculating the distance between tourist location and distance location
            distance = geodesic(touristLocation, destinationLocation).km

            #Now to plot the route between tourist location and the destination
            mapobj = folium.Map(width=900, height=550, location=get_center_coordinates(tourist_lat, tourist_lon,dest_lat,dest_long),
                                zoom_start=get_zoom(distance))
            #TouristLocation
            folium.Marker([tourist_lat, tourist_lon], tooltip= 'Click to get the name of city', popup=touristloc,
                        icon=folium.Icon(color='green')).add_to(mapobj)
            #TouristDestination
            folium.Marker([dest_lat, dest_long], tooltip= 'Click to get the name of city', popup=destination,
                        icon=folium.Icon(color='blue')).add_to(mapobj)
            #Now we will draw line between touristlocation and tourist destination
            line = folium.PolyLine(locations=[touristLocation, destinationLocation], weight=2.5, color='red')
            #adding the line to our map now
            mapobj.add_child(line)


            # fmwait.username = uname
            # fmwait.user_location = touristloc
            fmwait.distance = distance
            fmwait.destination = destination_

            # tfm.tourist_name = uname
            # tfm.tourist_latitude = tourist_lat
            # tfm.tourist_longitude = tourist_lon
            # tfm.tourist_location = tourist_locdetails

            # tfm.save()
            fmwait.save()
            touristobj = Tourist(tourist_name=uname,
            tourist_latitude= tourist_lat, tourist_longitude=tourist_lon, tourist_location = tourist_locdetails)
            touristobj.save()

            # for locdetail in dest_meta_details:
            #     meta_dest_loc = geolocator.geocode(locdetail.meta_destination_name)
            #     print("Jagah: ", locdetail.meta_destination_name," iski latitude value: ", meta_dest_loc.latitude, " or longitude value: ", meta_dest_loc.longitude)
            #     meta_dest_loc_val = (meta_dest_loc.latitude, meta_dest_loc.longitude)
            #     meta_dest_map = folium.Map(width=150, height=150,location=meta_dest_loc_val, zoom_start=15)
            #     folium.Marker([meta_dest_loc.latitude,meta_dest_loc.longitude], tooltip= 'Click to get the name of city', popup = None,
            #             icon=folium.Icon(color='green')).add_to(meta_dest_map)

            mapobj = mapobj._repr_html_()
            # for detail in dest_meta_details:
            #     print(detail.meta_destination_name)
            fm = DestinationForm()
            return render(request,'locapp/locationdetails.html', context={'form':fm, 'map': mapobj,
                    'username':uname,'dest_details': dest_details, 'distance': distance, 'dest_meta_details':dest_meta_details,})

    #rendering foliummap in template    
    mapobj = mapobj._repr_html_()
    fm = DestinationForm()
    obj = DestinationDetails.objects.all()
    sl=[1,2,3]
    return render(request,'locapp/index.html', context={'form':fm, 'map': mapobj,'username':uname,'sl':sl,'obj':obj})



def logoutuser(request):
    logout(request)
    return redirect('/')


def loc_meta_view(request, pk):
    geolocator = Nominatim(user_agent='syedarfa')
    dest_meta_details = DestinationMetaDetails.objects.get(id = pk)
    print("ye lo details", dest_meta_details.meta_destination_name)
    if dest_meta_details:
        meta_dest_loc = geolocator.geocode(dest_meta_details.meta_destination_name + " " + dest_meta_details.meta_destination.destination_name)
        print("Jagah: ", dest_meta_details.meta_destination_name," iski latitude value: ", meta_dest_loc.latitude,
             " or longitude value: ", meta_dest_loc.longitude)
        meta_dest_loc_val = (meta_dest_loc.latitude, meta_dest_loc.longitude)
        meta_dest_map = folium.Map(width=400, height=300,location=meta_dest_loc_val, zoom_start=12)
        folium.Marker([meta_dest_loc.latitude,meta_dest_loc.longitude], tooltip= 'Click to get the name of city', popup = None,
                            icon=folium.Icon(color='green')).add_to(meta_dest_map)


        meta_dest_map = meta_dest_map._repr_html_()
        return render(request, 'locapp/meta_dest_map.html', context={'map': meta_dest_map, 'dest_meta_details': dest_meta_details})

    return HttpResponse("Hello Arfa")