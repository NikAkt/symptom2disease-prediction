import sys
from collections import defaultdict

# Initialize a dictionary to collect diseases for each symptom
symptom_diseases = defaultdict(set)

# Read each line from the mapper output
for line in sys.stdin:
    line = line.strip()
    symptom, disease = line.split("\t", 1)
    symptom_diseases[symptom].add(disease)

# Output each symptom with its list of associated diseases
for symptom, diseases in symptom_diseases.items():
    diseases_list = ", ".join(diseases)
    print("{}\t{}".format(symptom, diseases_list))
