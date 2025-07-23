# CI/CD for Cloud Composer with BigQuery Slot Reservation and Governance

## 🧠 Project Objective

To design and deploy a CI/CD pipeline that automates the deployment of Apache Airflow DAGs in Cloud Composer while using BigQuery Slot Reservations for cost-optimized and performance-guaranteed job execution. This project ensures strong data governance and resource management using GCP-native tools.

---

## 🏗️ Architecture


                 ┌──────────────────────────────┐
                 │       GitHub Repository      │
                 │ (Composer DAGs + CloudBuild) │
                 └─────────────┬────────────────┘
                               │
                     ┌─────────▼───────────┐
                     │  Cloud Build Triggers │
                     │  (dev and prod tags)  │
                     └─────────┬───────────┬┘
                               │           │
                ┌──────────────▼─┐     ┌────▼────────────┐
                │ Composer (Dev) │     │ Composer (Prod) │
                │  gcp-dev-env   │     │  gcp-prod-env   │
                └──────┬─────────┘     └────────┬────────┘
                       │                          │
           ┌───────────▼────────┐     ┌───────────▼────────┐
           │  Airflow DAG (Dev) │     │  Airflow DAG (Prod)│
           │  gcs_to_bq_dev     │     │  gcs_to_bq_prod     │
           └───────────┬────────┘     └───────────┬────────┘
                       │                          │
            ┌──────────▼──────────┐     ┌─────────▼──────────┐
            │ GCS Dev Bucket      │     │ GCS Prod Bucket     │
            │ sample_health_dev.csv│     │ sample_health.csv   │
            └──────────┬──────────┘     └──────────┬──────────┘
                       │                          │
            ┌──────────▼────────────┐   ┌─────────▼────────────┐
            │ BigQuery Dev Table    │   │ BigQuery Prod Table   │
            │ health.health_table_dev│   │ health.health_table   │
            └──────────┬────────────┘   └──────────┬────────────┘
                       │                          │
     ┌─────────────────▼────────────┐ ┌────────────▼────────────────┐
     │ BigQuery Dev Reservation     │ │ BigQuery Prod Reservation    │
     │ dev-slot-assignment          │ │ prod-slot-assignment         │
     └──────────────────────────────┘ └──────────────────────────────┘




---

## 🔧 Tools & Services Used

- **Cloud Composer** (Apache Airflow)
- **Cloud Build** (CI/CD automation)
- **GitHub** (source repo integration)
- **BigQuery** (data sink)
- **BigQuery Reservations** (slot allocation & assignment)
- **IAM Policies** (governance)

---

## 🚀 Features Implemented

- ✅ CI/CD pipeline using GitHub + Cloud Build for DAG deployment
- ✅ Reservation-based BigQuery job execution
- ✅ DAG orchestration in Composer with explicit reservation use
- ✅ Job governance via service account-based assignment
- ✅ Error handling and retries in DAG execution

---

## 🎯 Key Use Case

> A healthcare organization wants to load sensitive data into BigQuery using guaranteed compute resources (slots) to avoid performance delays and cost unpredictability. The data pipeline must be version-controlled and deploy automatically upon code changes.

---

## ⚠️ Challenges Faced

| Challenge | Solution |
|----------|----------|
| Cloud Build trigger failed due to missing tag/commit | Switched to **manual commit hash** trigger and ensured correct `cloudbuild.yaml` |
| DAG deployment failed due to incorrect file paths | Corrected the DAG path inside `cloudbuild.yaml` (`gsutil cp dags/*.py`) |
| BigQuery job ran with on-demand slots initially | Resolved by assigning **specific reservations** and using `parent="projects/PROJECT_ID/locations/LOCATION/reservations/RESERVATION_ID"` in DAG |
| Slot assignment wasn't honored | Ensured **IAM roles** for job-running service account + validated reservation assignment to job type |

---

## 🏁 Outcome & Success

- 👨‍💻 Fully automated deployment of Airflow DAGs from GitHub to Composer
- 💰 Reduced query execution cost and improved predictability via BQ Reservations
- ✅ Fine-grained job governance using IAM + Reservation Assignments
- 🛡️ Clean, repeatable CI/CD setup for data engineering teams

---

