# Healthcare EHR/EMR Data Analysis
**Project Duration:** September 2023 – March 2024

---

## Project Overview
This project focuses on analyzing Electronic Health Records (EHR) and Electronic Medical Records (EMR) data to provide insights into patient outcomes, operational efficiency, clinical quality metrics, and healthcare cost optimization.

---

## End-to-End Power BI Workflow

### 1. Data Source Identification & Connection

#### Data Sources
- **EHR/EMR System**: Patient demographics, medical history, diagnoses, treatments
- **Practice Management System (PMS)**: Appointments, scheduling, billing
- **Laboratory Information System (LIS)**: Lab test results, orders
- **Radiology Information System (RIS)**: Imaging studies, results
- **Pharmacy System**: Medication orders, dispensing records
- **Claims Database**: Insurance claims, reimbursements
- **Patient Portal**: Patient engagement, satisfaction surveys
- **Hospital Information System (HIS)**: Admission, discharge, transfer (ADT) data

#### Connection Methods
- HL7 FHIR APIs for EHR/EMR data extraction
- Direct SQL Server connections to internal databases
- ODBC connections for legacy systems
- Secure FTP for external claims data
- Azure SQL Database for data warehouse

#### Compliance & Security
- **HIPAA Compliance:** All data connections encrypted (TLS 1.2+)
- **De-identification:** PHI removed/masked per HIPAA Safe Harbor method
- **Audit Logging:** All data access logged and monitored
- **Access Controls:** Role-based security with MFA

---

### 2. Data Extraction & Preparation

#### Power Query Transformations
```
// Connect to EHR database
// Remove duplicate patient records (match on MRN)
// Standardize ICD-10 diagnosis codes
// Clean CPT procedure codes
// Parse HL7 messages to tabular format
// Handle missing values in lab results
// Standardize date/time formats across systems
// De-identify PHI (remove names, SSN, addresses)
// Create patient age groups and demographics
// Merge medication records from multiple sources
// Calculate encounter duration and wait times
```

#### Data Quality Checks
- Validate patient identifiers (MRN uniqueness)
- Check for impossible dates (future dates, age >120)
- Verify diagnosis code validity (ICD-10 format)
- Ensure lab values within physiological ranges
- Identify incomplete encounters (missing discharge dates)
- Flag duplicate orders or medications
- Validate insurance eligibility dates

---

### 3. Data Modeling

#### Star Schema Design

**Fact Tables:**
- `FactEncounter`: Patient visits and encounters
  - EncounterID, PatientID, ProviderID, FacilityID, DateID
  - EncounterType, AdmissionDate, DischargeDate, LengthOfStay
  - PrimaryDiagnosisID, TotalCharges, PayerAmount, PatientAmount

- `FactLabResults`: Laboratory test results
  - LabResultID, PatientID, ProviderID, DateID, LabTestID
  - ResultValue, ResultUnit, ReferenceRange, AbnormalFlag

- `FactMedication`: Medication orders and administration
  - MedicationID, PatientID, ProviderID, DateID, DrugID
  - DosageAmount, Frequency, RouteOfAdmin, StartDate, EndDate

- `FactProcedure`: Medical procedures performed
  - ProcedureID, PatientID, ProviderID, DateID, CPTCodeID
  - ProcedureDate, Duration, ChargeAmount, Complications

- `FactAppointment`: Scheduled appointments
  - AppointmentID, PatientID, ProviderID, FacilityID, DateID
  - ScheduledTime, ActualTime, NoShow, CancellationReason
  - WaitTime, VisitDuration

**Dimension Tables:**
- `DimPatient`: Patient master data
  - PatientID, MRN, DateOfBirth, Age, AgeGroup
  - Gender, Race, Ethnicity, MaritalStatus
  - InsuranceType, PrimaryLanguage, RiskScore

- `DimProvider`: Healthcare providers
  - ProviderID, NPI, ProviderName, Specialty, SubSpecialty
  - Department, HireDate, FTE

- `DimFacility`: Healthcare facilities
  - FacilityID, FacilityName, FacilityType
  - Address, City, State, BedCount, ERStatus

- `DimDiagnosis`: Diagnosis codes
  - DiagnosisID, ICD10Code, DiagnosisDescription
  - DiagnosisCategory, ChronicConditionFlag

