import argparse
import json
import sys

from .api import PyLacus


def main():
    parser = argparse.ArgumentParser(description='Query a Lacus instance.')
    parser.add_argument('--url-instance', type=str, required=True, help='URL of the instance.')
    parser.add_argument('--redis_up', action='store_true', help='Check if redis is up.')

    subparsers = parser.add_subparsers(help='Available commands', dest='command')

    enqueue = subparsers.add_parser('enqueue', help="Enqueue a url for capture")
    enqueue.add_argument('url', help='URL to capture')

    status = subparsers.add_parser('status', help="Get status of a capture")
    status.add_argument('uuid', help="UUID of the capture")

    result = subparsers.add_parser('result', help="Get result of a capture.")
    result.add_argument('uuid', help="UUID of the capture")

    args = parser.parse_args()

    client = PyLacus(args.url_instance)

    if not client.is_up:
        print(f'Unable to reach {client.root_url}. Is the server up?')
        sys.exit(1)
    if args.redis_up:
        response = client.redis_up()
    elif args.command == 'enqueue':
        response = client.enqueue({'url': args.url})
    elif args.command == 'status':
        response = client.capture_status(args.uuid)
    elif args.command == 'result':
        response = client.capture_result(args.uuid, decode=False)
    else:
        response = "Invalid request"

    print(json.dumps(response, indent=2))
