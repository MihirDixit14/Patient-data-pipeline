-- Q2: Patients readmitted within 30 days of a previous discharge
SELECT e1.patient_id,
        e1.encounter_id AS first_encounter,
        e1.discharge_date AS first_discharge,
        e2.encounter_id AS readmission_encounter,
        e2.admission_date AS readmission_date,
        CAST(julianday(e2.admission_date)-julianday(e1.discharge_date)
        AS INTEGER ) AS days_between

FROM encounters e1 JOIN encounters e2 ON e1.patient_id=e2.patient_id
            AND e2.admission_date>e1.discharge_date
            AND julianday(e2.admission_date)-julianday(e1.discharge_date)<=30
WHERE e1.discharge_date is NOT NULL
ORDER BY e1.patient_id,days_between;