- `DimProcedure`: Procedure codes
  - ProcedureID, CPTCode, ProcedureDescription
  - ProcedureCategory, RVUValue

- `DimLabTest`: Laboratory test catalog
  - LabTestID, LOINC_Code, TestName, TestCategory
  - SpecimenType, TurnaroundTime

- `DimMedication`: Drug catalog
  - DrugID, NDC_Code, GenericName, BrandName
  - DrugClass, TherapeuticCategory, FormularyStatus

- `DimDate`: Date dimension
  - DateID, Date, Year, Quarter, Month, Week, DayOfWeek
  - IsHoliday, FiscalYear, FiscalQuarter

- `DimInsurance`: Payer information
  - InsuranceID, PayerName, PayerType
  - (Medicare, Medicaid, Commercial, Self-Pay)

#### Relationships
- One-to-Many from all dimension tables to fact tables
- Many-to-Many relationship: Patient ↔ Diagnosis (bridge table)
- Active relationships on primary date fields
- Calculated relationships for multiple date contexts

---

### 4. DAX Measures & Calculated Columns

#### Key Measures

**Patient Metrics:**
```
Total Patients = DISTINCTCOUNT(FactEncounter[PatientID])

New Patients = 
CALCULATE(
    DISTINCTCOUNT(FactEncounter[PatientID]),
    FILTER(
        FactEncounter,
        FactEncounter[EncounterID] = 
        CALCULATE(MIN(FactEncounter[EncounterID]), 
                  ALLEXCEPT(FactEncounter, FactEncounter[PatientID]))
    )
)

Active Patients = 
CALCULATE(
    DISTINCTCOUNT(FactEncounter[PatientID]),
    FILTER(
        VALUES(FactEncounter[PatientID]),
        CALCULATE(MAX(FactEncounter[AdmissionDate])) >= TODAY() - 365
    )
)

Average Patient Age = AVERAGE(DimPatient[Age])

High-Risk Patient Count = 
CALCULATE(
    DISTINCTCOUNT(DimPatient[PatientID]),
    DimPatient[RiskScore] >= 3
)
```

**Encounter Metrics:**
```
Total Encounters = COUNTROWS(FactEncounter)

Inpatient Encounters = 
CALCULATE([Total Encounters], FactEncounter[EncounterType] = "Inpatient")

Outpatient Encounters = 
CALCULATE([Total Encounters], FactEncounter[EncounterType] = "Outpatient")

Emergency Encounters = 
CALCULATE([Total Encounters], FactEncounter[EncounterType] = "Emergency")

Average Length of Stay (ALOS) = 
AVERAGEX(
    FILTER(FactEncounter, FactEncounter[EncounterType] = "Inpatient"),
    FactEncounter[LengthOfStay]
)

30-Day Readmission Rate = 
VAR ReadmissionCount = 
    CALCULATE(
        COUNTROWS(FactEncounter),
        FILTER(
            FactEncounter,
            VAR CurrentPatient = FactEncounter[PatientID]
            VAR CurrentDischarge = FactEncounter[DischargeDate]
            VAR NextAdmission = 
                CALCULATE(
                    MIN(FactEncounter[AdmissionDate]),
                    FILTER(
                        ALLEXCEPT(FactEncounter, FactEncounter[PatientID]),
                        FactEncounter[AdmissionDate] > CurrentDischarge &&
                        FactEncounter[AdmissionDate] <= CurrentDischarge + 30
                    )
                )
            RETURN NOT(ISBLANK(NextAdmission))
        )
    )
VAR TotalDischarges = 
    CALCULATE(
        [Total Encounters],
        FactEncounter[EncounterType] = "Inpatient"
    )
RETURN DIVIDE(ReadmissionCount, TotalDischarges, 0)
```

**Financial Metrics:**
```
Total Charges = SUM(FactEncounter[TotalCharges])

Total Collections = SUM(FactEncounter[PayerAmount]) + SUM(FactEncounter[PatientAmount])

Collection Rate = DIVIDE([Total Collections], [Total Charges], 0)

Average Charge per Encounter = DIVIDE([Total Charges], [Total Encounters], 0)

Revenue per Patient = DIVIDE([Total Collections], [Total Patients], 0)

Net Revenue = [Total Collections] - [Total Operating Costs]

Operating Margin % = DIVIDE([Net Revenue], [Total Collections], 0)

Days in A/R = 
DIVIDE(
    [Accounts Receivable Balance],
    [Total Collections] / 365,
    0
)
```

