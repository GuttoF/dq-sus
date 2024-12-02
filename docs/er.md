# Modelagem de DataFrame

No total, são oito DataFrames, todos vêm de um banco de dados DuckDB.

## Modelo ER

```mermaid
%%{init: {"themeVariables": {"fontFamily": "Times New Roman, Times, serif"}}}%%
%%{init: {'theme':'neutral'}}%%

erDiagram
    NOTIFICATIONS_INFO {
        string notification_id
        string notification_type
        string disease_condition_id
        string notification_date
        string notification_week
        string notification_year
        string notification_state_id
        string notification_city_id
        string notification_region_id
        string notification_health_unit_id
    }

    SINAN_INTERNAL_INFO {
        string notification_id
        string lot_number
        string system_type
        string duplicated_number
        string typing_date
        string record_enabled_send
        string computer_id
        string windows_migration
    }

    PATIENTS_DISEASES {
        string notification_id
        string diabetes
        string hematological_diseases
        string hepatopathies
        string renal_diseases
        string hypertension
        string peptic_ulcer
        string autoimmune_diseases
    }

    CLINICAL_SIGNS {
        string notification_id
        string clinical_signs_fever
        string clinical_signs_myalgia
        string clinical_signs_headache
        string clinical_signs_rash
        string clinical_signs_vomiting
        string clinical_sign_nausea
        string clinical_sign_back_pain
        string clinical_sign_conjunctivitis
        string clinical_sign_arthritis
        string clinical_sign_arthralgia
        string clinical_sign_petechiae
        string clinical_sign_leukopenia
        string clinical_sign_orbital_pain
    }

    PERSONAL_DATA {
        string notification_id
        string symptoms_onset_date
        string symptoms_onset_week
        string age
        string birth_date
        string gender
        string pregnancy_status
        string education_level
        string ethnicity
        string country_of_residence
        string state_of_residence
        string city_of_residence
        string region_of_residence
        string country_of_residence
        string investigation_date
        string occupation_or_activity_field
    }

    HOSPITAL_INFO {
        string notification_id
        string hospitalization
        string hospitalization_date
        string state_of_the_hospital
        string city_of_the_hospital
        string autochthonous_case_of_residence
        string country_of_the_infection
        string country_of_the_infection_id
        string infection_city_id
        string final_classification
        string classification_criteria
        string work_related_case
        string clinical_classification_chikungunya
        string death_date
        string evolution_case
        string case_close_case
    }

    EXAMS {
        string notification_id
        string laco_test
        string if_patient_did_laco_test
        string igm_chikungunya_serum_1_date
        string igm_chikungunya_serum_1_result
        string igm_chikungunya_serum_2_date
        string igm_chikungunya_serum_2_result
        string prnt_test_date
        string prnt_test_result
        string serological_test_igm_dengue_date
        string serological_test_igm_dengue_result
        string ns1_test_date
        string ns1_test_result
        string viral_isolation_date
        string viral_isolation_result
        string rt_pcr_date
        string rt_pcr_result
        string serotype
        string histopathology_result
        string immunohistochemistry_result
        string plasmatic_value
        string evidence
        string platelet_count
        string fdh_scd_degree
    }

    ALARM_SEVERITIES {
        string notification_id
        string hypotension_alarm
        string platelet_alarm
        string vomiting_alarm
        string bleeding_alarm
        string lethargy_alarm
        string hematocrit_alarm
        string abdominal_pain_alarm
        string lethargy_alarm_1
        string hepatomegaly_alarm
        string liquid_alarm
        string alarm_dengue_date
        string pulse_severity
        string convergence_pressure_severity
        string capilar_enchiment_severity
        string respiratory_insufficiency_liquid_severity
        string tachycardia_severity
        string extremity_coldness_severity
        string hypotension_severity
        string hematemesis_severity
        string melena_severity
        string metrorrhagia_severity
        string bleeding_severity
        string higher_ast_alt_severity
        string myocarditis_severity
        string consciousness_severity
        string other_organs_severity
        string severity_date
        string hemorrhaegic_manifestations
        string epistaxis
        string gengival_bleeding
        string metrorrhagia
        string petechiae
        string hematuria
        string bleeding
        string complications
    }
````
