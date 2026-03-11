# main.py

import json
import customtkinter as CTk

from patient import Patient
from storage import load_patients, calc_all, save_all_patients, read_json


CTk.set_appearance_mode("light")
CTk.set_default_color_theme("blue")


class App(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.patients = load_patients()

        self.geometry("1100x760")
        self.title("Intensive Station")
        self.resizable(False, False)
        self.configure(fg_color="#f3f5f7")

        self.build_main_menu()

    def build_main_menu(self):
        outer_frame = CTk.CTkFrame(self, fg_color="transparent")
        outer_frame.pack(fill="both", expand=True, padx=60, pady=50)

        menu_card = CTk.CTkFrame(
            outer_frame,
            width=780,
            height=520,
            corner_radius=18,
            fg_color="#ffffff"
        )
        menu_card.pack(expand=True)
        menu_card.pack_propagate(False)

        title = CTk.CTkLabel(
            menu_card,
            text="Menu",
            font=("Arial", 34, "bold"),
            text_color="#1f1f1f"
        )
        title.pack(pady=(55, 50))

        btn_style = {
            "width": 620,
            "height": 58,
            "font": ("Arial", 20),
            "corner_radius": 12
        }

        CTk.CTkButton(
            menu_card,
            text="Neue Aufnahme",
            command=self.pat_registr,
            **btn_style
        ).pack(pady=16)

        CTk.CTkButton(
            menu_card,
            text="Patienten auf der Station",
            command=self.load_pat,
            **btn_style
        ).pack(pady=16)

        CTk.CTkButton(
            menu_card,
            text="Speicherung und Exit",
            command=self.exit_and_save,
            **btn_style
        ).pack(pady=16)

    def exit_and_save(self):
        save_all_patients(self.patients)
        self.destroy()

    def pat_registr(self):
        new_window = CTk.CTkToplevel(self)
        new_window.title("Neue Aufnahme")
        new_window.geometry("1180x860")
        new_window.resizable(False, False)
        new_window.configure(fg_color="#eef3f7")

        main_frame = CTk.CTkFrame(new_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_card = CTk.CTkFrame(
            main_frame,
            width=520,
            height=780,
            corner_radius=18,
            fg_color="#25a0c9"
        )
        left_card.pack(side="left", fill="y", padx=(0, 20))
        left_card.pack_propagate(False)

        right_card = CTk.CTkFrame(
            main_frame,
            width=560,
            height=780,
            corner_radius=18,
            fg_color="#ffffff"
        )
        right_card.pack(side="left", fill="both", expand=True)
        right_card.pack_propagate(False)

        title_label = CTk.CTkLabel(
            left_card,
            text="Enter patient data",
            font=("Arial", 30, "bold"),
            text_color="#111111"
        )
        title_label.pack(anchor="w", padx=35, pady=(24, 16))

        entry_style = {
            "width": 430,
            "height": 36,
            "corner_radius": 10
        }

        p_name = CTk.CTkEntry(left_card, placeholder_text="Name", **entry_style)
        p_name.pack(pady=5, padx=35, anchor="w")

        p_sex = CTk.CTkEntry(left_card, placeholder_text="Sex (f/m)", **entry_style)
        p_sex.pack(pady=5, padx=35, anchor="w")

        p_age = CTk.CTkEntry(left_card, placeholder_text="Age", **entry_style)
        p_age.pack(pady=5, padx=35, anchor="w")

        p_height = CTk.CTkEntry(left_card, placeholder_text="Height", **entry_style)
        p_height.pack(pady=5, padx=35, anchor="w")

        p_diagnose = CTk.CTkEntry(left_card, placeholder_text="Diagnose", **entry_style)
        p_diagnose.pack(pady=5, padx=35, anchor="w")

        p_wb_target = CTk.CTkEntry(left_card, placeholder_text="Water balance target", **entry_style)
        p_wb_target.pack(pady=5, padx=35, anchor="w")

        p_Na = CTk.CTkEntry(left_card, placeholder_text="Na", **entry_style)
        p_Na.pack(pady=5, padx=35, anchor="w")

        p_glu = CTk.CTkEntry(left_card, placeholder_text="glu", **entry_style)
        p_glu.pack(pady=5, padx=35, anchor="w")

        p_urea = CTk.CTkEntry(left_card, placeholder_text="urea", **entry_style)
        p_urea.pack(pady=5, padx=35, anchor="w")

        p_Ht = CTk.CTkEntry(left_card, placeholder_text="Ht", **entry_style)
        p_Ht.pack(pady=5, padx=35, anchor="w")

        p_temp = CTk.CTkEntry(left_card, placeholder_text="temp", **entry_style)
        p_temp.pack(pady=5, padx=35, anchor="w")

        p_diuresis = CTk.CTkEntry(left_card, placeholder_text="diuresis", **entry_style)
        p_diuresis.pack(pady=5, padx=35, anchor="w")

        save_btn = CTk.CTkButton(
            left_card,
            text="Patienten Speichern",
            text_color="black",
            width=430,
            height=46,
            fg_color="#E3EA21",
            hover_color="#d3d71d",
            font=("Arial", 18, "bold"),
            corner_radius=10,
            command=lambda: save_p()
        )
        save_btn.pack(pady=(18, 0), padx=35, anchor="w")

        result_title = CTk.CTkLabel(
            right_card,
            text="Calculation Result",
            font=("Arial", 28, "bold"),
            text_color="#111111"
        )
        result_title.pack(anchor="w", padx=30, pady=(28, 18))

        result_box = CTk.CTkTextbox(
            right_card,
            width=500,
            height=640,
            font=("Courier", 15),
            corner_radius=12,
            fg_color="#f7f8fa",
            text_color="#1f1f1f"
        )
        result_box.pack(anchor="w", padx=30, pady=(0, 20))

        def save_p():
            try:
                name = p_name.get().strip()
                sex = p_sex.get().strip().lower()
                age = int(p_age.get())
                height = float(p_height.get())
                diagnose = p_diagnose.get().strip()
                target = int(p_wb_target.get())

                Na = float(p_Na.get())
                glu = float(p_glu.get())
                urea = float(p_urea.get())
                Ht = float(p_Ht.get())
                temp = float(p_temp.get())
                diuresis = float(p_diuresis.get())

                if not name:
                    raise ValueError("Name required")
                if sex not in ["f", "m"]:
                    raise ValueError("Sex must be 'f' or 'm'")

                p = Patient(name, sex, age, height, diagnose, target)

                p.analyse["Na"] = Na
                p.analyse["glu"] = glu
                p.analyse["urea"] = urea
                p.analyse["Ht"] = Ht

                p.parameters["temp"] = temp
                p.parameters["diuresis"] = diuresis

                ibw = p.ibw_calc()
                osm = p.osm_calc()
                infusion_target = p.infusion_calc()

                p.save_data()
                p.save_to_json()
                self.patients[name] = p

                result_box.delete("1.0", "end")
                result_box.insert(
                    "1.0",
                    f"Patient saved\n\n"
                    f"Name: {name}\n"
                    f"Diagnose: {diagnose}\n\n"
                    f"IBW: {ibw} kg\n"
                    f"Wasser-Defizit: {osm}\n"
                    f"Status: {p.osm_comment}\n\n"
                    f"{p.recommendation}\n\n"
                    f"Infusion-Ziel: {infusion_target} ml/d"
                )

            except ValueError:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "Enter valid numeric values.")
            except Exception as e:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", str(e))

    def load_pat(self):
        new_window2 = CTk.CTkToplevel(self)
        new_window2.title("Read and update")
        new_window2.geometry("1180x860")
        new_window2.resizable(False, False)
        new_window2.configure(fg_color="#eef3f7")

        patients = self.patients

        main_frame = CTk.CTkFrame(new_window2, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        left_card = CTk.CTkFrame(
            main_frame,
            width=520,
            height=780,
            corner_radius=18,
            fg_color="#01c7a6"
        )
        left_card.pack(side="left", fill="y", padx=(0, 20))
        left_card.pack_propagate(False)

        right_card = CTk.CTkFrame(
            main_frame,
            width=560,
            height=780,
            corner_radius=18,
            fg_color="#ffffff"
        )
        right_card.pack(side="left", fill="both", expand=True)
        right_card.pack_propagate(False)

        label2 = CTk.CTkLabel(
            left_card,
            text="Read and update patient",
            font=("Arial", 28, "bold"),
            text_color="#111111"
        )
        label2.pack(anchor="w", padx=35, pady=(28, 20))

        entry_style = {
            "width": 430,
            "height": 40,
            "corner_radius": 10
        }

        p_name = CTk.CTkEntry(left_card, placeholder_text="Name", **entry_style)
        p_name.pack(pady=7, padx=35, anchor="w")

        labelA = CTk.CTkLabel(
            left_card,
            text="Add or update analyse",
            font=("Arial", 20, "bold"),
            text_color="#111111"
        )
        labelA.pack(anchor="w", padx=35, pady=(16, 8))

        analyse_key = CTk.CTkEntry(left_card, placeholder_text="Analyse name (Na, glu...)", **entry_style)
        analyse_key.pack(pady=7, padx=35, anchor="w")

        analyse_value = CTk.CTkEntry(left_card, placeholder_text="Analyse value", **entry_style)
        analyse_value.pack(pady=7, padx=35, anchor="w")

        btnA = CTk.CTkButton(
            left_card,
            text="Update Analyse",
            text_color="black",
            width=430,
            height=46,
            fg_color="#F4385A",
            hover_color="#d92d4d",
            font=("Arial", 16, "bold"),
            corner_radius=10,
            command=lambda: updateA()
        )
        btnA.pack(pady=(10, 18), padx=35, anchor="w")

        labelP = CTk.CTkLabel(
            left_card,
            text="Add or update parameters",
            font=("Arial", 20, "bold"),
            text_color="#111111"
        )
        labelP.pack(anchor="w", padx=35, pady=(8, 8))

        parameters_key = CTk.CTkEntry(left_card, placeholder_text="Parameter name (temp, pulse...)", **entry_style)
        parameters_key.pack(pady=7, padx=35, anchor="w")

        parameters_value = CTk.CTkEntry(left_card, placeholder_text="Parameter value", **entry_style)
        parameters_value.pack(pady=7, padx=35, anchor="w")

        btnP = CTk.CTkButton(
            left_card,
            text="Update Parameter",
            text_color="black",
            width=430,
            height=46,
            fg_color="#7954B0",
            hover_color="#68449a",
            font=("Arial", 16, "bold"),
            corner_radius=10,
            command=lambda: updateP()
        )
        btnP.pack(pady=(10, 18), padx=35, anchor="w")

        btnR = CTk.CTkButton(
            left_card,
            text="Patient history open",
            text_color="black",
            width=430,
            height=46,
            fg_color="#CCCF2C",
            hover_color="#b8bb25",
            font=("Arial", 16, "bold"),
            corner_radius=10,
            command=lambda: read()
        )
        btnR.pack(pady=(10, 12), padx=35, anchor="w")

        btnS = CTk.CTkButton(
            left_card,
            text="Calculate",
            text_color="black",
            width=430,
            height=46,
            fg_color="#57E77B",
            hover_color="#47cf69",
            font=("Arial", 16, "bold"),
            corner_radius=10,
            command=lambda: calculate_all_gui()
        )
        btnS.pack(pady=(8, 0), padx=35, anchor="w")

        result_title = CTk.CTkLabel(
            right_card,
            text="Result / Status",
            font=("Arial", 28, "bold"),
            text_color="#111111"
        )
        result_title.pack(anchor="w", padx=30, pady=(28, 18))

        result_box = CTk.CTkTextbox(
            right_card,
            width=500,
            height=640,
            font=("Courier", 15),
            corner_radius=12,
            fg_color="#f7f8fa",
            text_color="#1f1f1f"
        )
        result_box.pack(anchor="w", padx=30, pady=(0, 20))

        def updateA():
            name = p_name.get().strip()
            key = analyse_key.get().strip()
            value = analyse_value.get().strip()

            if name not in patients:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", f"Patient {name} not found")
                return

            try:
                value = float(value)
            except ValueError:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "Enter a number")
                return

            try:
                p = patients[name]
                p.update_analyse(key, value)
                p.ibw_calc()
                osm = p.osm_calc()
                infusion_target = p.infusion_calc()
                p.save_data()
                p.save_to_json()

                result_box.delete("1.0", "end")
                result_box.insert(
                    "1.0",
                    f"{key} = {value} saved for {name}\n\n"
                    f"Wasser-Defizit: {osm}\n"
                    f"Status: {p.osm_comment}\n\n"
                    f"{p.recommendation}\n\n"
                    f"Infusion-Ziel: {infusion_target} ml/d"
                )

            except Exception as e:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", f"Update error: {e}")

        def updateP():
            name = p_name.get().strip()
            key = parameters_key.get().strip()
            value = parameters_value.get().strip()

            if name not in patients:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", f"Patient {name} not found")
                return

            try:
                value = float(value)
            except ValueError:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "Enter a number")
                return

            try:
                p = patients[name]
                p.update_parameters(key, value)
                p.ibw_calc()
                osm = p.osm_calc()
                infusion_target = p.infusion_calc()
                p.save_data()
                p.save_to_json()

                result_box.delete("1.0", "end")
                result_box.insert(
                    "1.0",
                    f"{key} = {value} saved for {name}\n\n"
                    f"Wasser-Defizit: {osm}\n"
                    f"Status: {p.osm_comment}\n\n"
                    f"{p.recommendation}\n\n"
                    f"Infusion-Ziel: {infusion_target} ml/d"
                )

            except Exception as e:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", f"Update error: {e}")

        def read():
            name = p_name.get().strip()

            if not name:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", "Enter patient name")
                return

            patient = read_json(name)
            if patient is None:
                result_box.delete("1.0", "end")
                result_box.insert("1.0", f"Patient {name} not found")
                return

            hist_window = CTk.CTkToplevel(new_window2)
            hist_window.title(f"{name} - History")
            hist_window.geometry("950x900")

            text_box = CTk.CTkTextbox(
                hist_window,
                wrap="word",
                font=("Courier", 14),
                fg_color="#54c7b4"
            )
            text_box.pack(fill="both", expand=True, padx=20, pady=20)

            text_box.insert("1.0", json.dumps(patient.history, indent=4, ensure_ascii=False))
            text_box.configure(state="disabled")

        def calculate_all_gui():
            message = calc_all(patients)
            result_box.delete("1.0", "end")
            result_box.insert("1.0", message)


if __name__ == "__main__":
    app = App()
    app.mainloop()
