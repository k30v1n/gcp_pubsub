# WIP
docker support is still WORK IN PROGRESS

# gcp-tools

GCP Tools, including tools to run pubsub emulator locally.


## Configure pubsub emulator locally
Those instructions were based on https://cloud.google.com/pubsub/docs/emulator


1. Install the latest versions of Python 2 and 3 ([Python Website](https://www.python.org/downloads/windows/))
    - When you install each version, make sure you select the Add Python to PATH option for both versions. If you didn't do this, you need to add Python's installation directory and the Scripts folder to your path, for example: C:\Python27\;C:\Python27\Scripts\.
1. Install [Google CLoud SDK](https://cloud.google.com/sdk/docs/). GCP SDK contains the gcloud command-line tool.
1. It will prompt to you authenticate, do it with your questrade account, or run the following. Don't worry, if you are a developer you will not have permission to messup anything on the real GCP server :)

    `gcloud auth login`
1. Install pubsub emulator:

    `gcloud components install pubsub-emulator`

    `gcloud components update`

The configuration is done now.

## Running and setting up new topic and its subscription
These scripts are locaded on the `pubsub-local/` directory, so its recommended to run those on this directory.

> **IMPORTANT NOTE**: Every time you shut down your pubsub emulator all topics and subscriptions are DELETED from your environment. So its higly recommended to try to automate its initialization with the variables that you need.

1. Starting the emulator. Here is a shortcut script to it

    `pubsub_start [PROJECT_ID]`
    - `[PROJECT_ID]`: You can also list all projects available by running `gcloud projects list`.

1. To run the following commands we'll be using a python customized [client API](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/master/pubsub/cloud-client). But before that:
    
    - navigate to `pubsub-local/cloud-client/`
    - run `pip install -r requirements.txt`
    - get back to `pubsub-local/`
1. Now with the pubsub running start another CMD window and create a new topic and a subscriber for it

    `pubsub_create [PROJECT_ID] [PUBLISHER_TOPIC_ID] [SUBSCRIBER_TOPIC_ID]`
    - `[PROJECT_ID]`:  You can also list all projects available by running `gcloud projects list`.
    - `[PUBLISHER_TOPIC_ID]`: The publisher topic ID that will be created locally. Example: `local.1.0.testing`
    - `[SUBSCRIBER_TOPIC_ID]`: The subscriber topic ID that will be created locally to the previous publisher. Example: `local.1.0.testing`

## Testing it
These scripts are locaded on the `pubsub-local/` directory, so its recommended to run those on this directory.

1. Now that pubsub emulator is running and topics and subscribers were created, lets listen to the subscriber:

    `pubsub_subscriber_listen [PROJECT_ID] [SUBSCRIBER_TOPIC_ID]`
    - `[PROJECT_ID]`:  You can also list all projects available by running `gcloud projects list`.
    - `[SUBSCRIBER_TOPIC_ID]`: The subscriber topic ID that was created locally to the previous publisher. Example: `local.1.0.testing`
1. With the subscriber listening lets publish 10 messages in sequence on this topic (**this command is just for testing**). It will print the message IDs.

    `pubsub_publisher_test [PROJECT_ID] [PUBLISHER_TOPIC_ID]`
    - `[PROJECT_ID]`:  You can also list all projects available by running `gcloud projects list`.
    - `[PUBLISHER_TOPIC_ID]`: The publisher topic ID that was created locally. Example: `local.1.0.testing`
1. It is possible to publish a string to a topic as well:

    `pubsub_publisher_publish [PROJECT_ID] [PUBLISHER_TOPIC_ID] [MESSAGE_STRING]`
    - `[PROJECT_ID]`:  You can also list all projects available by running `gcloud projects list`.
    - `[PUBLISHER_TOPIC_ID]`: The publisher topic ID that was created locally. Example: `local.1.0.testing`
    - `[MESSAGE_STRING]`: The message string that will be sent to topic. Example `"{'id':'1','name':'testing object serialization'}"`