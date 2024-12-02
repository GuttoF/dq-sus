# Flowchart

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

    NOTIFICATIONS_INFO ||--o{ SINAN_INTERNAL_INFO : "connected by notification_id"

    NOTIFICATIONS_INFO ||--o{ CLINICAL_SIGNS : "connected by notification_id"



    NOTIFICATIONS_INFO ||--o{ ALARM_SEVERITIES : "connected by notification_id"


````
