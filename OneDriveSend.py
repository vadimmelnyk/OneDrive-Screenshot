__author__ = 'Vadim Melnyk'

import requests
import os.path
class OneDriveSend():

    @staticmethod
    def upload_file(file_path, access_token):
        url = 'https://apis.live.net/v5.0/me/skydrive/files/sp_image.png?access_token='
        if os.path.isfile(file_path):
            # print "File exists. Opening file..."
            my_file = open(file_path, 'rb')
            my_file = my_file.read()
            # print "Uploading file..."
            r = requests.put(url+access_token, my_file)
            # print "Done"
            data = r.json()
            link = data['source']
            final_link = link[:-16]
            print final_link
            return final_link
        else:
            return False

