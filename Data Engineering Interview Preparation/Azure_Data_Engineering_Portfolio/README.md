# Azure Data Engineering Project and Resume Pack

Six detailed Azure/Microsoft reference project designs, a shared technical implementation handbook, a full master resume, an ATS application draft and six project-focused resume variants.

The named clients and project titles come from your request. Their internal architectures, your employment and your achievements were not provided. All proposed source systems, technology choices, flows and responsibilities require confirmation before they become resume claims. A proposed modernization design can be presented as a portfolio project if clearly labeled; it must not be presented as a historical implementation that did not happen.

## Project documents

| Project | Focus | Document |
|---|---|---|
| Citi Bank (EMEA) | Enterprise Banking Data Analytics Platform on Microsoft Fabric | [End-to-end design](projects/01_citi_fabric_banking_analytics.md) |
| Barclays (RFT-UKC Gen3) | Azure Data Lake Modernization | [End-to-end design](projects/02_barclays_rft_ukc_gen3_modernization.md) |
| BNP Paribas | Enterprise Datahub and Data Integration Platform | [End-to-end design](projects/03_bnp_enterprise_datahub.md) |
| Synchrony Financial | Enterprise Data Quality and Governance | [End-to-end design](projects/04_synchrony_data_quality_governance.md) |
| Barclays (RFTBSL & SRP) | Financial Data Warehouse Integration | [End-to-end design](projects/05_barclays_rftbsl_srp_warehouse.md) |
| Mobistar | Telecom Data Warehouse Transformation | [End-to-end design](projects/06_mobistar_telecom_warehouse.md) |

## Implementation and resumes

- [Shared implementation handbook](IMPLEMENTATION_HANDBOOK.md): build sequence, metadata tables, ADF orchestration, PySpark validation, Delta upsert, SCD history, streaming, reconciliation, CI/CD and recovery.
- [Full master resume](resumes/FULL_AZURE_DATA_ENGINEER_RESUME.md): all six engagements, technical skills, employer history and education placeholders.
- [ATS resume draft](resumes/ATS_AZURE_DATA_ENGINEER_RESUME.md): concise candidate content for selecting the most relevant verified projects.
- [Citi Bank (EMEA) focused resume](resumes/01_citi_fabric_banking_analytics_RESUME.md).
- [Barclays (RFT-UKC Gen3) focused resume](resumes/02_barclays_rft_ukc_gen3_modernization_RESUME.md).
- [BNP Paribas focused resume](resumes/03_bnp_enterprise_datahub_RESUME.md).
- [Synchrony Financial focused resume](resumes/04_synchrony_data_quality_governance_RESUME.md).
- [Barclays (RFTBSL & SRP) focused resume](resumes/05_barclays_rftbsl_srp_warehouse_RESUME.md).
- [Mobistar focused resume](resumes/06_mobistar_telecom_warehouse_RESUME.md).

## How to finalize

1. Add your name, contact details, employer titles/dates, client engagement dates, education and credentials.
2. Replace illustrative sources and architectures with actual components. Confirm acronyms and historical technology availability against engagement dates.
3. Select only responsibilities you personally performed. Distinguish implementation, contribution, operation and design review accurately.
4. Add metrics with baseline/result, unit, measurement period and evidence. Remove metric bullets if evidence is unavailable.
5. Use project documents for interview preparation; use the master resume as an inventory and trim the ATS version for the target role.

Microsoft Fabric is a Microsoft SaaS analytics platform integrated with the Azure ecosystem; it is not interchangeable with ADF, ADLS or Synapse. The Citi design intentionally uses Fabric, while the other designs use Azure services. The documents are implementation specifications with example code, not deployed projects. Azure deployment and integration tests have not been run.

## Official platform references

- [Fabric medallion lakehouse architecture](https://learn.microsoft.com/en-us/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Fabric end-to-end lakehouse tutorial](https://learn.microsoft.com/en-us/fabric/data-engineering/tutorial-lakehouse-introduction)
- [ADF incremental ingestion with watermarks](https://learn.microsoft.com/en-us/azure/data-factory/tutorial-incremental-copy-portal)
- [Azure Databricks MERGE reference](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/delta-merge-into)
- [Azure Databricks change data feed](https://learn.microsoft.com/en-us/azure/databricks/delta/delta-change-data-feed)
- [Microsoft Purview governance setup](https://learn.microsoft.com/en-us/purview/data-governance-get-started)

<!-- FLOW_INDEX_START -->

## Expanded full-flow documentation

[Open the full project flow diagram atlas](FULL_PROJECT_FLOW_DIAGRAMS.md).

Each of the six project Markdown files now includes seven Mermaid diagrams: complete data flow, runtime sequence, project-specific business transformation, lifecycle states, failure/replay recovery, security/governance, and development-to-production deployment. Each also includes source-to-output contracts, a detailed stage narrative, a worked record journey, dependencies, publication behavior, consumer flows, observability and acceptance evidence.

The atlas collects the six complete project data-flow diagrams. Mermaid requires a compatible Markdown viewer; plain-text flows are retained in every project document. These files specify reference implementations and have not deployed or executed Azure resources.
