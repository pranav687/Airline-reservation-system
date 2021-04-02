from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . models import Announcement,Flights,Passengers
from datetime import date

def index(request):
    ancmnts = Announcement.objects.all()
    return render(request, 'index.html',{'ancmnts' : ancmnts} )

def search(request):       
    orgn = request.POST.get('origin','')
    dest = request.POST.get('destination','')
    depdate = request.POST.get('date','')
    numseats = int(request.POST.get('required_seats',''))
    flights = Flights.objects.filter(source__iexact=orgn).filter(destination__iexact=dest).filter(departure_date__gte=date.today()).filter(departure_date=depdate).filter(available_seats__gte=numseats)
    dict2=dict()
    dict2['flights']=flights
    dict2['seats']=numseats
    return render(request, 'available_flights.html' , dict2)

def book_flight(request):
    global dict1
    if request.method=="GET":
        fid = int(request.GET["id"])
        num = int(request.GET["sits"])
        print(fid)
        print(num)
        flight_obj = Flights.objects.get(pk=fid)           
        passenger_obj = Passengers.objects.filter(flights=flight_obj)
        rate = flight_obj.price

        dict1 = dict()
        dict1['num'] = num
        dict1['num_list'] = [i for i in range(1,num+1) ]
        dict1['flight_obj'] = flight_obj
        dict1['total'] = int(num)*int(rate)
        dict1['rate'] = rate
        dict1['map'] = {        # map for seat selection 
        'raw1':[1,2,3] ,
        'raw2':[4,5,6] ,
        'raw3':[7,8,9] ,
        'raw4':[10,11,12] ,
        'raw5':[13,14,15] ,
        'raw6':[16,17,18] ,
        'raw7':[19,20,21] ,
        'raw8':[22,23,24] ,
        'raw9':[25,26,27] ,
        'raw10':[28,29,30] ,       
         }

        unavailable_list = []       # generating list for unavailable seats (i.e : already booked seats)
        for tik in passenger_obj :
            unavailable_list.append(tik.seat_num) 
        dict1['unavailable_list'] = unavailable_list

    if request.method == 'POST':
        action = request.POST['act']

        if(action == "book"):            
            dict1['passen_names'] = request.POST.getlist('p_name')
            dict1['passen_ages'] = request.POST.getlist('p_age')
            dict1['passen_seats'] = request.POST.getlist('p_seat[]')
            return render(request,'pay.html',dict1)  
            
            

        if(action=="pay"):
            print(dict1)
            flight_obj = dict1['flight_obj']
            num =  dict1['num']
            rate =  dict1['rate']
            if int(flight_obj.available_seats) > int(num):
                for i in range(0,num):
                    nm = dict1['passen_names'][i]
                    age  = dict1['passen_ages'][i]
                    sit = dict1['passen_seats'][i]
                    passenger = Passengers.objects.create(flights=flight_obj,passenger_name=nm,passenger_age=age,seat_num=sit)

                flight_obj.available_seats = int(flight_obj.available_seats) - int(num)
                flight_obj.save()
                return render(request, 'done.html', dict1)
            
            else:
                return HttpResponseRedirect('/')

    return render(request,'available_seats.html',dict1)  



