__author__ = 'Vadim Melnyk'
import requests
import webbrowser
import urllib
import json


def check_code_existence(code):
    import os.path
    if os.path.isfile(code+'.txt'):
        file = open(code+'.txt','r')
        code = file.read()
        return code
    else:
        return False


def save_code(code, value):
    try:
        file = open(code+'.txt', 'w')
        file.write(value)
        file.close()
        return True
    except Exception, e:
        print "Error saving " + code
        print e
        return False


class OneDriveConnect():

    #Connection necessary values
    client_id = ''
    client_secret = ''
    scope = ''
    response_type = ''
    redirect_uri = ''

    #Access Code
    access_code = ''
    #Tokens
    access_token_value = ''
    refresh_token_value = ''


    def __init__(self, client_id, client_secret, scope, response_type, redirect_uri):

        self.client_id = str(client_id)
        self.client_secret = str(client_secret)
        self.scope = str(scope)
        self.response_type = str(response_type)
        self.redirect_uri = str(redirect_uri)
        self.init_saved_values()

    def init_saved_values(self):
        code = check_code_existence('access_code')
        if code:
            self.access_code = code
        else:
            self.obtain_access_code()
            return

        code = check_code_existence('access_token')
        if code:
            self.access_token_value = code
        else:
            self.obtain_access_token()
            return

        code = check_code_existence('refresh_token')
        if code:
            self.refresh_token_value = code
        else:
            self.refresh_token()
            return

    def obtain_access_code(self):
        code = check_code_existence('access_code')
        if code != False:
            self.access_code = code
        else:
            url = 'https://login.live.com/oauth20_authorize.srf'
            payload = {'client_id': self.client_id,
                       'scope': self.scope,
                       'response_type': self.response_type,
                       'redirect_uri': self.redirect_uri}
            r = requests.get(url, params=payload, allow_redirects=True)
            webbrowser.open_new(r.url)
            result = raw_input("Enter the access code:")
            if len(result) != 0:
                self.access_code = result
                save_result = save_code('access_code', result)
                if not save_result:
                    exit(1)
        print self.access_code

    def obtain_access_token(self):
        code = check_code_existence('access_token')
        if code:
            self.access_token_value = code
        else:
            url = 'https://login.live.com/oauth20_token.srf'
            params = urllib.urlencode({
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'client_secret': self.client_secret,
                'code': self.access_code,
                'grant_type': 'authorization_code'
            })
            response = urllib.urlopen(url, params).read()
            data = json.loads(response)
            print data
            self.access_token_value = data['access_token']
            self.refresh_token_value = data['refresh_token']
            save_result_access_token = save_code('access_token', data['access_token'])
            if not save_result_access_token:
                exit(1)
            save_result_refresh_token = save_code('refresh_token', data['refresh_token'])
            if not save_result_refresh_token:
                exit(1)

            #logs
            # print 'token_type: ' + data['token_type']
            # print 'expires_in: ' + str(data['expires_in'])
            # print 'scope: ' + data['scope']
            # print 'access_token: ' + data['access_token']
            # print 'refresh_token: ' + data['refresh_token']

    def refresh_token(self):
        url = 'https://login.live.com/oauth20_token.srf'
        params = urllib.urlencode({
        'client_id': self.client_id,
        'redirect_uri': self.redirect_uri,
        'client_secret': self.client_secret,
        'refresh_token': self.refresh_token_value,
        'grant_type': 'refresh_token'
        })

        response = urllib.urlopen(url, params).read()
        data = json.loads(response)
        #logs
        # print 'token_type: ' + data['token_type']
        # print 'expires_in: ' + str(data['expires_in'])
        # print 'scope: ' + data['scope']
        # print 'access_token: ' + data['access_token']
        # print 'refresh_token: ' + data['refresh_token']

        self.access_token_value = data['access_token']
        self.refresh_token_value = data['refresh_token']
