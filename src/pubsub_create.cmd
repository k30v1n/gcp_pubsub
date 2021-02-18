python cloud-client/publisher.py %1 create %2
python cloud-client/subscriber.py %1 create %2 %3
python cloud-client/publisher.py %1 list
python cloud-client/subscriber.py %1 list_in_topic %2