####################################################
# (C) Mark Trimmer, 2016, All Rights Reserved
#
# File Name: ststoken.py
#
# Creation Date: 28-12-2016
#
# Created By: Mark Trimmer
#
# Purpose:
#
####################################################
from __future__ import print_function

import boto3
import boto3.session
import getpass

class StsToken(object):

    def __init__(self, credentials):
        self.credentials = credentials
        # We should make this work for other regions
        self.session = boto3.session.Session(
            aws_access_key_id=self.credentials['root_access_key_id'],
            aws_secret_access_key=self.credentials['root_secret_access_key']
        )
        self.sts_client = self.session.client('sts', region_name='us-east-1')
        self.iam = self.session.resource('iam', region_name='us-east-1')


    def get_auth(self):
        user_identity = self.sts_client.get_caller_identity()
        username = user_identity['Arn'].split('/')[1]
        user = self.iam.User(username)
        mfas = [mfa for mfa in user.mfa_devices.all()]
        if len(mfas) is not 1:
            raise Exception('Either No MFA is set, or more than one MFA is set!')
        mfa = mfas[0]
        serial_number = mfa.serial_number

        token_code = getpass.getpass('Please Enter MFA Token: ')

        credentials = self.sts_client.get_session_token(
            DurationSeconds=43200,
            SerialNumber=serial_number,
            TokenCode=token_code
        )

        self.credentials['aws_access_key_id'] = credentials['Credentials']['AccessKeyId']
        self.credentials['aws_secret_access_key'] = credentials['Credentials']['SecretAccessKey']
        self.credentials['aws_session_token'] = credentials['Credentials']['SessionToken']

        self.credentials['expiration'] = credentials['Credentials']['Expiration'].strftime('%Y%m%d %H:%M:%S%Z')


        self.credentials.make_active()
        self.credentials.save()
