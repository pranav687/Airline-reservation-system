from travel.models import Destination
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . models import Destination,Flights,Tickets
from datetime import date

def index(request):
    dests = Destination.objects.all()
    return render(request, 'index.html',{'dests' : dests} )

def search(request):       
    orgn = request.POST.get('origin','')
    dest = request.POST.get('destination','')
    depdate = request.POST.get('date','')
    numseats = int(request.POST.get('num_seats',''))
    flights = Flights.objects.filter(source__iexact=orgn).filter(destination__iexact=dest).filter(departure_date__gte=date.today()).filter(departure_date=depdate).filter(available_seats__gte=numseats)
    dict2=dict()
    dict2['flights']=flights
    dict2['seats']=numseats
    return render(request, 'available_flights.html' , dict2)

def book_flight(request , **kwargs):
    # num = request.GET['numseats']   
    num = kwargs.pop("no_seats")
    # print("hi")
    # print(num)
    #num = 3
    # fid = 16
    fid = kwargs.pop("travel_id") 
    flight_obj = Flights.objects.get(pk=fid)
    rate = flight_obj.price

    dict1 = dict()
    dict1['seats'] = num
    dict1['flight'] = flight_obj
    dict1['total'] = int(num)*int(rate)
    dict1['rate'] = rate

    if request.method == 'POST':
        if int(flight_obj.available_seats) > int(num):
                    flight_obj.available_seats = int(flight_obj.available_seats) - int(num)
                    #flight_obj.collected = int(flight_obj.collected) + int(rate)
                    flight_obj.save()
                    ticket_obj = Tickets.objects.create(flights=flight_obj,num_seats=num,cost=rate)
                    return render(request, 'done.html', dict1)
        else:
                    return HttpResponseRedirect('/')

    return render(request,'pay.html',dict1)   

