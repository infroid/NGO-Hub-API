from django.http import JsonResponse

# Create your views here.


def index(request):
    response = JsonResponse(
        {
            'version': '1',
            'name': 'NGO-Hub-API',
            'purpose': 'Dummy Data for Testing Mobile Application'
        }
    )
    return response
