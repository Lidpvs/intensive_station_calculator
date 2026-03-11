# storage.py

from pathlib import Path
from datetime import datetime
import json
from patient import Patient


my_patients = Path("my_patients")
my_patients.mkdir(exist_ok=True)


def read_json(name):
    try:
        with open(f"my_patients/{name}.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        patient = Patient(
            data["name"],
            data["sex"],
            data["age"],
            data["height"],
            data["diagnose"],
            data["target"]
        )

        patient.ibw = data.get("ibw")
        patient.osm = data.get("osm")
        patient.defizit = data.get("defizit")
        patient.infusion_target = data.get("infusion target")
        patient.osm_comment = data.get("osm comment", "")
        patient.recommendation = data.get("recommendation", "")
        patient.analyse = data.get("analyse", {})
        patient.parameters = data.get("parameters", {})
        patient.history = data.get("history", {})

        print(f"Data von {patient.name} ist geladen")
        return patient

    except Exception:
        print(f"File {name} ist nicht gefunden")
        return None


def load_patients():

    patients = {}

    for file in my_patients.glob("*.json"):

        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        patient = Patient(
            data["name"],
            data["sex"],
            data["age"],
            data["height"],
            data["diagnose"],
            data["target"]
        )

        patient.ibw = data.get("ibw")
        patient.osm = data.get("osm")
        patient.defizit = data.get("defizit")
        patient.infusion_target = data.get("infusion target")
        patient.osm_comment = data.get("osm comment", "")
        patient.recommendation = data.get("recommendation", "")
        patient.analyse = data.get("analyse", {})
        patient.parameters = data.get("parameters", {})
        patient.history = data.get("history", {})

        patients[patient.name] = patient

    return patients


def save_all_patients(patients, date=None):

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    for pat in patients.values():
        pat.save_data(date)
        pat.save_to_json()

    print("Alle Daten sind gespeichert")


def calc_all(patients, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    messages = []

    for name, pat in patients.items():
        try:
            if date not in pat.history:
                ibw = pat.ibw_calc()
                osm = pat.osm_calc()
                infusion_target = pat.infusion_calc()

                pat.save_data(date)
                pat.save_to_json()

                messages.append(
                    f"{name}\n"
                    f"IBW={ibw}\n" 
                    f"Osm={osm}\n" 
                    f"Status: {pat.osm_comment}\n"
                    f"{pat.recommendation}\n"
                    f"Infusion Ziel={infusion_target} ml/d\n"
                )
            else:
                messages.append(f"{name}: already calculated for today\n")

        except Exception as e:
            messages.append(f"{name}: calculation error -> {e}")

    return "\n".join(messages)