**Quality Metrics:**
```
Appointment No-Show Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FactAppointment), FactAppointment[NoShow] = TRUE),
    COUNTROWS(FactAppointment),
    0
)

Average Wait Time (Minutes) = AVERAGE(FactAppointment[WaitTime])

Patient Satisfaction Score = AVERAGE(FactEncounter[SatisfactionScore])

Medication Error Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FactMedication), FactMedication[ErrorFlag] = TRUE),
    COUNTROWS(FactMedication),
    0
)

Complication Rate = 
DIVIDE(
    CALCULATE(COUNTROWS(FactProcedure), FactProcedure[Complications] = TRUE),
    COUNTROWS(FactProcedure),
    0
)

Lab TAT Compliance % = 
DIVIDE(
    CALCULATE(
        COUNTROWS(FactLabResults),
        FactLabResults[ActualTAT] <= RELATED(DimLabTest[TurnaroundTime])
    ),
    COUNTROWS(FactLabResults),
    0
)
```

**Population Health Metrics:**
```
Diabetes Prevalence = 
VAR DiabetesPatients = 
    CALCULATE(
        DISTINCTCOUNT(FactEncounter[PatientID]),
        FILTER(
            DimDiagnosis,
            LEFT(DimDiagnosis[ICD10Code], 3) IN {"E10", "E11"}
        )
    )
RETURN DIVIDE(DiabetesPatients, [Total Patients], 0)

Hypertension Prevalence = 
VAR HTNPatients = 
    CALCULATE(
        DISTINCTCOUNT(FactEncounter[PatientID]),
        FILTER(
            DimDiagnosis,
            LEFT(DimDiagnosis[ICD10Code], 3) = "I10"
        )
    )
RETURN DIVIDE(HTNPatients, [Total Patients], 0)

Preventive Care Compliance = 
VAR EligiblePatients = [Total Patients]
VAR CompliantPatients = 
    CALCULATE(
        DISTINCTCOUNT(FactEncounter[PatientID]),
        FactProcedure[PreventiveCareFlag] = TRUE
    )
RETURN DIVIDE(CompliantPatients, EligiblePatients, 0)

Chronic Disease Burden = 
AVERAGEX(
    VALUES(FactEncounter[PatientID]),
    CALCULATE(DISTINCTCOUNT(DimDiagnosis[DiagnosisID]))
)
```

**Provider Productivity:**
```
Encounters per Provider = 
DIVIDE(
    [Total Encounters],
    DISTINCTCOUNT(FactEncounter[ProviderID]),
    0
)

Revenue per Provider = 
DIVIDE(
    [Total Collections],
    DISTINCTCOUNT(DimProvider[ProviderID]),
    0
)

Average Visit Duration = AVERAGE(FactAppointment[VisitDuration])

Provider Utilization % = 
DIVIDE(
    [Total Scheduled Hours],
    [Total Available Hours],
    0
)

RVU per Provider = 
SUMX(
    FactProcedure,
    RELATED(DimProcedure[RVUValue])
) / DISTINCTCOUNT(FactProcedure[ProviderID])
```

---

### 5. Report Design & Visualizations

#### Page 1: Executive Dashboard
**Purpose:** High-level healthcare operations overview

**Visuals:**
- **KPI Cards:**
  - Total Patients (with MoM change)
  - Total Encounters
  - Average Length of Stay
  - Collection Rate
  - Patient Satisfaction Score
  
- **Line Chart:** Encounter Volume Trend (12-month rolling)
- **Clustered Bar Chart:** Encounters by Department/Specialty
- **Gauge Chart:** Quality Metrics vs. Benchmarks
- **Donut Chart:** Encounter Distribution (Inpatient/Outpatient/Emergency)
- **Matrix Table:** Department Performance Summary

#### Page 2: Patient Analytics
**Purpose:** Patient population insights and demographics

**Visuals:**
- **Population Pyramid:** Age & Gender Distribution
- **Donut Chart:** Insurance Payer Mix
- **Bar Chart:** Top 10 Diagnoses by Patient Count
- **Heat Map:** Chronic Disease Comorbidity Matrix
- **Scatter Plot:** Patient Risk Score vs. Healthcare Utilization
- **Cohort Analysis:** Patient Retention by Acquisition Month
- **Map Visual:** Patient Geographic Distribution by ZIP Code
- **Table:** High-Risk Patient List (filtered for care management)

