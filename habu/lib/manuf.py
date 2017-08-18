#!/usr/bin/env python

# manuf.py: Parser library for Wireshark's OUI database.
# Copyright (c) 2016 Michael Huang
#
# This library is free software. It is dual licensed under the terms of the GNU Lesser General
# Public License version 3.0 (or any later version) and the Apache License version 2.0.
#
# For more information, see:
#
# <http://www.gnu.org/licenses/>
# <http://www.apache.org/licenses/>
"""Parser library for Wireshark's OUI database.

Converts MAC addresses into a manufacturer using Wireshark's OUI database.

See README.md.

"""
from __future__ import print_function
from collections import namedtuple
import argparse
import re
import sys
import io
import os

try:
    from urllib2 import urlopen
    from urllib2 import URLError
except ImportError:
    from urllib.request import urlopen
    from urllib.error import URLError

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

# Vendor tuple
Vendor = namedtuple('Vendor', ['manuf', 'comment'])


FILEDIR = os.path.dirname(os.path.abspath(__file__))
DATADIR = os.path.abspath(os.path.join(FILEDIR, '../data'))
MANUFILE = os.path.abspath(os.path.join(DATADIR, 'manuf.txt'))
MANUF_URL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf"


class MacParser(object):
    """Class that contains a parser for Wireshark's OUI database.

    Optimized for quick lookup performance by reading the entire file into memory on
    initialization. Maps ranges of MAC addresses to manufacturers and comments (descriptions).
    Contains full support for netmasks and other strange things in the database.

    See https://www.wireshark.org/tools/oui-lookup.html

    Args:
        update (bool): Whether to update the manuf file automatically. Defaults to False.

    Raises:
        IOError: If manuf file could not be found.

    """

    def  __init__(self, update=False):

        self.manufile = MANUFILE
        self.manuf_url = MANUF_URL

        if update:
            self.update()
        else:
            self.refresh()

    def refresh(self):
        """Refresh/reload manuf database. Call this when manuf file is updated.

        Raises:
            IOError: If manuf file could not be found.

        """
        with io.open(self.manufile, "r", encoding="utf-8") as read_file:
            manuf_file = StringIO(read_file.read())
        self._masks = {}

        # Build mask -> result dict
        for line in manuf_file:
            com = line.split("#", 1)
            arr = com[0].split()

            if len(arr) < 1:
                continue

            parts = arr[0].split("/")
            mac_str = self._strip_mac(parts[0])
            mac_int = self._get_mac_int(mac_str)
            mask = self._bits_left(mac_str)

            # Specification includes mask
            if len(parts) > 1:
                mask_spec = 48 - int(parts[1])
                if mask_spec > mask:
                    mask = mask_spec

            if len(com) > 1:
                result = Vendor(manuf=arr[1], comment=com[1].strip())
            else:
                result = Vendor(manuf=arr[1], comment=None)

            self._masks[(mask, mac_int >> mask)] = result

        manuf_file.close()

    def update(self, refresh=True):
        """Update the Wireshark OUI database to the latest version.

        Args:
            manuf_url (str): URL pointing to OUI database. Defaults to database located at
                code.wireshark.org.
            refresh (bool): Refresh the database once updated. Defaults to True.

        Raises:
            URLError: If the download fails

        """

        # Retrieve the new database
        try:
            response = urlopen(self.manuf_url)
        except URLError:
            raise URLError("Failed downloading OUI database")

        # Parse the response
        if response.code is 200:
            with open(self.manufile, "wb") as write_file:
                write_file.write(response.read())
            if refresh:
                self.refresh()
        else:
            err = "{0} {1}".format(response.code, response.msg)
            raise URLError("Failed downloading database: {0}".format(err))

        response.close()

    def search(self, mac, maximum=1):
        """Search for multiple Vendor tuples possibly matching a MAC address.

        Args:
            mac (str): MAC address in standard format.
            maximum (int): Maximum results to return. Defaults to 1.

        Returns:
            List of Vendor namedtuples containing (manuf, comment), with closest result first. May
            be empty if no results found.

        Raises:
            ValueError: If the MAC could not be parsed.

        """
        vendors = []
        if maximum <= 0:
            return vendors
        mac_str = self._strip_mac(mac)
        mac_int = self._get_mac_int(mac_str)

        # If the user only gave us X bits, check X bits. No partial matching!
        for mask in range(self._bits_left(mac_str), 48):
            result = self._masks.get((mask, mac_int >> mask))
            if result:
                vendors.append(result)
                if len(vendors) >= maximum:
                    break
        return vendors

    def get_all(self, mac):
        """Get a Vendor tuple containing (manuf, comment) from a MAC address.

        Args:
            mac (str): MAC address in standard format.

        Returns:
            Vendor: Vendor namedtuple containing (manuf, comment). Either or both may be None if
            not found.

        Raises:
            ValueError: If the MAC could not be parsed.

        """
        vendors = self.search(mac)
        if len(vendors) == 0:
            return Vendor(manuf=None, comment=None)
        return vendors[0]

    def get_manuf(self, mac):
        """Returns manufacturer from a MAC address.

        Args:
            mac (str): MAC address in standard format.

        Returns:
            string: String containing manufacturer, or None if not found.

        Raises:
            ValueError: If the MAC could not be parsed.

        """
        return self.get_all(mac).manuf

    def get_comment(self, mac):
        """Returns comment from a MAC address.

        Args:
            mac (str): MAC address in standard format.

        Returns:
            string: String containing comment, or None if not found.

        Raises:
            ValueError: If the MAC could not be parsed.

        """
        return self.get_all(mac).comment

    # Gets the integer representation of a stripped mac string
    def _get_mac_int(self, mac_str):
        try:
            # Fill in missing bits with zeroes
            return int(mac_str, 16) << self._bits_left(mac_str)
        except ValueError:
            raise ValueError("Could not parse MAC: {0}".format(mac_str))

    # Regular expression that matches '-', ':', and '.' characters
    _pattern = re.compile(r"[-:\.]")

    # Strips the MAC address of '-', ':', and '.' characters
    def _strip_mac(self, mac):
        return self._pattern.sub("", mac)

    # Gets the number of bits left in a mac string
    @staticmethod
    def _bits_left(mac_str):
        return 48 - 4 * len(mac_str)


