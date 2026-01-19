# Resume – Gagan Raj (DevOps Engineer → MLOps / Data Science Platform)

## Details
- **Name**: Gagan Raj  
- **Target Role**: MLOps / Data Platform Engineer for Data Science & GenAI  
- **Experience**: 1+ year  
- **Primary Stack**: CI/CD, Git, Jenkins, Docker, Linux  

## Career Objective
DevOps Engineer with 1+ year of experience in CI/CD, containerization, and infrastructure automation, seeking to specialize in MLOps and Data Science platforms. Motivated to build reliable, scalable pipelines for ML and GenAI workloads, enabling data scientists to ship experiments to production quickly and safely using modern agentic AI tooling.

## Roles & Responsibilities (Data/ML Platform Focus)
1. Designed and maintained CI/CD pipelines (Jenkins/Git-based) to build, test, and deploy Python and data services to staging and production.
2. Containerized applications and ML services using Docker, optimizing image sizes and startup times.
3. Managed Linux-based servers/environments, configuring security, monitoring, and resource allocation for data workloads.
4. Automated environment setup for data science teams (Python environments, libraries, GPU dependencies) via scripts and configuration management.
5. Integrated ML model build steps (unit tests, training jobs, packaging) into CI/CD pipelines to enable repeatable deployments.
6. Introduced observability for ML/GenAI services, including logging, metrics, and alerting for latency, errors, and model-specific KPIs.
7. Supported LLM and agent workloads by provisioning containers/runtimes with appropriate memory, GPUs, and network policies.
8. Documented deployment patterns, runbooks, and best practices for data and AI services.
9. Collaborated with data scientists, data engineers, and product teams to translate model requirements into infrastructure designs.
10. Advocated for security and compliance best practices (secrets management, least-privilege access, artifact signing).

## Skills
- **DevOps & MLOps**: CI/CD (Jenkins, GitHub Actions), Docker, artifact registries, environment management
- **Cloud & Infra**: Linux administration, basic Kubernetes, Nginx, systemd, shell scripting
- **Data/ML Tooling**: Python environments, MLflow (basic), model packaging (Docker, wheels), API deployment (FastAPI/Flask)
- **GenAI & Agentic AI**: Deploying LLM-based services in containers, scaling API-based GenAI workloads, orchestrating background agents with queues/schedulers
- **Other**: Git, monitoring/logging (Prometheus/Grafana/ELK basics), collaboration & documentation

## Projects

### Project 1: CI/CD for ML Model Deployment
- **Title**: CI/CD for ML Model Deployment
- **Description**: Implemented CI/CD pipelines that automate building, testing, and deploying ML models as REST APIs.
- **Skills**: Jenkins, Git, Docker, Python, FastAPI, MLflow (model packaging)
- **Roles & Responsibilities**:
  1. Created Jenkins pipelines to run unit tests, linting, and container builds whenever model code was updated.
  2. Pushed built images to a secure registry and deployed to staging/production environments with version tagging.
  3. Integrated model configuration (hyperparameters, model paths) via environment variables and config files for reproducibility.
  4. Implemented health checks and rollback mechanisms in case of deployment failures.

### Project 2: GenAI Service Infrastructure
- **Title**: GenAI Service Infrastructure
- **Description**: Set up infrastructure for a Generative AI service that exposes LLM capabilities (summarization, Q&A) to internal tools.
- **Skills**: Docker, Linux, LLM APIs, API gateway, monitoring
- **Roles & Responsibilities**:
  1. Containerized the GenAI service and configured autoscaling policies based on CPU/memory and request volume.
  2. Implemented secure connection to external LLM providers, including API key management and network rules.
  3. Added structured logging and metrics (requests/sec, latency, cost per request) and exposed them to dashboards.
  4. Worked with data scientists to test performance and reliability under different workloads.

### Project 3: Agentic Automation for Environment Maintenance
- **Title**: Agentic Automation for Environment Maintenance
- **Description**: Built simple agent-like automation that monitors environment drift and automatically fixes common issues (missing packages, storage pressure).
- **Skills**: Bash, Python, cron/schedulers, monitoring APIs, agent patterns
- **Roles & Responsibilities**:
  1. Wrote scripts that periodically check system metrics and installed packages, comparing them against desired states.
  2. Implemented automated remediation actions (cleanup, package installation, service restarts) with alerts for manual review.
  3. Documented the automation workflows and integrated them into operational runbooks for the data/ML platform.