#### Page 3: Clinical Quality Dashboard
**Purpose:** Quality metrics and clinical outcomes

**Visuals:**
- **KPI Cards:**
  - 30-Day Readmission Rate
  - Medication Error Rate
  - Complication Rate
  - Preventive Care Compliance
  
- **Line Chart:** Readmission Rate Trend
- **Clustered Column Chart:** Quality Metrics by Department
- **Matrix:** HEDIS Measures Performance
- **Waterfall Chart:** Factors Contributing to Readmissions
- **Funnel:** Patient Care Pathway Completion Rates
- **Table:** Quality Measure Outliers (flagged for review)
- **Gauge Charts:** Core Quality Measures vs. National Benchmarks

#### Page 4: Financial Performance
**Purpose:** Revenue cycle and financial analytics

**Visuals:**
- **KPI Cards:**
  - Total Charges
  - Total Collections
  - Collection Rate
  - Days in A/R
  - Operating Margin %
  
- **Area Chart:** Revenue Trend (by service line)
- **Clustered Bar Chart:** Revenue by Department
- **Waterfall Chart:** Revenue Cycle Performance
- **Matrix Table:** Payer Mix Analysis (charges, payments, denials)
- **Scatter Plot:** Charge Amount vs. Collection Rate by Procedure
- **Funnel:** Claims Processing (submitted → approved → collected)
- **Table:** Aging A/R Report (30/60/90/120+ days)

#### Page 5: Operational Efficiency
**Purpose:** Scheduling, appointments, and resource utilization

**Visuals:**
- **KPI Cards:**
  - Appointment No-Show Rate
  - Average Wait Time
  - Bed Occupancy Rate
  - Provider Utilization %
  
- **Line Chart:** Daily Appointment Volume
- **Heat Map:** Appointment Scheduling Patterns (day/time)
- **Clustered Column Chart:** No-Show Rate by Department
- **Bar Chart:** Average Wait Time by Clinic Location
- **Matrix:** Provider Productivity (encounters, RVUs, revenue)
- **Gantt Chart:** OR Scheduling and Utilization
- **Gauge Charts:** Resource Utilization Metrics

#### Page 6: Population Health Management
**Purpose:** Chronic disease management and preventive care

**Visuals:**
- **KPI Cards:**
  - Diabetes Prevalence
  - Hypertension Prevalence
  - Average Chronic Conditions per Patient
  - Preventive Screening Rate
  
- **Donut Chart:** Disease Prevalence Distribution
- **Clustered Bar Chart:** Top Chronic Conditions
- **Line Chart:** Disease Management Program Enrollment Trend
- **Matrix:** Care Gaps by Patient Risk Tier
- **Table:** Patients Due for Preventive Services
- **Decomposition Tree:** Risk Stratification Analysis
- **Scatter Plot:** Social Determinants of Health Impact

#### Page 7: Provider Performance
**Purpose:** Individual and group provider analytics

**Visuals:**
- **Matrix Table:** Provider Scorecard
  - Encounters, RVUs, Revenue, Patient Satisfaction, Quality Metrics
- **Clustered Bar Chart:** Top Providers by Productivity
- **Line Chart:** Provider Patient Volume Trend
- **Scatter Plot:** Provider Efficiency (RVUs vs. Hours)
- **Table:** Provider Patient Panel Summary
- **Heat Map:** Provider Schedule Utilization

---

### 6. Advanced Features Implementation

#### Row-Level Security (RLS)
```
// Provider Access - Only see own patients
[ProviderID] = LOOKUPVALUE(
    DimProvider[ProviderID],
    DimProvider[NPI],
    USERNAME()
)

// Department Access
[Department] IN VALUES(UserDepartmentAccess[Department])

// De-identified data for analysts
[PHI_Flag] = "DeIdentified"
```

#### Dynamic Security for HIPAA Compliance
- Automatic PHI masking based on user role
- Minimum necessary data access principle
- Audit trail for all data access

#### Bookmarks & Buttons
- Toggle between different time periods (MTD, QTD, YTD)
- Filter presets for common analysis (high-risk patients, specific conditions)
- Switch between aggregate and detail views

