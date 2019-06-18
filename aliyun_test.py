# coding=utf-8
import unittest

from aliyun import (add_domain_record, RecordType, get_domain_record_list, delete_sub_domain_record)

domain_name = 'shangao.tech'
rr = '__test'


class AliDNSTests(unittest.TestCase):

    @staticmethod
    def get_sub_domain_describe(sub_domain, record_list):
        records = record_list['DomainRecords']['Record']
        return tuple(filter(lambda r: r['RR'] == sub_domain, records))

    def test_record_type(self):
        # for rt in RecordType:
        #     print(rt)
        self.assertEqual(10, len(RecordType))

    def test_get_record_list(self):
        print(get_domain_record_list(domain_name))

    def test_add(self):
        print(add_domain_record(domain_name, rr, RecordType.TXT, 'test_value'))
        print(self.get_sub_domain_describe(rr, get_domain_record_list(domain_name)))

    def test_delete(self):
        print(delete_sub_domain_record(domain_name, rr))
        print(get_domain_record_list(get_domain_record_list(domain_name)))
        print(self.get_sub_domain_describe(rr, get_domain_record_list(domain_name)))


