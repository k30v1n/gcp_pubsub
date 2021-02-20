#!/usr/bin/env python

# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This application demonstrates how to perform basic operations on topics
with the Cloud Pub/Sub API.

For more information, see the README.md under /pubsub and the documentation
at https://cloud.google.com/pubsub/docs.
"""

import argparse
import os
import sys

def list_topics(project_id):
    """Lists all Pub/Sub topics in the given project."""
    # [START pubsub_list_topics]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"

    publisher = pubsub_v1.PublisherClient()
    project_path = publisher.project_path(project_id)

    for topic in publisher.list_topics(project_path):
        print(topic)
    # [END pubsub_list_topics]


def create_topic(project_id, topic_name):
    """Create a new Pub/Sub topic."""
    # [START pubsub_quickstart_create_topic]
    # [START pubsub_create_topic]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    topic = publisher.create_topic(topic_path)

    print('Topic created: {}'.format(topic))
    # [END pubsub_quickstart_create_topic]
    # [END pubsub_create_topic]


def delete_topic(project_id, topic_name):
    """Deletes an existing Pub/Sub topic."""
    # [START pubsub_delete_topic]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    publisher.delete_topic(topic_path)

    print('Topic deleted: {}'.format(topic_path))
    # [END pubsub_delete_topic]


def publish_messages(project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic."""
    # [START pubsub_quickstart_publisher]
    # [START pubsub_publish]
    from google.cloud import pubsub_v1

    print("publish_messages(project_id, topic_name)")

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    print("client created.")
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)
    print("topic set.")

    for n in range(1, 10):
        print("publishing message...", n)
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print('Published messages.')
    # [END pubsub_quickstart_publisher]
    # [END pubsub_publish]

def publish_message(project_id, topic_name, message):
    """Publishes a specific message to a Pub/Sub topic."""
    from google.cloud import pubsub_v1

    publisher = pubsub_v1.PublisherClient()
    # The `topic_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/topics/{topic_name}`
    topic_path = publisher.topic_path(project_id, topic_name)

    data = u'{}'.format(message)
    # Data must be a bytestring
    data = data.encode('utf-8')
    # When you publish a message, the client returns a future.
    future = publisher.publish(topic_path, data=data)
    print(future.result())

    print('Published message.')


def publish_messages_with_custom_attributes(project_id, topic_name):
    """Publishes multiple messages with custom attributes
    to a Pub/Sub topic."""
    # [START pubsub_publish_custom_attributes]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # Add two attributes, origin and username, to the message
        future = publisher.publish(
            topic_path, data, origin='python-sample', username='gcp'
        )
        print(future.result())

    print('Published messages with custom attributes.')
    # [END pubsub_publish_custom_attributes]


