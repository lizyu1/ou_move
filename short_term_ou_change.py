#!/usr/bin/python
'''
Making a short-lived OU change, the change will be reverted back to the original setting after a timeut period
'''
import sys
import argparse
import ou_change
from datetime import datetime
from time import sleep

timeout = ''

def print_time():
    print
    now = datetime.now()
    print("Time is now: {}".format(now)
    print("Time is now: {}".format(now.strftime("%Y-%m-%d %H:%M"))
    print


def wait(timeout):
    print
    print("Waiting for {} seconds and revert back to original OU").format(timeout)
    for i in range(1,101):
        sys.stdout.write('\r')
        sys.stdout.write("[%-100s] %d%%" % ('='*i, i))
        sys.stdout.flush()
        sleep(timeout/100)
    print


def main(args):
    print_time()
    source_ou_name = ou_change.main(args)
    if args.dest_ou_name:
        timeout = int(args.duration)
    wait(timeout)
    args.dest_ou_name = source_ou_name
    ou_change.main(args)
    print_time()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update OU for an account')
    parser.add_argument('--account_id', help='Account ID', required=True)
    parser.add_argument('--dest_ou_name', help='Destination OU', required=True)
    parser.add_argument('--aws_access_key', help='AWS Access Key', required=True)
    parser.add_argument('--aws_secret_key', help='AWS Secret key', required=True)
    parser.add_argument('--aws_session_token', help='AWS Session Token', required=True)
    parser.add_argument('--duration', help='Duration of change in seconds', default=1200)
    args = parser.parse_args()
    main(args)

