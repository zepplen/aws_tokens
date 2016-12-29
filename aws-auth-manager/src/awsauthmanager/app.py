####################################################
# (C) Mark Trimmer, 2016, All Rights Reserved
#
# File Name: app.py
#
# Creation Date: 28-12-2016
#
# Created By: Mark Trimmer
#
# Purpose:
#
####################################################
from __future__ import print_function

from credentialfile import CredentialFile
from ststoken import StsToken

class App(object):
    def __init__(self, options):
        self.options = options
        self.credential_file = CredentialFile(path=options['credential_file'], profile=options['profile_name'])
        self.credential_file.back_fill_user_data()

        self.sts = StsToken(self.credential_file)
        self.sts.get_auth()
