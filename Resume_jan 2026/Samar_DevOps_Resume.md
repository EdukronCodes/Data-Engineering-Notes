# Resume – Samar (DevOps Engineer → MLOps / GenAI Platforms)

## Details
- **Name**: Samar  
- **Target Role**: DevOps / MLOps Engineer for Data Science & GenAI  
- **Experience**: Not specified (1–2+ years assumed)  
- **Primary Stack**: CI/CD, Cloud Infrastructure, Automation  

## Career Objective
DevOps Engineer focusing on CI/CD and cloud infrastructure, seeking to specialize in MLOps and GenAI platform engineering. Motivated to build reliable, automated pipelines and environments that empower data scientists to deploy ML and agentic AI workloads at scale.

## Roles & Responsibilities
1. Implemented CI/CD pipelines to build, test, and deploy data and ML-related services.
2. Managed cloud resources (compute, storage, networking) for data engineering and data science teams.
3. Automated infrastructure provisioning and configuration using scripts and templates.
4. Containerized applications and simple ML services using Docker and managed their lifecycle.
5. Set up monitoring and logging solutions for critical services and tuned alerts for reliability.
6. Collaborated with data teams to define deployment strategies for models, LLM services, and APIs.
7. Introduced infrastructure support for GenAI workloads, including GPU-enabled instances and secure access to LLM providers.
8. Helped design agentic AI workflows that tie infrastructure events (failures, scale needs) to automated actions.
9. Documented platform components, deployment runbooks, and troubleshooting steps.
10. Participated in security reviews, applying best practices for secrets management and access control.

## Skills
- **DevOps & MLOps**: CI/CD, Docker, basic Kubernetes, infrastructure scripting, deployment patterns for ML/GenAI
- **Cloud**: AWS/Azure/GCP basics, networking, load balancers, storage
- **Tooling**: Git, Terraform/CloudFormation (optional), monitoring (Prometheus/Grafana, CloudWatch)
- **GenAI & Agentic AI**: Deploying LLM services, configuring autoscaling, integrating with vector stores/feature stores, event-driven agents
- **Other**: Linux administration, scripting, documentation, collaboration

## Projects
#  Azure DevOps Projects

---

## Project 1: End-to-End CI/CD Pipeline for Microservices on Azure Kubernetes Service (AKS)

### Problem Statement
Automate build, test, and deployment of multiple microservices with **zero downtime** and **rollback support**.

### Tools & Services
- Azure DevOps (Repos, Pipelines, Artifacts)
- Azure Kubernetes Service (AKS)
- Docker
- Helm
- Azure Container Registry (ACR)
- SonarQube
- Azure Key Vault

### Implementation
- Created **multi-stage Azure DevOps YAML pipelines** for build, test, security scanning, and deployment.
- Dockerized microservices and pushed container images to **Azure Container Registry (ACR)**.
- Integrated **SonarQube** for static code analysis and vulnerability scanning.
- Used **Helm charts** to manage Kubernetes deployments.
- Implemented **Blue-Green and Canary deployment strategies** in AKS.
- Managed application secrets and configuration using **Azure Key Vault**.
- Enabled **automatic rollback** on deployment failure to ensure high availability.

### Outcome
- Reduced deployment time by **70%**
- Achieved **zero-downtime deployments**
- Improved code quality and release confidence

**Key Skills Shown:**  
CI/CD · AKS · Docker · Helm · YAML Pipelines · DevSecOps

---

## Project 2: Infrastructure as Code (IaC) Automation Using Terraform & Azure DevOps

### Problem Statement
Manual Azure resource provisioning was **error-prone**, **time-consuming**, and inconsistent across environments.

### Tools & Services
- Azure DevOps Pipelines
- Terraform
- Azure Resource Manager (ARM)
- Azure Storage (Remote Backend)
- Azure Key Vault

### Implementation
- Designed reusable **Terraform modules** for VNet, VM, AKS, SQL Database, and Storage Accounts.
- Created **environment-specific Azure DevOps pipelines** for Dev, QA, and Prod.
- Configured **Terraform remote state** using Azure Storage backend.
- Integrated **Azure Key Vault** for secure secret management.
- Implemented **manual approval gates** for production deployments.
- Enabled **infrastructure drift detection** using `terraform plan`.

### Outcome
- Standardized infrastructure provisioning across environments
- Reduced infrastructure setup time from **days to minutes**
- Improved compliance, governance, and auditability

**📌 Key Skills Shown:**  
Terraform · IaC · Azure DevOps · Environment Isolation · Governance
