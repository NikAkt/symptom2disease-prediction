# hadoop/entrypoint.sh
#!/bin/bash

# Format the HDFS namenode to prepare for HDFS initialization
hdfs namenode -format -force

# Start the Hadoop namenode and datanode services
$HADOOP_HOME/sbin/hadoop-daemon.sh start namenode
$HADOOP_HOME/sbin/hadoop-daemon.sh start datanode

# Wait for HDFS services to fully start up before proceeding
sleep 10

# Create input directory in HDFS if not present and upload dataset
hdfs dfs -mkdir -p /user/root/input
hdfs dfs -put /app/dataset.csv /user/root/input/

# Configure APT repositories for Debian Stretch (used for package installations)
# We disable validity checks as the archive is no longer updated
echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list
echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list
echo 'Acquire::Check-Valid-Until "false";' | tee /etc/apt/apt.conf.d/99no-check-valid-until

# Update packages and install Python3 and pip
apt-get update
apt-get install -y python3 python3-pip

# Clean up old output directories in HDFS, if they exist, to prevent conflicts
hdfs dfs -rm -r output/symptom_disease_mapping
hdfs dfs -rm -r output/symptom_disease_mapping_run2
hdfs dfs -rm -r user/root/output/symptom_disease_mapping_run2

# Remove any previous local symptom-disease output file to ensure a fresh run
rm -f /app/symptom_disease_mapping.txt

# Run the Hadoop Streaming job using Python mapper and reducer scripts
# This processes the dataset.csv file and outputs the results to HDFS
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -input /user/root/input/dataset.csv \
    -output /user/root/output/symptom_disease_mapping_run2 \
    -mapper "/usr/bin/python3 /app/mapper.py" \
    -reducer "/usr/bin/python3 /app/reducer.py"

# Fetch the result file from HDFS to the local application directory
# This makes the output accessible to other containers or services like Streamlit
hdfs dfs -get /user/root/output/symptom_disease_mapping_run2/part-00000 /app/symptom_disease_mapping.txt

# Keep the container running after script completion by tailing a non-existent file
# This prevents the container from exiting immediately after the setup
tail -f /dev/null