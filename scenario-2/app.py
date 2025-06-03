from flask import Flask, render_template, request, redirect
from kafka import KafkaProducer
import json
import threading
import time
import os

app = Flask(__name__)
tracker_file = 'tracker_partition.json'
topic_name = 'ticket_partitioned'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: v.encode('utf-8')
)

def update_tracker(key):
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

    data[key] += 1

    with open(tracker_file, 'w') as file:
        json.dump(data, file)
@app.route('/')
def index():
    with open(tracker_file, 'r') as file:
        data = json.load(file)
    return render_template('index.html', stats=data)

@app.route('/book', methods=['POST'])
def book_ticket():
    user = request.form['username']
    from_station = request.form['from_station']
    to_station = request.form['to_station']
    date = request.form['travel_date']

    event = {
        'user': user,
        'from_station': from_station,
        'to_station': to_station,
        'date': date,
        'event': 'ticket_booked'
    }

    # Use alphabetical rule to determine partition via key
    first_letter = user[0].upper()
    key = 'group1' if 'A' <= first_letter <= 'M' else 'group2'
    producer.send(topic_name, key=key, value=event)

    update_tracker("produced")
    update_tracker("topic")
    if key == 'group1':
        update_tracker("partition_0")
    else:
        update_tracker("partition_1")

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
