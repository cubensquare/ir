from kafka import KafkaConsumer
import json
import os

tracker_file = 'tracker_partition.json'

def update_tracker(booking, partition):
    if not os.path.exists(tracker_file):
        with open(tracker_file, 'w') as file:
            json.dump({
                "produced": 0,
                "topic": 0,
                "partition_0": 0,
                "partition_1": 0,
                "consumed": 0,
                "last_message": {},
                "last_partition": 0
            }, file)

    with open(tracker_file, 'r') as file:
        data = json.load(file)

    data['consumed'] += 1
    data['last_message'] = booking
    data['last_partition'] = partition

    with open(tracker_file, 'w') as file:
        json.dump(data, file, indent=2)

consumer = KafkaConsumer(
    'ticket_partitioned',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='rail-consumer-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📬 Listening to 'ticket_partitioned' topic...")

for msg in consumer:
    booking = msg.value
    print(f"📥 Partition {msg.partition} | Ticket: {booking}")
    update_tracker(booking, msg.partition)
