#!/usr/bin/env python
####################################################
# (C) Mark Trimmer, 2016, All Rights Reserved
#
# File Name: entrypoint.py
#
# Creation Date: 28-12-2016
#
# Created By: Mark Trimmer
#
# Purpose:
#
####################################################
from __future__ import print_function
import argparse

from app import App

def token():
    parser = argparse.ArgumentParser(description='AWS STS MFA Token Generator')
    parser.add_argument('-n', '--profile-name', help='Profile Name', required=True)
    parser.add_argument('--credential-file', help='Location of AWS Credential File')
    args = parser.parse_args()
    options = vars(args)
    my_app = App(options)

if __name__ == '__main__':
    token()
