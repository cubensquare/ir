from kafka import KafkaConsumer
import json
import os

tracker_file = 'tracker.json'

consumer = KafkaConsumer(
    'ticket_bookings',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='bulletin-board-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📬 Consumer bulletin listening...")

for message in consumer:
    booking = message.value
    print(f"📥 Received: {booking}")

    if os.path.exists(tracker_file):
        with open(tracker_file, 'r') as f:
            data = json.load(f)
    else:
        data = {
            "produced": 0,
            "topic": 0,
            "partition": 0,
            "consumed": 0,
            "last_message": {}
        }

    data["consumed"] += 1
    data["last_message"] = booking

    with open(tracker_file, 'w') as f:
        json.dump(data, f, indent=2)
