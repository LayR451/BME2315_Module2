# created a patient class to make my life easier. Only includes the attributes I need for my tests
import csv 

class Patient:

    all_patients = []

    def __init__(self, subject_id: int, ff_baseline_R: float, ff_y1_R: float, ff_y2_R: float, ff_baseline_L: float, ff_y1_L: float, ff_y2_L: float, clinical_severity_score_baseline: int, clinical_severity_score_y1: int, clinical_severity_score_y2: int, lag_months_baseline: float, lag_months_y1: float, lag_months_y2: float):
        self.subject_id = subject_id  
        self.ff_baseline_R = ff_baseline_R  #fat fraction right baseline
        self.ff_y1_R = ff_y1_R  #fat fraction right year 1
        self.ff_y2_R = ff_y2_R  #fat fraction right year 2
        self.ff_baseline_L = ff_baseline_L  #fat fraction left baseline
        self.ff_y1_L = ff_y1_L  #fat fraction left year 1
        self.ff_y2_L = ff_y2_L  #fat fraction left year 2
        self.clinical_severity_score_baseline = clinical_severity_score_baseline  #clinical severity score baseline
        self.clinical_severity_score_y1 = clinical_severity_score_y1  #clinical severity score year 1
        self.clinical_severity_score_y2 = clinical_severity_score_y2  #clinical severity score year 2
        self.lag_months_baseline = lag_months_baseline  #month of first visit
        self.lag_months_y1 = lag_months_y1 # month of year 1 visit  
        self.lag_months_y2 = lag_months_y2  # month of year 2 visit

        
    @classmethod
    def instantiate_from_csv(cls, filename: str):
        patients = []

        with open(filename, encoding="utf8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                patient = cls(
                    subject_id=row["subject_id"],
                    ff_baseline_R=row["ff_baseline_R"],
                    ff_y1_R=row["ff_y1_R"],
                    ff_y2_R=row["ff_y2_R"],
                    ff_baseline_L=row["ff_baseline_L"],
                    ff_y1_L=row["ff_y1_L"],
                    ff_y2_L=row["ff_y2_L"],
                    clinical_severity_score_baseline=row["clinical_severity_score_baseline"],
                    clinical_severity_score_y1=row["clinical_severity_score_y1"],
                    clinical_severity_score_y2=row["clinical_severity_score_y2"],
                    lag_months_baseline=row["lag_months_baseline"],
                    lag_months_y1=row["lag_months_y1"],
                    lag_months_y2=row["lag_months_y2"]
                )

                patients.append(patient)

        cls.all_patients.extend(patients)
        return patients


    def __repr__(self):
        return f"Patient({self.subject_id}, {self.ff_baseline_R}, {self.ff_y1_R}, {self.ff_y2_R}, {self.ff_baseline_L}, {self.ff_y1_L}, {self.ff_y2_L}, {self.clinical_severity_score_baseline}, {self.clinical_severity_score_y1}, {self.clinical_severity_score_y2}, {self.lag_months_baseline}, {self.lag_months_y1}, {self.lag_months_y2})"


    def create_Patient(self):
        return Patient(
            self.subject_id,
            self.ff_baseline_R,
            self.ff_y1_R,
            self.ff_y2_R,
            self.ff_baseline_L,
            self.ff_y1_L,
            self.ff_y2_L,
            self.clinical_severity_score_baseline,
            self.clinical_severity_score_y1,
            self.clinical_severity_score_y2,
            self.lag_months_baseline,
            self.lag_months_y1,
            self.lag_months_y2
        )


    def year1_visit(self):
        return {
            "lag_months": self.lag_months_y1
         }

    def year2_visit(self):
        return {
            "lag_months": self.lag_months_y2
         }