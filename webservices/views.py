from django.views.decorators.csrf import csrf_exempt
from .models import Author, Story
from django.shortcuts import get_object_or_404
from django.http import QueryDict, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime
import json

### NEWS API SERVICES ###

# Logs the user in 
@csrf_exempt
def HandleLoginRequest(request):
    if (request.method == 'POST'):
        if (request.content_type == 'application/x-www-form-urlencoded'):
            body = request.body
            decoded_body = body.decode('utf-8')

            try:
                parsed_data = QueryDict(decoded_body)
                username = parsed_data['username']
                password = parsed_data['password']

            except (ValueError, KeyError):
                response = HttpResponse(
                        "Malformed request.",
                        content_type="text/plain",
                        status=400,
                        reason="Bad Request")
                return response
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                response = HttpResponse(
                        "Welcome! You are logged in.",
                        content_type="text/plain",
                        status=200, 
                        reason="OK")
                return response
            else:
                response = HttpResponse(
                        "Incorrect credentials.",
                        content_type="text/plain",
                        status=401,
                        reason="Unauthorized")
                return response
        else:
            response = HttpResponse(
                "Invalid content encoding.",
                content_type="text/plain",
                status=415,
                reason="Unsupported Media Type")
            return response    
    else:
        response = HttpResponse(
            "Invalid request method.",
            content_type="text/plain",
            status=405,
            reason="Method Not Allowed")
        return response

# Logs the user out
@csrf_exempt
def HandleLogoutRequest(request):
    if (request.method == 'POST'):
        if request.POST:
            response = HttpResponse(
                    "Malformed request.",
                    content_type="text/plain",
                    status=400,
                    reason="Bad Request")
            return response
        else:
            if request.user.is_authenticated:
                logout(request)
                response = HttpResponse(
                         "Logged out.",
                         content_type="text/plain",
                         status=200,
                         reason="OK")
                return response
            else:
                response = HttpResponse(
                "User is not logged in.",
                content_type="text/plain",
                status=400,
                reason="Bad Request")
                return response
    else:
        response = HttpResponse(
            "Invalid request method.",
            content_type="text/plain",
            status=405,
            reason="Method Not Allowed")
        return response
    
# Handles posting and requesting news stories
@csrf_exempt
def HandleStoryRequests(request):
    ## POST STORY REQUESTS
    if (request.method == 'POST'):
       if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                response = HttpResponse(
                    "Data not in JSON format.",
                    content_type="text/plain",
                    status=503,
                    reason="Service Unavailable")
                return response

            try:
                author= Author.objects.get(user=request.user)
            except Author.DoesNotExist:
                response = HttpResponse(
                    "Author does not exist.",
                    content_type="text/plain",
                    status=503,
                    reason="Service Unavailable")
                return response

            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')

            if ((headline != "") and
                (category == "pol" or category == "art" or category == "tech" or category == "trivia") and
                (region == "uk" or region == "eu" or region == "w") and
                (details != "")):
                story = Story(
                    headline=headline,
                    category=category,
                    region=region,
                    details=details,
                    author=author,
                )
                story.save()
                response = HttpResponse(
                    "Posted story.",
                    content_type="text/plain",
                    status=200,
                    reason="OK")
                return response
            else:
                response = HttpResponse(
                    "Missing/Incorrect data.",
                    content_type="text/plain",
                    status=503,
                    reason="Service Unavailable")
                return response

       else:
            response = HttpResponse(
                "User is not logged in.",
                content_type="text/plain",
                status=503,
                reason="Service Unavailable")
            return response

    ## GET STORY REQUESTS
    else:
        if (request.method == 'GET'):
            if (request.content_type == 'application/x-www-form-urlencoded'):

                 try:
                    params = request.GET.dict()
                 except (ValueError, KeyError):
                     response = HttpResponse(
                             "Malformed request.",
                             content_type="text/plain",
                             status=400,
                             reason="Bad Request")
                     return response

                 filters = {}

                 if params['story_cat'] != '*':
                    filters['category'] = params['story_cat']
                 if params['story_region'] != '*':
                    filters['region'] = params['story_region']
                 if params['story_date'] != '*':
                    try:
                        filters['datetime__gte'] = datetime.strptime(params['story_date'], "%Y-%m-%d")
                    except ValueError:
                        response = HttpResponse(
                             "Invalid date format.",
                             content_type="text/plain",
                             status=400,
                             reason="Bad Request")
                        return response

                 stories_data = Story.objects.filter(**filters)

                 if stories_data.exists():
                    stories = []
                    for story in stories_data:
                        story_dict = {
                            "key": str(story.pk),
                            "headline": story.headline,
                            "story_cat": story.category,
                            "story_region": story.region,
                            "author": story.author.name,
                            "story_date": story.datetime.strftime("%Y-%m-%d"),
                            "story_details": story.details,
                        }
                        stories.append(story_dict)


                    return JsonResponse({"stories":stories}, safe=False, status=200)

                 else:
                     response = HttpResponse(
                             "No stories available.",
                             content_type="text/plain",
                             status=404,
                             reason="Not Found")
                     return response

            else:
                response = HttpResponse(
                    "Invalid content encoding.",
                    content_type="text/plain",
                    status=415,
                    reason="Unsupported Media Type")
                return response
        else:
            response = HttpResponse(
                "Invalid request method.",
                content_type="text/plain",
                status=405,
                reason="Method Not Allowed")
            return response

# Deletes a story
@csrf_exempt
def HandleDeleteRequest(request, key):
    if (request.method == 'DELETE'):
        if request.user.is_authenticated:
             try:
                entry = Story.objects.get(pk=key)
             except Story.DoesNotExist:
                    response = HttpResponse(
                    "Invalid key.",
                    content_type="text/plain",
                    status=503,
                    reason="Service Unavailable")
                    return response
    
             entry.delete()
             response = HttpResponse(
                "Story deleted.",
                content_type="text/plain",
                status=200,
                reason="OK")
             return response

        else:
            response = HttpResponse(
                "User is not logged in.",
                content_type="text/plain",
                status=503,
                reason="Service Unavailable")
            return response

    else:
        response = HttpResponse(
            "Invalid request method.",
            content_type="text/plain",
            status=405,
            reason="Method Not Allowed")
        return response

### END OF NEWS API SERVICES ###

# Create your views here.