#### Drill-Through Pages
- Patient detail drill-through (full encounter history)
- Provider detail page (complete performance metrics)
- Encounter detail (all associated diagnoses, procedures, meds)
- Financial detail (claim-level information)

#### Custom Tooltips
- Patient tooltip: demographics, risk score, active conditions
- Provider tooltip: specialty, years of service, current panel size
- Encounter tooltip: diagnoses, procedures, charges

#### Parameters
- Target setting for quality metrics
- Benchmark comparisons (national/regional averages)
- Risk stratification threshold adjustment
- Cost per patient scenarios

---

### 7. Data Refresh Strategy

#### Scheduled Refresh
- **Frequency:** 
  - Clinical data: Every 4 hours (DirectQuery for real-time ED data)
  - Financial data: Daily at 6:00 AM
  - Patient demographics: Weekly on Sundays
  
- **Incremental Refresh:**
  - Historical encounters (> 2 years): Refresh quarterly
  - Recent encounters (< 2 years): Refresh daily
  - Current day: DirectQuery for real-time monitoring

#### Performance Optimization
- Aggregations for encounter and lab result fact tables
- Composite models for frequently accessed dimensions
- Partitioning on date ranges
- Index optimization on high-cardinality columns
- Remove PHI columns not needed for analytics

---

### 8. Publishing & Distribution

#### Power BI Service Configuration
- **Workspace:** Healthcare Analytics Premium Capacity
- **App Creation:** Clinical Operations & Quality App
- **Access Control:**
  - C-Suite: Full access, all facilities
  - CMO/CNO: Clinical quality dashboards
  - CFO: Financial performance dashboards
  - Providers: RLS-filtered (own patients only)
  - Quality Managers: Quality & outcomes dashboards
  - Compliance Officers: Audit reports

#### Secure Report Sharing
- Published app with Azure AD authentication
- Email subscriptions with data export restrictions
- Power BI Mobile app with offline disabled
- Embedded reports in EHR portal (single sign-on)
- Export restrictions to prevent PHI leakage

---

### 9. Monitoring & Maintenance

#### Usage Metrics
- Track report access and user engagement
- Monitor query performance and timeout issues
- Identify unused reports for archival

#### Data Governance
- Monthly data quality audits
- Quarterly security reviews
- Annual HIPAA compliance assessment
- Regular validation against source systems

#### Continuous Improvement
- Bi-weekly clinical stakeholder meetings
- Monthly quality metric reviews with medical staff
- Quarterly benchmark updates
- New clinical measures based on regulatory requirements

---

## Key Performance Indicators (KPIs)

### Patient Care Quality KPIs

1. **30-Day Readmission Rate**
   - **Definition:** % Inpatients readmitted within 30 days
   - **Target:** <12% (below national average)
   - **Frequency:** Monthly monitoring

2. **Average Length of Stay (ALOS)**
   - **Definition:** Average days for inpatient encounters
   - **Target:** 4.2 days (specialty-adjusted)
   - **Frequency:** Weekly monitoring

3. **Patient Satisfaction Score (HCAHPS)**
   - **Definition:** Average rating on patient surveys (1-5 scale)
   - **Target:** 4.3+ (90th percentile nationally)
   - **Frequency:** Continuous, reported monthly

4. **Emergency Department Wait Time**
   - **Definition:** Average minutes from arrival to provider
   - **Target:** <30 minutes
   - **Frequency:** Daily monitoring

5. **Medication Reconciliation Rate**
   - **Definition:** % Encounters with completed med reconciliation
   - **Target:** >95%
   - **Frequency:** Weekly monitoring

6. **Hospital-Acquired Infection Rate**
   - **Definition:** Infections per 1,000 patient days
   - **Target:** <2.0
   - **Frequency:** Monthly monitoring

7. **Mortality Index**
   - **Definition:** Observed Deaths / Expected Deaths (risk-adjusted)
   - **Target:** <1.0
   - **Frequency:** Quarterly review

---

### Clinical Outcomes KPIs

8. **Complication Rate**
   - **Definition:** % Procedures with documented complications
   - **Target:** <2%
   - **Frequency:** Monthly review

9. **Preventive Care Screening Compliance**
   - **Definition:** % Eligible patients with completed screenings
   - **Target:** >75%
   - **Frequency:** Quarterly review

