from flask import Flask, render_template, request, redirect
from kafka import KafkaProducer
import json
import os

app = Flask(__name__)
tracker_file = 'tracker_partition.json'
booking_log_file = 'booking_log.json'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def update_tracker(key, partition=None):
    if not os.path.exists(tracker_file):
        with open(tracker_file, 'w') as file:
            json.dump({
                "produced": 0,
                "topic": 0,
                "partition": 0,
                "consumed": 0,
                "last_partition": 0
            }, file)
    with open(tracker_file, 'r') as file:
        data = json.load(file)
    data[key] += 1
    if partition is not None:
        data['last_partition'] = partition
    with open(tracker_file, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    if not os.path.exists(tracker_file):
        with open(tracker_file, 'w') as file:
            json.dump({
                "produced": 0,
                "topic": 0,
                "partition": 0,
                "consumed": 0,
                "last_partition": 0
            }, file)
    with open(tracker_file, 'r') as file:
        stats = json.load(file)

    if os.path.exists(booking_log_file):
        with open(booking_log_file, 'r') as file:
            logs = json.load(file)
    else:
        logs = {"0": [], "1": []}
    return render_template('index.html', stats=stats, logs=logs)

@app.route('/book', methods=['POST'])
def book_ticket():
    user = request.form['username']
    from_station = request.form['from_station']
    to_station = request.form['to_station']
    date = request.form['travel_date']

    first_letter = user[0].upper()
    if 'A' <= first_letter <= 'M':
        key = 'group1'
        partition = 0
    else:
        key = 'group2'
        partition = 1

    event = {
        'user': user,
        'from_station': from_station,
        'to_station': to_station,
        'date': date
    }

    producer.send('ticket_partitioned', key=key.encode(), value=event, partition=partition)
    update_tracker("produced")
    update_tracker("topic")
    update_tracker("partition", partition=partition)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
