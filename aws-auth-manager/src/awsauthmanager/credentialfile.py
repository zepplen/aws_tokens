####################################################
# (C) Mark Trimmer, 2016, All Rights Reserved
#
# File Name: credentialfile.py
#
# Creation Date: 20-12-2016
#
# Created By: Mark Trimmer
#
# Purpose:
#
####################################################
from __future__ import print_function

import os
import os.path
import getpass

import ConfigParser

class CredentialFile(object):

    required_data = {
        'root_access_key_id': 'AWS Access Key ID',
        'root_secret_access_key': 'AWS Secret Key',
    }

    active_data = [
        'aws_access_key_id',
        'aws_secret_access_key',
        'aws_session_token',
    ]

    def __init__(self, profile, path=None):
        if path:
            self.credential_path = path
        else:
            self.credential_path = os.path.join(os.environ['HOME'], '.aws', 'credentials')
        if not os.path.exists(self.credential_path):
            self._template_empty_credential_file()

        self.profile = profile
        if self.profile == 'defailt':
            raise Exception('profile name "default" is not allowed')

        self.config = ConfigParser.SafeConfigParser()
        self.config.read(self.credential_path)
        self._create_section()


    def back_fill_user_data(self):
        for key, desc in self.__class__.required_data.iteritems():
            if key not in self:
                value = getpass.getpass('{}: '.format(desc))
                self[key] = value

    def _create_section(self):
        if not self.exists():
            self.config.add_section(self.profile)

    def exists(self):
        return self.config.has_section(self.profile)

    def make_active(self):
        for key in self.__class__.active_data:
            self.config.set('default', key, self[key])

    def save(self):
        with open(self.credential_path, 'w') as creds_out:
            self.config.write(creds_out)


    # The python ini parser does stupid thing when trying to create a lowercased
    # 'default' section. So we just create the file w/ it existing.
    def _template_empty_credential_file(self):
        file_contents = """[default]
last_updated=0
"""
        credential_dir = os.path.dirname(self.credential_path)
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir, 0700)
        with os.fdopen(
            os.open(
                self.credential_path,
                os.O_WRONLY | os.O_CREAT, 0o600
            ),
            'w'
        ) as cred_file:
            cred_file.write(file_contents)


    # Dictionary methods

    def __setitem__(self, key, value):
        self.config.set(self.profile, key, value)


    def __getitem__(self, key):
        if not self.config.has_option(self.profile, key):
            raise KeyError('Unknown key: {} in {}'.format(key, self.profile))
        return self.config.get(self.profile, key)

    def __contains__(self, key):
        return self.config.has_option(self.profile, key)

    def __delitem__(self, key):
        self.config.remove(key)

    def __iter__(self):
        return iter(self.config.items(self.profile))

    def __len__(self):
        return len(self.config.options(self.profile))

    def keys(self):
        return self.config.options(self.profile)
