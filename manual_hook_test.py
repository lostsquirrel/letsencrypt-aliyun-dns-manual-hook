# coding=utf-8
import unittest

from manual_hook import query_dns


class AliDNSTests(unittest.TestCase):

    def test_check(self):
        print(query_dns('xx.shangao.tech'))