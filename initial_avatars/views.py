# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import last_modified
from datetime import date, timedelta
from .generator import GRAVATAR_DEFAULT_SIZE
from .utils import get_avatar_backend
from django.conf import settings
from django.contrib.auth import get_user_model

def last_modified_func(request, id, size=GRAVATAR_DEFAULT_SIZE):
    try:
        u = get_user_model().objects.get(id=id)
    except get_user_model().DoesNotExist:
        return None
    avatar_backend = get_avatar_backend()
    return avatar_backend(u, int(size)).last_modification()

def avatar(request, id, size=GRAVATAR_DEFAULT_SIZE):
    user = get_object_or_404(get_user_model(), id=id)
    avatar_backend = get_avatar_backend()
    url = avatar_backend(user, size=int(size)).get_avatar_url()
    try:
        response = HttpResponseRedirect(url)
        response['Cache-Control'] = 'max-age=2592000'
        response['Expires'] = (date.today() + timedelta(days=31)).strftime('%a, %d %b %Y 20:00:00 GMT')
        return response
    except Exception:
        return HttpResponse('Not Found', status=404)
