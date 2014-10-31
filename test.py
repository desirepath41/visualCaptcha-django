import os
import sys
import unittest
import json

from django.test.client import Client

client = {}
frontendData = {}

# Runs before each test
def globalSetup():
    global client

    # Set a new "client" every time
    client = Client()

# Test NonExisting routes
class NonExistingTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return 404 error when calling a non-existing route
    def test_unexisting_test_route( self ):
        response = client.get( '/test' )
        self.assertEqual( response.status_code, 404 )

# Test Start routes
class StartTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

    # Should return 404 error when calling /start without the number of requested images
    def test_start_no_number_of_images( self ):
        response = client.get( '/start' )

        self.assertEqual( response.status_code, 404 )

    # Should return 200 when calling /start/5, the image and audio field names, image name, and image values
    def test_start_correct( self ):
        global frontendData

        response = client.get( '/start/5' )

        self.assertEqual( response.status_code, 200 )

        data = json.loads( response.content )

        self.assertIsNotNone( data['imageName'] )
        self.assertIsNotNone( data['imageFieldName'] )
        self.assertIsNotNone( data['audioFieldName'] )
        self.assertIsNotNone( data['values'] )

        self.assertTrue( len(data['imageName']) > 0 )
        self.assertTrue( len(data['imageFieldName']) > 0 )
        self.assertTrue( len(data['audioFieldName']) > 0 )

        self.assertIsInstance( data['values'], list )
        self.assertTrue( len(data['values']) > 0 )

        self.assertIsNotNone( data['values'][0] )

# Test Audio routes
class AudioTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

        # This request generates a valid visualCaptcha session
        response = client.get( '/start/5' )

    # Should return an mp3 audio file
    def test_audio_mp3( self ):
        response = client.get( '/audio' )

        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response['Content-Type'], "{'Expires': 0, 'Content-Type': 'audio/mpeg', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache, no-store, must-revalidate'}" )

    # Should return an ogg audio file
    def test_audio_ogg( self ):
        response = client.get( '/audio/ogg' )

        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response['Content-Type'], "{'Expires': 0, 'Content-Type': 'audio/ogg', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache, no-store, must-revalidate'}" )

# Test Image routes
class ImageTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        globalSetup()

        # This request generates a valid visualCaptcha session
        response = client.get( '/start/5' )

    # Should return 404 error when calling /image without the index number
    def test_image_no_index( self ):
        response = client.get( '/image' )
        self.assertEqual( response.status_code, 404 )

    # Should return an image file
    def test_image_zero( self ):
        response = client.get( '/image/0' )

        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response['Content-Type'], "{'Expires': 0, 'Content-Type': 'image/png', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache, no-store, must-revalidate'}" )

    # Should return another image file
    def test_image_one( self ):
        response = client.get( '/image/1' )

        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response['Content-Type'], "{'Expires': 0, 'Content-Type': 'image/png', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache, no-store, must-revalidate'}" )

    # Should return a retina image file
    def test_image_retina( self ):
        response = client.get( '/image/1?retina=1' )

        self.assertEqual( response.status_code, 200 )
        self.assertEqual( response['Content-Type'], "{'Expires': 0, 'Content-Type': 'image/png', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache, no-store, must-revalidate'}" )

    # Should return 404 error when calling /image with a non-existing index_number
    def test_image_invalid_index( self ):
        response = client.get( '/image/100' )
        self.assertEqual( response.status_code, 404 )

# Test Try routes
class TryTest( unittest.TestCase ):

    # Runs before each test in this group
    def setUp( self ):
        global frontendData

        globalSetup()

        # This request generates a valid visualCaptcha session
        response = client.get( '/start/5' )

        # We need to store this to use it later
        frontendData = json.loads( response.content )

    # Should redirect to /?status=failedPost when no data is posted
    def test_no_data( self ):
        response = client.post( '/try', {} )

        self.assertEqual( response.status_code, 302 )
        self.assertEqual( response.url, 'http://testserver/?status=failedPost' )

    # Should redirect to /?status=failedImage when captcha image fails
    def test_invalid_image( self ):
        response = client.post( '/try', { frontendData['imageFieldName']: 'definitely-wrong-image-answer' } )

        self.assertEqual( response.status_code, 302 )
        self.assertEqual( response.url, 'http://testserver/?status=failedImage' )

    # Should redirect to /?status=failedAudio when captcha image fails
    def test_invalid_audio( self ):
        response = client.post( '/try', { frontendData['audioFieldName']: 'definitely-wrong-audio-answer' } )

        self.assertEqual( response.status_code, 302 )
        self.assertEqual( response.url, 'http://testserver/?status=failedAudio' )

if __name__ == '__main__':
    print "Running unit tests"
    unittest.main()
