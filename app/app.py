import streamlit as st
import pandas as pd
from collections import defaultdict

# Load the symptom-to-disease mapping and the symptoms list
file_path = "./symptom_disease_mapping.txt"
symptoms_list_path = "./symptoms_list.txt"
dataset_path = "./dataset.csv"

# Read the dataset
df = pd.read_csv(dataset_path)

# Collect unique symptoms from each row, excluding 'Disease' column
symptoms = set()
for index, row in df.iterrows():
    row_symptoms = row.drop(labels=["Disease"]).dropna().tolist()  # Drop empty values
    symptoms.update(
        [symptom.strip() for symptom in row_symptoms if symptom]
    )  # Strip whitespace and ignore empty strings

# Sort symptoms alphabetically and save to file
with open(symptoms_list_path, "w") as f:
    f.write(", ".join(sorted(symptoms)))

print(f"Unique symptoms saved to {symptoms_list_path}")

# Load the symptom-to-disease mapping into a DataFrame
data = None
try:
    data = pd.read_csv(file_path, sep="\t", header=None, names=["Symptom", "Diseases"])
    data.set_index("Symptom", inplace=True)
except FileNotFoundError:
    st.error(
        "The symptom-disease mapping file was not found. Please ensure Hadoop has generated the file."
    )

# Load symptoms list for typing prediction
symptoms = []
try:
    with open(symptoms_list_path, "r") as f:
        symptoms = [line.strip() for line in f.read().split(", ")]
except FileNotFoundError:
    st.error("The symptoms list file was not found.")

# Only proceed with the dashboard if data was loaded successfully
if data is not None:
    # Dashboard Title
    st.title("Automatic Disease Diagnosis Dashboard")
    st.write("Enter symptoms to get a ranked list of possible diseases.")

    # Multiselect box for symptoms with typing prediction
    input_symptoms = st.multiselect(
        "Select symptoms",
        options=symptoms,
        default=None,
        help="Type to see suggested symptoms",
    )

    # Process the input symptoms and retrieve matching diseases
    if input_symptoms:
        disease_counts = defaultdict(int)  # Dictionary to store disease match counts

        # Iterate over each input symptom
        for symptom in input_symptoms:
            if symptom in data.index:
                diseases = data.loc[symptom, "Diseases"].split(", ")
                for disease in diseases:
                    disease_counts[
                        disease
                    ] += 1  # Increment the count for each matched disease

        # Sort diseases by the number of matching symptoms, in descending order
        sorted_diseases = sorted(
            disease_counts.items(), key=lambda x: x[1], reverse=True
        )

        # Display the results
        st.write("### Possible Diseases Based on Symptoms:")
        for disease, count in sorted_diseases:
            st.write(f"**{disease}**: matched {count} symptom(s)")
else:
    st.stop()
