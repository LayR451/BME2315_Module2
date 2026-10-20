# created a patient class to make my life easier. Only includes the attributes I need for my tests

class Patient:
    def __init__(self, patient_id, ff_baseline_R,ff_y1_R,ff_y2_R,ff_baseline_L,ff_y1_L,ff_y2_L,dorsiflexion_qmt_R_baseline,dorsiflexion_qmt_R_y1,dorsiflexion_qmt_R_y2,dorsiflexion_qmt_L_baseline,dorsiflexion_qmt_L_y1,dorsiflexion_qmt_L_y2, lag_months_baseline,lag_months_y1,lag_months_y2):
        self.patient_id = patient_id  
        self.ff_baseline_R = ff_baseline_R  #fat fraction right baseline
        self.ff_y1_R = ff_y1_R  #fat fraction right year 1
        self.ff_y2_R = ff_y2_R  #fat fraction right year 2
        self.ff_baseline_L = ff_baseline_L  #fat fraction left baseline
        self.ff_y1_L = ff_y1_L  #fat fraction left year 1
        self.ff_y2_L = ff_y2_L  #fat fraction left year 2
        self.dorsiflexion_qmt_R_baseline = dorsiflexion_qmt_R_baseline  #dorsiflexion QMT right baseline
        self.dorsiflexion_qmt_R_y1 = dorsiflexion_qmt_R_y1  #dorsiflexion QMT right year 1
        self.dorsiflexion_qmt_R_y2 = dorsiflexion_qmt_R_y2  #dorsiflexion QMT right year 2
        self.dorsiflexion_qmt_L_baseline = dorsiflexion_qmt_L_baseline  #dorsiflexion QMT left baseline
        self.dorsiflexion_qmt_L_y1 = dorsiflexion_qmt_L_y1  #dorsiflexion QMT left year 1
        self.dorsiflexion_qmt_L_y2 = dorsiflexion_qmt_L_y2  #dorsiflexion QMT left year 2
        self.lag_months_baseline = lag_months_baseline  #month of first visit
        self.lag_months_y1 = lag_months_y1 # month of year 1 visit  
        self.lag_months_y2 = lag_months_y2  # month of year 2 visit

    def __repr__(self):
        return f"Patient({self.patient_id}, {self.ff_baseline_R}, {self.ff_y1_R}, {self.ff_y2_R}, {self.ff_baseline_L}, {self.ff_y1_L}, {self.ff_y2_L}, {self.dorsiflexion_qmt_R_baseline}, {self.dorsiflexion_qmt_R_y1}, {self.dorsiflexion_qmt_R_y2}, {self.dorsiflexion_qmt_L_baseline}, {self.dorsiflexion_qmt_L_y1}, {self.dorsiflexion_qmt_L_y2}, {self.lag_months_baseline}, {self.lag_months_y1}, {self.lag_months_y2})"


    def create_Patient(self):
        return Patient(
            self.patient_id,
            self.ff_baseline_R,
            self.ff_y1_R,
            self.ff_y2_R,
            self.ff_baseline_L,
            self.ff_y1_L,
            self.ff_y2_L,
            self.dorsiflexion_qmt_R_baseline,
            self.dorsiflexion_qmt_R_y1,
            self.dorsiflexion_qmt_R_y2,
            self.dorsiflexion_qmt_L_baseline,
            self.dorsiflexion_qmt_L_y1,
            self.dorsiflexion_qmt_L_y2,
            self.lag_months_baseline,
            self.lag_months_y1,
            self.lag_months_y2
        )