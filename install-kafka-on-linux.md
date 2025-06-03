## Install Kafka

Kafka Installation in Linux

```Console
## 1. Prerequisites
	•	Java 8 or later installed (java -version)
	•	A Linux OS (Ubuntu/RHEL/CentOS)
```

## 2. Install Java (if not already)
```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
java -version
```

## 3. Download and Extract Kafka
```bash
wget https://archive.apache.org/dist/kafka/3.6.1/kafka_2.13-3.6.1.tgz
tar -xzf kafka_2.13-3.6.1.tgz
cd kafka_2.13-3.6.1
```

## 4. Kafka Components Installed (within Kafka folder)
	•	bin/: Scripts to run Kafka and ZooKeeper
	•	config/: Config files
	  server.properties: Kafka Broker configuration
	  zookeeper.properties: ZooKeeper config
	•	libs/: Kafka JAR dependencies
	•	logs/: Runtime logs


## Components

🔹 ZooKeeper
	•	Coordinates the Kafka cluster.
	•	Manages leader election and metadata.
	•	Required for Kafka 3.6.1 (Kafka 4.0 will remove ZooKeeper).

🔹 Kafka Broker
	•	Accepts and stores messages from producers.
	•	Serves them to consumers.

🔹 Kafka Server (Broker) vs Kafka Cluster
	•	Kafka server = 1 broker
	•	Kafka cluster = group of brokers

## ⚙️ Important Configurations
ZooKeeper Config (config/zookeeper.properties)

# Properties
```bash
dataDir=/tmp/zookeeper
clientPort=2181
maxClientCnxns=60
```

Kafka Broker Config (config/server.properties)
# Properties
```bash
broker.id=0  # unique ID for each broker
listeners=PLAINTEXT://:9092
log.dirs=/tmp/kafka-logs
zookeeper.connect=localhost:2181
```

▶️ Starting Kafka and ZooKeeper
# Start ZooKeeper:
```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

# Start Kafka Broker (in new terminal):
```bash
bin/kafka-server-start.sh config/server.properties
```

### 🧪 How to Use
# Create a topic:
```bash
bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

# Start a producer:
```bash
bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092
```

# Start a consumer:
```bash
bin/kafka-console-consumer.sh --topic test-topic --bootstrap-server localhost:9092 --from-beginning
```


### 💬 In Application (Java, Python, etc.)

Kafka is referred in code as:
	bootstrap_servers='localhost:9092'
	Producer sends data to a topic
	Consumer subscribes to a topic

