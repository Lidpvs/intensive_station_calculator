# patient.py

from pathlib import Path     
from datetime import datetime
import json      

my_patients = Path("my_patients")
my_patients.mkdir(exist_ok=True)

class Patient:

    def __init__(self, name, sex, age, height, diagnose, target):
        self.name = name
        self.sex = sex
        self.age = age
        self.height = height
        self.diagnose = diagnose
        self.target = target
        self.ibw = None
        self.osm = None
        self.defizit = None
        self.infusion_target = None

        self.osm_comment = ""
        self.recommendation = ""

        self.analyse = {
            "Na": None, 
            "glu": None, 
            "urea": None, 
            "Hb": None, 
            "Ht": None, 
            "K": None, 
            "pH": None, 
            "pCO2": None, 
            "HCO3": None, 
            "BE": None
            }
        self.parameters = {
           "temp": None,
           "blood pressure": None,
           "pulse": None,
           "diuresis": None
       }
        
        self.history = {}

    def ibw_calc(self):
        try:
            if self.sex == "f":
                self.ibw = round(45.5 + 0.91 * (self.height - 152.4))
                
            elif self.sex == "m":
                self.ibw = round(50 + 0.91 * (self.height - 152.4))
                
            return self.ibw
        
        except Exception as e:
            print("IBW Calc:", type(e), e)


    def dehydro1(self):
        try:
            defizit_Na = 0.2 * self.ibw * (142 - self.analyse["Na"])
            replenishmentNa = round(self.ibw + defizit_Na)
            mlNaCl09 = round(1000 * replenishmentNa / 154)

            self.recommendation = (f"Na-Bedarf: {replenishmentNa} mmol/d\n"f"Recommended therapy: 0.9% NaCl {mlNaCl09} ml")

            defizit_water = 0

            return defizit_water
        
        except Exception as e: 
            print("Dehydro1:", type(e),e)

    def dehydro2(self):
            try:
                Ht = self.analyse["Ht"] / 100
                if Ht > 0.40:

                    defizit_water = round((0.2 * self.ibw * (Ht - 0.40)) * 1000)

                    self.recommendation = f"Wasser-Defizit - {defizit_water} ml//d"
                    
                    return defizit_water
                
                else:
                    self.recommendation = "No relevant water deficit detected" 
                    defizit_water = 0
                    return defizit_water
                
            except Exception as e: 
                print("Dehydro2:", type(e),e)    

    def dehydro3(self):
        try:
            defizit_water = round(((0.6 * self.ibw * (self.analyse["Na"] - 142)) / self.analyse["Na"]) * 1000) 

            self.recommendation = (f"Wasser-Defizit - {defizit_water} ml\n""5% /Glukose - Medikament der Wahl") 

            return defizit_water
        
        except Exception as e: 
            print("Dehydro3:", type(e),e)

    def osm_calc(self):
                try:
                    self.osm = round(2 * self.analyse["Na"] + (self.analyse["glu"] / 18) + (self.analyse["urea"] / 2.8))

                    if self.osm < 275:
                        self.osm_comment = "Natrium defizit! Hypoosmolarität!"
                      
                        self.defizit = self.dehydro1()
                    
                    elif self.osm > 295:
                        self.osm_comment = "Hyperosmolarität! Vorsicht mit Natrium gabe!"
                        self.defizit = self.dehydro3()
                        
                    else:
                        self.osm_comment = "Normale Osmolarität"
                        self.defizit = self.dehydro2()
                    
                    return self.defizit
                
                except Exception as e:
                    print("Osm Calc:", type(e), e)

    def infusion_calc(self):
        try:
            perspiration = 0.5 * self.ibw * 24
            temp = self.parameters["temp"]
            diuresis = self.parameters["diuresis"] or 0
            if temp is not None and temp > 38:
                perspiration += 500 * (temp - 38)

            if self.target == 0:
                self.infusion_target = round(30 * self.ibw + perspiration + self.defizit + diuresis)
                print(f"Infusion-Ziel: {self.infusion_target} ml/d")

            elif self.target < 0:
                self.infusion_target = round(30 * self.ibw + perspiration + self.defizit)
                print(f"Infusion-Ziel: {self.infusion_target} ml/d")

            elif self.target > 0:
                self.infusion_target = round(30* self.ibw + perspiration + self.defizit + diuresis)
                print(f"Infusion-Ziel: {self.infusion_target} ml/d")

            return self.infusion_target
        
        except Exception as e: 
            print("infusion target:", type(e),e)    

    def update_analyse(self, key, value):
        self.analyse[key] = value

    def update_parameters(self, key, value):
        self.parameters[key] = value


    def save_data(self, date=None):
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        self.history[date] = {
        "name": self.name,
        "sex": self.sex,
        "age": self.age,
        "height": self.height,
        "diagnose": self.diagnose,
        "target": self.target,
        "analyse": self.analyse.copy(),
        "parameters": self.parameters.copy(),
        "ibw": self.ibw,
        "osm": self.osm,
        "defizit": self.defizit,
        "infusion target": self.infusion_target,
        "osm comment": self.osm_comment,
        "recommendation": self.recommendation
        }

    def save_to_json(self):
        filename = my_patients / f"{self.name}.json"
        data = {
        
        "name": self.name,
        "sex": self.sex,
        "age": self.age,
        "height": self.height,
        "diagnose": self.diagnose,
        "target": self.target,
        "analyse": self.analyse,
        "parameters": self.parameters,
        "ibw": self.ibw,
        "osm": self.osm,
        "defizit": self.defizit,
        "infusion target": self.infusion_target,
        "osm comment": self.osm_comment,
        "recommendation": self.recommendation,
        "history": self.history,
            

        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f"Data von {self.name} ist in {filename} gespeichert")