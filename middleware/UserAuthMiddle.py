from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self, request):
        if request.path == '/app/addform/':
            return None
        try:
            request.session['userid']
        except KeyError:
            try:
                token = request.COOKIES['token']
            except KeyError:
                if request.path == '/app/login/':
                    return None
                else:
                    return redirect(reverse('app:login'))
            else:
                try:
                    userid = cache.get(token)
                except UnboundLocalError:
                    if request.path == '/app/login/':
                        return None
                    else:
                        return redirect(reverse('app:login'))
                else:
                    request.session['userid'] = userid
