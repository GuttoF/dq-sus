<!-- markdownlint-disable MD024 -->
# PyZDC

[![CI](https://img.shields.io/github/actions/workflow/status/GuttoF/dq-sus/ci.yaml?branch=main&logo=github&label=CI)](https://github.com/GuttoF/dq-sus/actions?query=event%3Apush+branch%3Amain+workflow%3ACI)
[![License](https://img.shields.io/github/license/GuttoF/dq-sus.svg)](https://github.com/GuttoF/dq-sus/blob/main/LICENSE)

## **Introduction**

**PyZDC** is a Python package that helps you work with health data, specifically for diseases like **Dengue**, **Zika**, and **Chikungunya**. It simplifies data extraction, transformation, and loading (ETL) from **SINAN**, a Brazilian epidemiological database.

The package is designed to be **easy to use**, even for beginners in programming.

---

## **Installation**

You can install PyZDC using:

```bash
pip install pyzdc
```

If you use `uv` or `poetry`:

```bash
# uv
uv add pyzdc

# poetry
poetry add pyzdc
```

---

## **How to Use PyZDC**

### **1. `get_years(disease)`**

This function tells you which years have data available for a disease.

#### **Parameters:**

- `disease` (str): The disease you want to check. Must be one of "DENG", "ZIKA", or "CHIK".

#### **Example of `get_notifications`:**

```python
import pyzdc as zdc

zdc.get_years("DENG")  # Output: "The available data for dengue is from 2015 to 2023."
```

#### **Possible Errors:**

- If you pass an invalid disease name, you’ll get an error message: "Error: Only DENG, ZIKA, and CHIK are allowed."

---

### **2. `get_notifications(years, disease, limit)`**

Gets notification records for a disease in a given year.

#### **Parameters:**

- `years` (list of int): The years you want data for (e.g., `[2022, 2023]`).
- `disease` (str): The disease name ("DENG", "ZIKA", or "CHIK").
- `limit` (int, optional): The number of records to return. If `None`, it gets all available data.

#### **Example:**

```python
df = zdc.get_notifications(years=[2022], disease="CHIK", limit=100)
print(df.head())
```

#### **Possible Errors:**

- If no data exists for your filters, an empty DataFrame is returned.

---

### **3. `get_personal_data(years, disease, limit)`**

Gets anonymized personal data of patients.

#### **Parameters:**

- `years`, `disease`, `limit`: Same as `get_notifications()`.

#### **Example:**

```python
df = zdc.get_personal_data(years=[2023], disease="DENG", limit=50)
```

---

### **4. `get_clinical_signs(years, disease, limit)`**

Retrieves clinical symptoms of reported cases.

#### **Example:**

```python
df = zdc.get_clinical_signs(years=[2021, 2022], disease="ZIKA")
```

---

### **5. `get_patient_diseases(years, disease, limit)`**

Gets information about other diseases patients have.

#### **Example:**

```python
df = zdc.get_patient_diseases(years=[2023], disease="CHIK")
```

---

### **6. `get_exams(years, disease, limit)`**

Gets laboratory test results.

#### **Example:**

```python
df = zdc.get_exams(years=[2023], disease="DENG")
```

---

### **7. `get_hospital_info(years, disease, limit)`**

Retrieves hospitalization details.

#### **Example:**

```python
df = zdc.get_hospital_info(years=[2020, 2021], disease="CHIK")
```

---

### **8. `get_alarm_severities(years, disease, limit)`**

Gets cases classified as severe.

#### **Example:**

```python
df = zdc.get_alarm_severities(years=[2022], disease="DENG")
```

---

### **9. `get_sinan_info(years, disease, limit)`**

Returns raw SINAN database records.

#### **Example:**

```python
df = zdc.get_sinan_info(years=[2023], disease="CHIK")
```

---

## **Common Errors and Solutions**

### **1. No Data Available**

If the dataset is empty for your filters, you will get an empty DataFrame.

**Solution:** Use `get_years()` to check available data before querying.

### **2. Invalid Disease Code**

If you enter a disease name that isn't "DENG", "ZIKA", or "CHIK", you will see an error.

**Solution:** Use only the supported disease codes.

---

## **Conclusion**

PyZDC makes it easy to extract and analyze epidemiological data. Whether you are a beginner or an advanced user, these functions help you get insights quickly.

For more details, visit: [GitHub Repository](https://github.com/GuttoF/dq-sus).
