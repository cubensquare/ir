from kafka import KafkaConsumer
import json
import os
import requests

tracker_file = 'tracker_partition.json'
log_file = 'booking_log.json'

# Reset logs
with open(tracker_file, 'w') as file:
    json.dump({
        "produced": 0,
        "topic": 0,
        "partition": 0,
        "consumed": 0,
        "last_partition": 0
    }, file)

with open(log_file, 'w') as file:
    json.dump({"0": [], "1": []}, file)

consumer = KafkaConsumer(
    'ticket_partitioned',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='rail-consumer-group-v3',
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def update_tracker():
    with open(tracker_file, 'r') as file:
        data = json.load(file)
    data['consumed'] += 1
    with open(tracker_file, 'w') as file:
        json.dump(data, file)

def log_booking(partition, booking):
    try:
        with open(log_file, 'r') as file:
            logs = json.load(file)
    except:
        logs = {"0": [], "1": []}
    logs[str(partition)].append(booking)
    with open(log_file, 'w') as file:
        json.dump(logs, file)

print("📬 Listening to ticket_partitioned topic...")
for message in consumer:
    booking = message.value
    print(f"📨 Received from Partition {message.partition}: {booking}")
    requests.get('http://locahost:5002/update_tracker?tracker=consumed')
    log_booking(message.partition, booking)
