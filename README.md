[![Build Status](http://img.shields.io/travis/emotionLoop/visualCaptcha-django.svg)](http://travis-ci.org/emotionLoop/visualCaptcha-django)
[![Coverage Status](https://coveralls.io/repos/emotionLoop/visualCaptcha-django/badge.svg)](https://coveralls.io/r/emotionLoop/visualCaptcha-django)
[![Codacy](https://www.codacy.com/project/badge/de63c55be5024f58804ede55c7f2b0e8)](https://www.codacy.com/app/bruno-bernardino/visualCaptcha-django)
[![Code Climate](https://codeclimate.com/github/emotionLoop/visualCaptcha-django/badges/gpa.svg)](https://codeclimate.com/github/emotionLoop/visualCaptcha-django)

# visualCaptcha-django

Django sample for visualCaptcha.

A demo/sample Django app that uses the [visualcaptcha python package](https://github.com/emotionLoop/visualCaptcha-python) and the [visualcaptcha vanilla js bower package](https://github.com/emotionLoop/visualCaptcha-frontend-vanilla), as a proof-of-concept for how to integrate it with your Django project.


## Installation 

You need Python installed with pip.
```
pip install -r requirements.txt
```


## Run server

To start the server on port, for example, 8282, run the following command:
```
python manage.py runserver 0.0.0.0:8282
```

## Run tests

If you want to run the unit tests, use the following command:
```
python manage.py test
```


## API

visualCaptcha, since 5.0, uses an API for increased security and to become back-end-agnostic (that's why you can easily plug-in a Vanilla JS, AngularJS, or jQuery front-end without changing anything).

It expects the following routes to exist, which we've put in this sample.

You are expected to have these routes in your implementation, but you can change them in visualCaptcha's front-end config.

### GET `/start/:howmany`

This route will be the first route called by the front-end, which will generate and store session data.

Parameters:

- `howmany` is required, the number of images to generate.

### GET `/image/:index`

This route will be called for each image, to get it and show it, by index.

Parameters:

- `index` is required, the index of the image you want to get.

### GET `/audio(/:type)`

This route will be called for the audio file, to get it and play it, either the mp3 or ogg file.

Parameters:

- `type` is optional, the audio file format defaults to `mp3`, but can also be `ogg`.

### POST `/try` 

This is just a sample route, where we post the form to, and where the visualCaptcha validation takes place.


## License

MIT. Check the [LICENSE](LICENSE) file.
