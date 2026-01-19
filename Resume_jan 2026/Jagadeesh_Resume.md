# Resume – Jagadeesh (DevOps Engineer → MLOps / Data Science Platform)

## Details
- **Name**: Jagadeesh  
- **Target Role**: Senior MLOps / Cloud Data Platform Engineer  
- **Experience**: 2+ years  
- **Primary Stack**: AWS/Azure, CI/CD, Kubernetes, Terraform  

## Career Objective
Cloud and DevOps Engineer with 2+ years of experience building CI/CD pipelines and managing Kubernetes-based environments, aiming to focus on MLOps and scalable Data Science/GenAI platforms. Looking to design secure, automated infrastructures that support the full ML lifecycle, including training, deployment, monitoring, and agentic AI workflows.

## Roles & Responsibilities (MLOps-Oriented)
1. Architected CI/CD pipelines for data and ML services using Git-based workflows, Terraform, and cloud-native tools.
2. Deployed and managed Kubernetes clusters hosting ML APIs, batch jobs, and GenAI services with autoscaling and rolling updates.
3. Implemented infrastructure as code (IaC) with Terraform to provision compute, storage, networking, and managed databases for data science workloads.
4. Collaborated with data scientists to containerize training and inference pipelines, optimizing resource usage (CPU/GPU, memory).
5. Set up experiment tracking, model artifact storage, and model registry integrations.
6. Built observability for ML and GenAI workloads (metrics, logs, tracing) and configured alerts on key SLOs.
7. Implemented security controls such as IAM roles, secrets management, and network policies for data and models.
8. Supported agentic AI flows by orchestrating background workers, queues, and event-driven functions that tie AI decisions to infrastructure actions.
9. Performed capacity planning and cost optimization for cloud resources used by data science teams.
10. Documented platform architecture, deployment standards, and troubleshooting guides.

## Skills
- **Cloud**: AWS (EKS, S3, IAM, Lambda), Azure (AKS, Storage, Key Vault)
- **DevOps/MLOps**: Kubernetes, Terraform, CI/CD (GitHub Actions, Jenkins), Docker, Helm
- **Data & ML**: Python (basic), model deployment patterns, MLflow/Vertex/SageMaker (concepts), feature store basics
- **GenAI & Agentic AI**: Deploying LLM/GenAI microservices, integrating with vector databases, orchestrating multi-step agent pipelines with queues/functions
- **Other**: Monitoring (Prometheus/Grafana), logging (ELK), security best practices, Agile collaboration

## Projects

### Project 1: Cloud-Native MLOps Platform
- **Title**: Cloud-Native MLOps Platform
- **Description**: Designed and implemented a Kubernetes-based MLOps platform on AWS to support training and deployment of multiple ML models.
- **Skills**: AWS EKS, Terraform, Docker, CI/CD, MLflow (or similar)
- **Roles & Responsibilities**:
  1. Provisioned and configured EKS clusters, node groups, and storage using Terraform.
  2. Implemented CI/CD pipelines that build training containers, execute training jobs, and register models in a central registry.
  3. Deployed inference services as containerized microservices with autoscaling and blue-green deployments.
  4. Set up monitoring dashboards with model latency, error rates, and resource usage.

### Project 2: GenAI Microservices for Document Intelligence
- **Title**: GenAI Microservices for Document Intelligence
- **Description**: Built infrastructure for GenAI microservices that perform document summarization, entity extraction, and semantic search.
- **Skills**: Kubernetes, Docker, LLM APIs, vector DBs (e.g., Pinecone/Faiss), Nginx ingress
- **Roles & Responsibilities**:
  1. Containerized GenAI applications and deployed them behind an API gateway with TLS termination.
  2. Configured vector database instances and storage for embeddings; managed backup and scaling policies.
  3. Implemented horizontal pod autoscaling based on request count and latency.
  4. Collaborated with data scientists to roll out updated prompts/models with minimal downtime.

### Project 3: Agentic AI Job Orchestration
- **Title**: Agentic AI Job Orchestration
- **Description**: Set up an agent-style orchestration layer to run multi-step ML and data processing workflows triggered by events.
- **Skills**: AWS Lambda/EventBridge/SQS, Kubernetes Jobs, Terraform, Python (scripting)
- **Roles & Responsibilities**:
  1. Defined event-driven workflows where agents decide which processing or model steps to execute based on input metadata.
  2. Connected queues, serverless functions, and Kubernetes jobs to form robust, recoverable pipelines.
  3. Implemented idempotency and retry strategies for long-running tasks.
  4. Documented the orchestration patterns for wider platform adoption.
