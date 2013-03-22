# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
from BeautifulSoup import BeautifulSoup
from oauth_tokens.base import BaseAccessToken
import cgi
import logging
import requests

log = logging.getLogger('oauth_tokens')

class FacebookAccessToken(BaseAccessToken):

    provider = 'facebook'
    authenticate_url = 'https://www.facebook.com/dialog/oauth'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    redirect_uri = 'http://socialcommunications.ru/404'
    response_decoder = lambda self,x: dict(cgi.parse_qsl(x))
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/536.11 (KHTML, like Gecko) Ubuntu/12.04 Chromium/20.0.1132.47 Chrome/20.0.1132.47 Safari/536.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'www.facebook.com',
    }

    def parse_auth_form(self, page_content):
        '''
        Parse page with auth form and return tuple with (method, form action, form submit parameters)
        '''
        content = BeautifulSoup(page_content)

        form = content.find('form')
        if not form:
            raise Exception('There is no any form in response')

        data = {}
        for input in form.findAll('input'):
            if input.get('name'):
                data[input.get('name')] = input.get('value')

        data['email'] = self.username
        data['pass'] = self.password

        return (form.get('method').lower(), form.get('action'), data)

    def parse_permissions_form(self, page_content):
        '''
        Parse page with permissions form and return tuple with (method, form action, form submit parameters)
        '''
        content = BeautifulSoup(page_content)

        form = content.find('form', {'id': 'uiserver_form'})
        if not form:
            raise Exception('There is no any form in response')

        data = {}
        for input in form.findAll('input'):
            if input.get('name'):
                data[input.get('name')] = input.get('value')

        del data['cancel_clicked']

        return (form.get('method').lower(), form.get('action'), data)

    def authorize(self):
        '''
        Handling specific errors
        '''
        response = super(FacebookAccessToken, self).authorize()

        if 'You are trying too often' in response.content:
            # TODO: fix it
            log.error("Vkontakte authorization request returns error 'You are trying too often'")
            raise Exception("Vkontakte authorization request returns error 'You are trying too often'")
        if 'Cookies Required' in response.content:
            response = requests.get('http://facebook.com')
            self.cookies = response.cookies
            self.authorize()
        if 'API Error Code: 191' in response.content:
            raise ImproperlyConfigured("You must specify URL '%s' in your facebook application settings" % self.redirect_uri)

        if 'Your account is temporarily locked.' in response.content:
            raise ImproperlyConfigured("Facebook errored 'Your account is temporarily locked.'. Try to login via web browser")

        return response