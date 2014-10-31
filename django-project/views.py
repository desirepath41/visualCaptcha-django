from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, redirect

from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import BaseRenderer
from rest_framework.parsers import JSONParser

from visualcaptcha import Captcha, Session

def index(request):
    return render_to_response('index.html')

def start(request, howMany):
    visualCaptcha = Captcha( Session(request.session) )

    visualCaptcha.generate( howMany )
    jsonFrontendData = JSONRenderer().render( visualCaptcha.getFrontendData() )
    response = HttpResponse( content = jsonFrontendData )
    response['Access-Control-Allow-Origin'] = '*'

    return response

def getImage(request, index):
    visualCaptcha = Captcha( Session(request.session) )

    headers = {}
    result = visualCaptcha.streamImage( headers, index, request.GET.get('retina') )

    if ( result == False ):
        return HttpResponse( result, headers, 404 )

    return HttpResponse( result, headers )

def getAudio(request, audioType = 'mp3'):
    visualCaptcha = Captcha( Session(request.session) )

    headers = {}
    result = visualCaptcha.streamAudio( headers, audioType )

    if ( result == False ):
        return HttpResponse( result, headers, 404 )

    return HttpResponse( result, headers )

@csrf_exempt
def trySubmission(request):
    visualCaptcha = Captcha( Session(request.session) )

    frontendData = visualCaptcha.getFrontendData();

    # If an image field name was submitted, try to validate it
    if ( request.POST.get(frontendData['imageFieldName'],None) != None ):
        if ( visualCaptcha.validateImage(request.POST[frontendData['imageFieldName'] ]) ):
            response = HttpResponse(status = 200)
            return redirect( '/?status=validImage' )
        else:
            response = HttpResponse(status = 403)
            return redirect( '/?status=failedImage' )
    elif ( request.POST.get(frontendData['audioFieldName'],None) != None ):
        # We set lowercase to allow case-insensitivity, but it's actually optional
        if ( visualCaptcha.validateAudio(request.POST[frontendData['audioFieldName']].lower()) ):
            response = HttpResponse(status = 200)
            return redirect( '/?status=validAudio' )
        else:
            response = HttpResponse(status = 403)
            return redirect( '/?status=failedAudio' )
    else:
        response = HttpResponse(status = 500)
        return redirect( '/?status=failedPost' )

    return response
