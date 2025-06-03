from flask import Flask, render_template, request, redirect
from kafka import KafkaProducer
import json
import threading
import time

app = Flask(__name__)
tracker_file = 'tracker.json'

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def update_tracker(key):
    with open(tracker_file, 'r') as file:
        data = json.load(file)
    data[key] += 1
    with open(tracker_file, 'w') as file:
        json.dump(data, file)

@app.route('/')
def index():
    with open(tracker_file, 'r') as file:
        data = json.load(file)
    return render_template('index.html', stats=data, last=data.get("last_message", {}))

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

    producer.send('ticket_bookings', event)
    update_tracker("produced")
    update_tracker("topic")
    update_tracker("partition")
    return redirect('/')

# Optional simulator – not needed if you use consumerapp.py
def simulated_consumer():
    while True:
        time.sleep(10)
        update_tracker("consumed")

threading.Thread(target=simulated_consumer, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