def publish_messages_with_futures(project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic and prints their
    message IDs."""
    # [START pubsub_publisher_concurrency_control]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        # When you publish a message, the client returns a future.
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print('Published messages with futures.')
    # [END pubsub_publisher_concurrency_control]


def publish_messages_with_error_handler(project_id, topic_name):
    # [START pubsub_publish_messages_error_handler]
    """Publishes multiple messages to a Pub/Sub topic with an error handler."""
    import time

    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    futures = dict()

    def get_callback(f, data):
        def callback(f):
            try:
                print(f.result())
                futures.pop(data)
            except:  # noqa
                print('Please handle {} for {}.'.format(f.exception(), data))

        return callback

    for i in range(10):
        data = str(i)
        futures.update({data: None})
        # When you publish a message, the client returns a future.
        future = publisher.publish(
            topic_path, data=data.encode('utf-8')  # data must be a bytestring.
        )
        futures[data] = future
        # Publish failures shall be handled in the callback function.
        future.add_done_callback(get_callback(future, data))

    # Wait for all the publish futures to resolve before exiting.
    while futures:
        time.sleep(5)

    print('Published message with error handler.')
    # [END pubsub_publish_messages_error_handler]


def publish_messages_with_batch_settings(project_id, topic_name):
    """Publishes multiple messages to a Pub/Sub topic with batch settings."""
    # [START pubsub_publisher_batch_settings]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    # Configure the batch to publish as soon as there is one kilobyte
    # of data or one second has passed.
    batch_settings = pubsub_v1.types.BatchSettings(
        max_bytes=1024,  # One kilobyte
        max_latency=1,   # One second
    )
    publisher = pubsub_v1.PublisherClient(batch_settings)
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print('Published messages with batch settings.')
    # [END pubsub_publisher_batch_settings]


def publish_messages_with_retry_settings(project_id, topic_name):
    """Publishes messages with custom retry settings."""
    # [START pubsub_publisher_retry_settings]
    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO topic_name = "Your Pub/Sub topic name"

    # Configure the retry settings. Defaults will be overwritten.
    retry_settings = {
        'interfaces': {
            'google.pubsub.v1.Publisher': {
                'retry_codes': {
                    'publish': [
                        'ABORTED',
                        'CANCELLED',
                        'DEADLINE_EXCEEDED',
                        'INTERNAL',
                        'RESOURCE_EXHAUSTED',
                        'UNAVAILABLE',
                        'UNKNOWN',
                    ]
                },
                'retry_params': {
                    'messaging': {
                        'initial_retry_delay_millis': 150,  # default: 100
                        'retry_delay_multiplier': 1.5,  # default: 1.3
                        'max_retry_delay_millis': 65000,  # default: 60000
                        'initial_rpc_timeout_millis': 25000,  # default: 25000
                        'rpc_timeout_multiplier': 1.0,  # default: 1.0
                        'max_rpc_timeout_millis': 35000,  # default: 30000
                        'total_timeout_millis': 650000,  # default: 600000
                    }
                },
                'methods': {
                    'Publish': {
                        'retry_codes_name': 'publish',
                        'retry_params_name': 'messaging',
                    }
                },
            }
        }
    }

    publisher = pubsub_v1.PublisherClient(client_config=retry_settings)
    topic_path = publisher.topic_path(project_id, topic_name)

    for n in range(1, 10):
        data = u'Message number {}'.format(n)
        # Data must be a bytestring
        data = data.encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        print(future.result())

    print('Published messages with retry settings.')
    # [END pubsub_publisher_retry_settings]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    print('PUBSUB_EMULATOR_HOST set to:', os.environ.get('PUBSUB_EMULATOR_HOST'))
    print('PUBSUB_PROJECT set to:', os.environ.get('PUBSUB_PROJECT'))
    print('PUBSUB_TOPIC set to:', os.environ.get('PUBSUB_TOPIC'))

    project_id = os.environ.get('PUBSUB_PROJECT')
    #parser.add_argument('project_id', help='Your Google Cloud project ID')

    # subparsers = parser.add_subparsers(dest='command')

    # publish_parser = subparsers.add_parser('publish',
    #                                        help=publish_messages.__doc__)
    # publish_parser.add_argument('topic_name')

    # publish_msg = subparsers.add_parser(
    #     'publish-msg',
    #     help=publish_message.__doc__
    # )

    parser.add_argument('--message', required=False)
    parser.add_argument('-m', required=False)
    parser.add_argument('--topic', required=False)
    parser.add_argument('-t', required=False)

    args = parser.parse_args()

    # Get topic value
    topic = None
    if args.topic != None:
        topic = args.topic
    elif args.t != None:
        topic = args.t
    elif os.environ.get('PUBSUB_TOPIC') != None:
        topic = os.environ.get('PUBSUB_TOPIC')
    else:
        sys.exit("topic should be provided or configured globally with PUBSUB_TOPIC")

    print("TOPIC set to", topic)

    # Get message content
    message = None
    if args.message != None:
        message = args.message
    elif args.m != None:
        message = args.m

    print('MESSAGE set to', message)

    if message != None:
        publish_message(project_id, topic, message)
    else:
        publish_messages(project_id, topic)

    print('end of the script')

    # if args.command == 'list':
    #     list_topics(project_id)
    # elif args.command == 'create':
    #     create_topic(project_id, args.topic)
    # elif args.command == 'delete':
    #     delete_topic(project_id, args.topic_name)
    # elif args.command == 'publish':
    #     publish_messages(project_id, args.topic_name)
    # elif args.command == 'publish-msg':
    #     publish_message(project_id, args.topic_name, args.message)
    # elif args.command == 'publish-with-custom-attributes':
    #     publish_messages_with_custom_attributes(project_id, args.topic_name)
    # elif args.command == 'publish-with-futures':
    #     publish_messages_with_futures(project_id, args.topic_name)
    # elif args.command == 'publish-with-error-handler':
    #     publish_messages_with_error_handler(project_id, args.topic_name)
    # elif args.command == 'publish-with-batch-settings':
    #     publish_messages_with_batch_settings(project_id, args.topic_name)
    # elif args.command == 'publish-with-retry-settings':
    #     publish_messages_with_retry_settings(project_id, args.topic_name)
