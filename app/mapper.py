# mapper.py
import sys

for line in sys.stdin:
    if line.startswith("Disease"):
        continue
    # Remove leading/trailing whitespace
    line = line.strip()

    # Split by commas, assuming the format: Disease, Symptom_1, Symptom_2, ..., Symptom_17
    parts = line.split(",")
    disease = parts[0].strip()
    symptoms = [symptom.strip() for symptom in parts[1:] if symptom.strip()]

    # Output each symptom as a key with the disease as the value
    for symptom in symptoms:
        print("{}\t{}".format(symptom, disease))