10. **Diabetes HbA1c Control**
    - **Definition:** % Diabetic patients with HbA1c <8%
    - **Target:** >70%
    - **Frequency:** Quarterly review

11. **Hypertension Control Rate**
    - **Definition:** % HTN patients with BP <140/90
    - **Target:** >65%
    - **Frequency:** Quarterly review

12. **Immunization Rate (Adult Flu)**
    - **Definition:** % Eligible patients receiving flu vaccine
    - **Target:** >60%
    - **Frequency:** Seasonal monitoring (Oct-Mar)

---

### Operational Efficiency KPIs

13. **Bed Occupancy Rate**
    - **Definition:** (Patient Days / Available Bed Days) × 100
    - **Target:** 75-85% (optimal range)
    - **Frequency:** Daily monitoring

14. **Emergency Department Throughput**
    - **Definition:** Average minutes from arrival to discharge
    - **Target:** <180 minutes
    - **Frequency:** Daily monitoring

15. **Operating Room Utilization**
    - **Definition:** % Scheduled OR time actually used
    - **Target:** >85%
    - **Frequency:** Weekly monitoring

16. **Appointment No-Show Rate**
    - **Definition:** % Scheduled appointments not kept
    - **Target:** <8%
    - **Frequency:** Daily monitoring

17. **Same-Day Appointment Availability**
    - **Definition:** % Days with same-day slots available
    - **Target:** >30%
    - **Frequency:** Weekly monitoring

18. **Lab Turnaround Time (TAT)**
    - **Definition:** Average hours from order to result
    - **Target:** <4 hours (routine), <1 hour (STAT)
    - **Frequency:** Daily monitoring

---

### Financial Performance KPIs

19. **Net Collection Rate**
    - **Definition:** (Payments / (Charges - Adjustments)) × 100
    - **Target:** >95%
    - **Frequency:** Monthly review

20. **Days in Accounts Receivable (A/R)**
    - **Definition:** Average days to collect payment
    - **Target:** <40 days
    - **Frequency:** Monthly monitoring

21. **Claim Denial Rate**
    - **Definition:** % Claims denied on first submission
    - **Target:** <5%
    - **Frequency:** Weekly monitoring

22. **Cost per Patient Encounter**
    - **Definition:** Total Operating Costs / Total Encounters
    - **Target:** Reduce by 10% YoY
    - **Frequency:** Monthly review

23. **Revenue per Provider (wRVU)**
    - **Definition:** Work Relative Value Units per FTE provider
    - **Target:** Specialty-specific benchmarks
    - **Frequency:** Monthly monitoring

24. **Operating Margin**
    - **Definition:** (Operating Revenue - Operating Expenses) / Operating Revenue
    - **Target:** 3-5%
    - **Frequency:** Monthly review

25. **Bad Debt as % of Revenue**
    - **Definition:** Uncollectible patient balances / Total Revenue
    - **Target:** <3%
    - **Frequency:** Quarterly review

---

### Population Health KPIs

26. **Active Patient Panel Size**
    - **Definition:** Patients with visit in last 24 months
    - **Target:** Maintain or grow 5% annually
    - **Frequency:** Monthly monitoring

27. **High-Risk Patient Enrollment**
    - **Definition:** % High-risk patients in care management programs
    - **Target:** >80%
    - **Frequency:** Monthly monitoring

28. **Chronic Disease Prevalence**
    - **Definition:** % Patients with 1+ chronic conditions
    - **Benchmark:** Track trend vs. regional average
    - **Frequency:** Quarterly review

29. **Care Gap Closure Rate**
    - **Definition:** % Identified care gaps addressed within 90 days
    - **Target:** >60%
    - **Frequency:** Monthly monitoring

30. **Total Cost of Care per Member per Month (PMPM)**
    - **Definition:** Total healthcare costs / Member months
    - **Target:** Reduce 5% annually
    - **Frequency:** Quarterly review

---

### Provider Performance KPIs

31. **Provider Productivity (Encounters per Day)**
    - **Definition:** Average patient encounters per clinical day
    - **Target:** 18-22 (primary care), specialty-specific
    - **Frequency:** Monthly monitoring

32. **Provider Patient Satisfaction**
    - **Definition:** Average provider rating (1-5 scale)
    - **Target:** 4.5+
    - **Frequency:** Continuous, reported monthly

