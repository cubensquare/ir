```Console

🧰 1. Prerequisites
	•	✅ Install Java (JDK 17 or higher)
	•	Download JDK → Install → Add JAVA_HOME to environment variables
	•	Verify:
```

```bash
java -version
```

```Console
	•	✅ Install Python 3.11+
	•	Download Python → Enable “Add to PATH” during install
	•	Verify:
```

```bash
python --version
```


## ✅ Install pip + virtualenv (optional but recommended):
```bash
pip install virtualenv
```

## ✅ Install Git Bash or use WSL (Windows Subsystem for Linux) for a Linux-like terminal


## 📦 2. Download and Extract Kafka
	1.	Go to Kafka downloads
	2.	Download: kafka_2.13-3.6.1.tgz
	3.	Extract using 7-Zip or similar
	4.	Navigate inside Kafka folder using terminal (Git Bash or PowerShell)


## ⚙️ 3. Run Zookeeper and Kafka on Windows

Navigate inside the Kafka folder (cd kafka_2.13-3.6.1) and open two terminal windows:

🐘 Terminal 1: Start ZooKeeper

```bash
bin\windows\zookeeper-server-start.bat config\zookeeper.properties
```

🔁 Terminal 2: Start Kafka Broker
```bash
bin\windows\kafka-server-start.bat config\server.properties
```

📨 4. Create Topic
```bash
bin\windows\kafka-topics.bat --create --topic ticket_bookings --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
```

🐍 5. Set Up Python Kafka App

## Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

##Install dependencies:
```bash
pip install flask kafka-python flask-socketio
```

Place your app.py, consumer.py, and index.html in a folder and run:
python app.py

🔁 6. Web Browser Access

Open browser:

http://localhost:5000

You can now book tickets (producer), and run a consumer in another terminal to simulate the bulletin board.

