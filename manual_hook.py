#!/usr/bin/env python

import sys
import os
import getopt
import time
import dns.resolver
import logging

from aliyun import Line, add_domain_record, RecordType, delete_sub_domain_record

CERTBOT_VALIDATION = 'CERTBOT_VALIDATION'  # The validation string (HTTP-01 and DNS-01 only)
DOMAIN = 'CERTBOT_DOMAIN'  # The domain being authenticated
RR = '_acme-challenge'
DNS_LINE = (Line.default, Line.google)

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def query_dns(domain_name):
    try:
        return dns.resolver.query(domain_name, rdtype=dns.rdatatype.TXT).response.answer[0][-1].strings[0]
    except dns.resolver.NXDOMAIN:
        return None


def auth():
    try:
        validate_required_env((DOMAIN, CERTBOT_VALIDATION))
        domain_name = os.environ[DOMAIN]
        value = os.environ[CERTBOT_VALIDATION]

        for line in DNS_LINE:
            add_domain_record(domain_name, RR, RecordType.TXT, value, line=line)

        while True:
            actual = query_dns('{}.{}'.format(RR, domain_name))
            logger.debug('query dns result {}'.format(actual))
            if actual == value:
                break
            else:
                logger.info('resolver result not match wait for 1 minute')
                time.sleep(1)

        print('Success.')

    except Exception as e:
        logger.error('Error: {}'.format(e.message))
        sys.exit()


def validate_required_env(env_names):
    for env_name in env_names:

        if env_name not in os.environ:
            raise KeyError('Environment variable {} is required.'.format(env_name))


def cleanup():
    try:
        validate_required_env((DOMAIN, CERTBOT_VALIDATION))
        domain_name = os.environ[DOMAIN]
        delete_sub_domain_record(domain_name, RR)
        logger.info('Finished...')

    except Exception as e:
        logger.error('Error: {}'.format(e.message))
        sys.exit()


def main(argv):
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'hv',
            [
                'auth',
                'cleanup',
            ]
        )

        for opt, arg in opts:
            if opt == '--auth':
                auth()
            elif opt == '--cleanup':
                cleanup()
            else:
                print('Invalid option: ' + opt)

    except getopt.GetoptError as e:
        logger.error('Error: {}'.format(e.message))
    except Exception as e:
        logger.error('Error: {}'.format(e.message))

        sys.exit()


if __name__ == '__main__':
    main(sys.argv)