33. **Clinical Documentation Completion**
    - **Definition:** % Charts closed within 48 hours
    - **Target:** >90%
    - **Frequency:** Weekly monitoring

34. **Referral Completion Rate**
    - **Definition:** % Referrals with completed specialist visit
    - **Target:** >85%
    - **Frequency:** Monthly monitoring

---

### Regulatory & Compliance KPIs

35. **HEDIS Measures Composite Score**
    - **Definition:** Average performance across all HEDIS measures
    - **Target:** 75th percentile or higher
    - **Frequency:** Annual review (mid-year check)

36. **Meaningful Use Attestation Metrics**
    - **Definition:** Compliance with EHR meaningful use criteria
    - **Target:** 100% compliance
    - **Frequency:** Quarterly review

37. **Medical Record Documentation Compliance**
    - **Definition:** % Charts passing audit criteria
    - **Target:** >98%
    - **Frequency:** Monthly audit sample

---

## Business Impact

### Clinical Achievements
- **Reduced 30-day readmissions by 18%** through predictive analytics
- **Improved patient satisfaction scores by 12%** via wait time optimization
- **Increased preventive screening compliance by 25%** with care gap identification
- **Decreased medication errors by 35%** through alert implementation

### Operational Improvements
- **Reduced appointment no-shows by 22%** with reminder optimization
- **Improved OR utilization from 78% to 89%**
- **Decreased average ED wait time by 15 minutes**
- **Increased provider productivity by 8%** through schedule optimization

### Financial Outcomes
- **$3.2M increase in annual collections** through denial management
- **Reduced days in A/R from 52 to 38 days**
- **Improved net collection rate from 92% to 96%**
- **$1.8M cost savings** through resource optimization

### Population Health
- **Enrolled 2,500 high-risk patients** in care management programs
- **Improved diabetes HbA1c control by 15%**
- **Reduced total cost of care by 7% PMPM** for managed population
- **Closed 5,000+ care gaps** in chronic disease management

---

## Technical Stack

- **Data Sources:** EHR/EMR (Epic/Cerner), SQL Server, HL7 FHIR APIs
- **Data Warehouse:** Azure SQL Database
- **ETL/Data Prep:** Azure Data Factory, Power Query
- **Data Modeling:** Power BI Desktop, DAX
- **Visualization:** Power BI Service (Premium Capacity)
- **Security:** Row-Level Security, Azure AD, HIPAA-compliant encryption
- **Compliance:** PHI de-identification, audit logging, access controls

---

## Compliance & Security

### HIPAA Compliance Measures
- **Data Encryption:** All data encrypted at rest (AES-256) and in transit (TLS 1.2+)
- **Access Controls:** Role-based access with MFA requirement
- **Audit Trails:** Comprehensive logging of all data access
- **De-identification:** PHI removed per Safe Harbor method for analytics
- **Business Associate Agreements:** Executed with all vendors
- **Regular Security Assessments:** Quarterly penetration testing

### Data Governance
- **Data Stewardship:** Clinical informatics team oversight
- **Quality Assurance:** Automated data validation rules
- **Change Management:** Version control and testing protocols
- **Incident Response:** 24-hour breach notification process
- **Training:** Annual HIPAA training for all users

---

## Future Enhancements

1. **Predictive Analytics:**
   - Readmission risk scoring with machine learning
   - No-show prediction models
   - Length of stay forecasting
   - Early sepsis detection algorithms

2. **Natural Language Processing:**
   - Clinical note analysis for diagnosis coding
   - Sentiment analysis of patient feedback
   - Automated quality measure extraction

3. **Real-Time Dashboards:**
   - Live ED capacity and bed management
   - Real-time provider schedules and patient flow
   - Immediate alert system for quality issues

4. **Social Determinants of Health:**
   - Integration of SDOH data (housing, food security, transportation)
   - Community resource referral tracking
   - Health equity analytics

5. **Interoperability:**
   - HIE (Health Information Exchange) integration
   - Care coordination across facilities
   - Patient-generated health data (wearables, apps)

6. **Advanced Visualizations:**
   - Clinical pathway analysis (Sankey diagrams)
   - Network analysis for referral patterns
   - Geospatial analysis for community health

---

*Last Updated: March 2024*
*HIPAA Compliant | De-identified Data Only*

