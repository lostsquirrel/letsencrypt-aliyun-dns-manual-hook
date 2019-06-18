#!/usr/bin/env python
import ConfigParser
from enum import Enum

from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteSubDomainRecordsRequest import DeleteSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkcore.client import AcsClient

CONFIG_FILE_PATH = '/etc/alidns/config.ini'


class RecordType(Enum):
    A = 1,
    CNAME = 2,
    MX = 3,
    AAAA = 4,
    TXT = 5,
    NS = 6,
    SRV = 7,
    CAA = 8,
    REDIRECT_URL = 9,
    FORWARD_URL = 10,

    def __str__(self):
        return self.name


class Line(Enum):
    default = 1,
    google = 2,

    def __str__(self):
        return self.name


def create_client():
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    ak = config.get('aliyun', 'app_access_key')
    secret = config.get('aliyun', 'app_secret')

    return AcsClient(ak, secret)


def add_domain_record(domain_name, rr, record_type, value, line=Line.default):
    client = create_client()
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    request.set_RR(rr)
    request.set_Type(record_type)
    request.set_Value(value)
    request.set_Line(line)
    response = client.do_action_with_exception(request)
    return response


def delete_sub_domain_record(domain_name, rr, record_type=None):
    client = create_client()
    request = DeleteSubDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    request.set_RR(rr)
    if record_type is not None:
        request.set_Type(record_type)

    response = client.do_action_with_exception(request)
    return response


def get_domain_record_list(domain_name):
    client = create_client()
    request = DescribeDomainRecordsRequest()
    request.set_accept_format('json')
    request.set_DomainName(domain_name)
    response = client.do_action_with_exception(request)
    return response
