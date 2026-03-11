# Intensive Station Calculator

A desktop medical calculator for basic fluid and electrolyte assessment in intensive care patients.

This project was built with Python and CustomTkinter. It allows creating patient records, storing laboratory and clinical parameters, calculating several derived values, and saving patient history in JSON format.

## Features

- Create a new patient record through a GUI
- Save patient data locally as JSON files
- Load all saved patients from storage
- Update laboratory values
- Update clinical parameters
- View saved patient history
- Calculate:
  - Ideal Body Weight (IBW)
  - Calculated serum osmolality
  - Estimated water / sodium deficit
  - Infusion target

## Clinical calculations included

### 1. Ideal Body Weight (IBW)
- Female: `45.5 + 0.91 × (height - 152.4)`
- Male: `50 + 0.91 × (height - 152.4)`

### 2. Calculated Osmolality
- `2 × Na + glucose / 18 + urea / 2.8`

### 3. Deficit estimation
Depending on osmolality:
- Hypoosmolar state → sodium deficit logic
- Normoosmolar state → water deficit logic based on hematocrit
- Hyperosmolar state → free water deficit logic

### 4. Infusion target
Based on:
- IBW
- Perspiration losses
- Deficit
- Diuresis
- Water-balance target

## Project structure

```text
project/
│
├── main.py
├── patient.py
├── storage.py
├── requirements.txt
├── README.md
└── my_patients/
File overview

main.py — GUI application built with CustomTkinter

patient.py — Patient class and medical calculation methods

storage.py — loading, saving, and batch calculations

my_patients/ — local JSON storage for patient records

How to run
1. Clone the repository
git clone <your-repo-link>
cd <your-repo-folder>
2. Install dependencies
pip install -r requirements.txt
3. Run the application
python main.py
Data storage

Each patient is stored as a separate JSON file inside the my_patients folder.

Stored data includes:

demographic data

diagnosis

laboratory values

clinical parameters

calculated values

dated history entries

Example workflow

Open the application

Create a new patient

Enter:

sex

age

height

diagnosis

sodium, glucose, urea, hematocrit

temperature and diuresis

Save patient

Review or update patient later

Recalculate values for loaded patients

Notes

This project is intended for educational and portfolio purposes.

It is not a certified medical device and must not be used as a sole basis for clinical decision-making.

Future improvements

Better validation of input fields

More detailed electrolyte correction logic

Search and filtering by diagnosis or date

Charts for trend visualization

Extended patient history viewer

Export to CSV or PDF

Improved error handling

Packaging as standalone desktop app

Author

Lidiia Petrovska

Python / medical logic / desktop application project