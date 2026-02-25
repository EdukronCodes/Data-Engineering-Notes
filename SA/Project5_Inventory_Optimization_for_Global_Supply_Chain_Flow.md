### Project 5 — Inventory Optimization for Global Supply Chain (Flow)

### Goal
Optimize global inventory (multi-echelon) by combining demand signals, lead times, constraints, and cost/service targets to produce **replenishment recommendations**, **safety stock**, and **exception management** with traceable KPIs.

### Objectives
- Improve target service levels (fill rate/OTIF) while reducing working capital and carrying costs.
- Provide consistent inventory policy parameters (safety stock, reorder point, min-max) by SKU-location and echelon.
- Generate explainable replenishment recommendations that planners can trust and override with audit trails.
- Enable scenario planning to quantify cost vs service trade-offs under disruptions.
- Establish monitoring to track realized outcomes (stockouts, overrides, turns) and continuously recalibrate parameters.

### Primary users and outputs
- **Supply planners**: reorder points, safety stock, recommended order quantities (ROQ)
- **Operations**: exceptions (at-risk stockouts, expiring inventory), expedite suggestions
- **Finance**: inventory value, carrying cost, working capital impacts
- **Executives**: service level, fill rate, OTIF, inventory turns

### Reference architecture (high-level)
```mermaid
flowchart LR
  subgraph Sources
    ERP[ERP: orders, shipments, purchase orders]
    WMS[WMS: on-hand, movements]
    TMS[TMS: transit status]
    SUP[Supplier: lead times, capacity]
    DEM[Demand signals: sales/POS/forecast]
    COST[Costs: holding, ordering, shortage]
    CAL[Calendars/holidays]
    MDM[Item/location master data]
  end

  subgraph Ingest
    ADF[ADF / Pipelines]
  end

  subgraph Lakehouse
    ADLS[(ADLS Gen2)]
    BR[Bronze]
    SL[Silver]
    GL[Gold: planning marts]
  end

  subgraph Optimization
    DBX[Databricks/Spark]
    RULES[Business rules + constraints]
    OPT[Optimization engine\n(heuristics/MIP as needed)]
    SIM[What-if scenarios]
  end

  subgraph Serve
    DW[(SQL/DW)]
    PBI[Power BI]
    API[Replenishment API/Exports]
    WB[Write-back to ERP/APS]
    MON[Monitoring/Alerts]
  end

  Sources --> Ingest --> ADLS --> BR --> SL --> GL
  GL --> DBX --> RULES --> OPT --> SIM --> DW
  DW --> PBI
  DW --> API --> WB
  OPT --> MON
```

### End-to-end flow (detailed)
- **0) Planning scope & KPI definition**
  - Define planning levels:
    - SKU-location-day/week, and echelons (plant/DC/region/store)
  - Define KPIs and targets:
    - Service level, fill rate, OTIF, inventory turns, backorders, cost-to-serve

- **1) Ingestion to Bronze**
  - Bring in:
    - On-hand, on-order, in-transit, open sales orders, open POs
    - Lead times (planned vs actual), supplier constraints, MOQ/pack sizes
    - Demand inputs (actuals + forecasts), promotions/seasonality flags (optional)
  - Capture run id, source watermarks, and reconciliation counts

- **2) Standardize to Silver**
  - Conform item and location keys (MDM)
  - Normalize units of measure (UoM), currency, and time zones
  - Clean/validate:
    - Negative inventory, duplicate shipments, missing lead times, invalid statuses

- **3) Build Gold planning marts**
  - Core tables:
    - `inventory_position` (on_hand, on_order, in_transit, allocated)
    - `demand_plan` (forecast + overrides, by horizon)
    - `supply_plan` (POs, production orders, constraints)
    - `lead_time_profile` (distribution, variability)
    - `item_location_params` (MOQ, lot size, shelf life, review period)
  - Derived metrics:
    - Demand variability (std dev), lead time variability, historical bias

- **4) Parameter calibration**
  - Safety stock drivers:
    - Service target, demand std dev, lead time std dev
  - Reorder policy selection by segment:
    - (s, S), min-max, periodic review, EOQ variants
  - Segment SKUs:
    - ABC/XYZ, criticality, margin, shelf-life risk

- **5) Optimization & recommendations**
  - Inputs:
    - Current inventory position, projected demand, supply constraints, costs
  - Constraints:
    - MOQ, pack size, supplier capacity, warehouse capacity, budget
  - Outputs:
    - Recommended orders by supplier/DC, reorder points, safety stock, exception flags

- **6) Scenario simulation (what-if)**
  - Examples:
    - Lead time increase, supplier outage, port delays, promo uplift, demand spike
  - Compare scenarios:
    - Service level vs cost trade-offs, working capital impact

- **7) Publish & write-back**
  - Store outputs with run id, scenario id, and audit fields
  - Serve via:
    - DW tables for reporting
    - API/exports for planners and ERP ingestion
  - Write-back:
    - ERP replenishment proposals, planned orders, parameter updates (controlled)

- **8) Monitoring & continuous improvement**
  - Data monitoring:
    - Late sources, volume anomalies, missing lead time updates
  - Recommendation monitoring:
    - Override rate, planner acceptance, realized stockout reduction
  - KPI monitoring:
    - Service level trend, inventory turns, aging/expiry waste

### Orchestration pattern
- ADF triggers:
  - Ingest → Conform → Build marts → Optimize → Publish → Notify
- Make optimization runs reproducible using run id + snapshotting inputs.

### Notes (design choices + practical tips)
- **Garbage in, garbage out**: lead times, on-hand accuracy, and open order status quality typically drive most failure modes—monitor them as first-class KPIs.
- **Multi-echelon complexity**: start with single-echelon (DC → store) then extend to plants/suppliers once validation is stable.
- **Service targets by segment**: use differentiated targets (A items higher service, C items lower) to control cost.
- **Variability matters**: safety stock should reflect both demand and lead time variability; don’t rely only on averages.
- **Constraints are business rules**: MOQ/pack sizes/capacity often dominate “optimal”; keep constraint violations visible as exceptions.
- **Planner trust**: store recommendation explanations (top drivers, constraints hit) and track acceptance/override rates.
- **Scenario discipline**: snapshot inputs and label scenarios so comparisons are reproducible and auditable.
- **Backtesting**: simulate policies on historical data to compare turns/stockouts before deploying globally.

### Deliverables
- Architecture + end-to-end flow diagram
- Gold planning marts (inventory position, demand plan, supply plan, lead time profile)
- Optimization logic (constraints + objective) and scenario framework
- Serving layer (DW + Power BI dashboards) + write-back interface
- Monitoring: data freshness + exception alerts + KPI tracking
