from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.http import JsonResponse


def home(request):

    # Define the data to be sent
    data = {
        'name': 'Nuha',
        'description': '20'
    }

    # Define the URL of your Django API endpoint
    url = 'http://localhost:8000/api/orm'

    # Send a POST request with the data
    # response = requests.post(url, json=data)

    #Check the response status code
    # if response.status_code == 201:
    #     print('Data sent successfully')
    # else:
    #     print('Error sending data:', response.status_code)

    # Sending a GET request to the external API
    response = requests.get(url,params=data)
    print(response.content)


    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # If successful, you can process the response data
        data = response.json()  # Assuming the response is JSON
        # Do something with the data
        return JsonResponse(data, safe=False)
    else:
        # If request was not successful, handle the error
        return JsonResponse({'error': 'Failed to retrieve data from external API'}, status=500)

    return HttpResponse("Hello, this is the home page!")


