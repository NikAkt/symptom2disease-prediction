# Symptom-to-Disorder Matching Application

This project is a symptom-to-disorder matching application using Hadoop/MapReduce and Streamlit. The application allows users to input symptoms and receive predictions for potential disorders based on a preprocessed healthcare dataset.
dsp is the folder that contains all of the files needed to run the application.
dsp stands for Disease - Symptom Prediction.

## Project Overview

The application processes a dataset of disorders and associated symptoms to create a mapping between symptoms and likely disorders. This mapping is then used by a Streamlit dashboard to provide symptom-based predictions.

### Key Components

- **Hadoop MapReduce**: Processes the dataset to generate a mapping between symptoms and disorders.
- **Docker**: Containerizes the application to enable easy setup and consistent deployment.
- **Streamlit**: Hosts the user interface where users can enter symptoms and view potential disorders.

## Prerequisites

- **Docker**: Ensure Docker is installed and running. [Download Docker](https://docs.docker.com/get-docker/).

## Getting Started

Follow these steps to set up and run the application:

1. **Extract the Project Files**

   - Unzip the project folder to your local machine.
   - Open a terminal and navigate to the extracted project folder (the root folder should contain the `docker-compose.yml` file).

   ```bash
   cd path/to/dsp
   ```

2. **Run the Application**

   - Start the application by running the following command in the project root directory:

     ```bash
     docker compose up
     ```

   This command will initialize three containers:

   - **Namenode**: Executes the MapReduce job to process the dataset.
   - **Datanode**: Supports data storage within the Hadoop Distributed File System (HDFS).
   - **Streamlit**: Hosts the user-facing dashboard.

3. **Access the Application**

   - Once the containers are running and this line shows up in the terminal:
     `namenode INFO streaming.StreamJob: Output directory:/user/root/output/symptom_disease_mapping_run2` open your web browser and navigate to:

     ```
     http://localhost:8501
     ```

   - The Streamlit dashboard should now be accessible. You can enter symptoms into the input field, and the app will display a list of potential disorders associated with those symptoms.

## Stopping the Application

To stop the application, return to the terminal where `docker compose up` is running and press `Ctrl + C`. To fully clean up containers, networks, and volumes, run:

```bash
docker compose down
```
