# 25-Day PySpark Learning Plan

Open [25_Day_PySpark_Learning_Plan.ipynb](./25_Day_PySpark_Learning_Plan.ipynb) in JupyterLab or Jupyter Notebook and run it from the top.

The master notebook contains:

- 25 progressive lessons from Spark fundamentals to Delta Lake and medallion ETL
- reusable retail and banking sample DataFrames
- 10 retail practice problems per day
- 10 independent banking assignment questions per day
- one banking challenge per day
- 15 interview questions with short spoken answers per day
- continuous Retail Sales Analytics and Banking Transaction Analytics projects
- expected outputs, common errors, summaries, and capstone acceptance checklists

## Start locally

```powershell
python -m pip install pyspark jupyterlab
jupyter lab .\25_Day_PySpark_Learning_Plan.ipynb
```

Day 23 additionally needs a `delta-spark` release compatible with the installed PySpark version. On native Windows, Spark file-write examples may require an organization-approved Hadoop Windows configuration; WSL/Linux or a managed Spark platform such as Azure Databricks avoids that local filesystem dependency.

`build_pyspark_course.py` is the reproducible source used to generate the notebook.
