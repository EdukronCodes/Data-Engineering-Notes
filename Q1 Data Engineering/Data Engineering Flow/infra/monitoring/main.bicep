@description('Log Analytics workspace for retail data pipeline monitoring')
param location string = resourceGroup().location

@description('Suffix for resource names')
param suffix string = '3546'

@description('Data Factory name')
param dataFactoryName string

@description('Lake storage account name')
param storageLakeAccount string

@description('Sources storage account name')
param storageSourcesAccount string

@description('SQL server name')
param sqlServerName string

@description('SQL database name')
param sqlDatabaseName string

@description('PostgreSQL server name')
param postgresServerName string

@description('Cosmos DB account name')
param cosmosAccountName string

@description('Databricks workspace name')
param databricksWorkspaceName string

@description('Key Vault name')
param keyVaultName string

var workspaceName = 'log-retailde-${suffix}'
var actionGroupName = 'ag-retailde-ops-${suffix}'

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: workspaceName
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource actionGroup 'Microsoft.Insights/actionGroups@2023-01-01' = {
  name: actionGroupName
  location: 'Global'
  properties: {
    groupShortName: 'RetailDE'
    enabled: true
  }
}

resource adfDiag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-adf-retail'
  scope: resourceId('Microsoft.DataFactory/factories', dataFactoryName)
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'PipelineRuns', enabled: true }
      { category: 'ActivityRuns', enabled: true }
      { category: 'TriggerRuns', enabled: true }
    ]
    metrics: [{ category: 'AllMetrics', enabled: true }]
  }
}

resource lakeStorageDiag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-lake-storage'
  scope: resourceId('Microsoft.Storage/storageAccounts', storageLakeAccount)
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'StorageRead', enabled: true }
      { category: 'StorageWrite', enabled: true }
    ]
    metrics: [
      { category: 'Transaction', enabled: true }
      { category: 'Ingress', enabled: true }
      { category: 'Egress', enabled: true }
    ]
  }
}

resource sourcesStorageDiag 'Microsoft.Insights/diagnosticSettings@2021-05-01-preview' = {
  name: 'diag-sources-storage'
  scope: resourceId('Microsoft.Storage/storageAccounts', storageSourcesAccount)
  properties: {
    workspaceId: logAnalytics.id
    logs: [
      { category: 'StorageRead', enabled: true }
      { category: 'StorageWrite', enabled: true }
    ]
    metrics: [{ category: 'Transaction', enabled: true }]
  }
}

output logAnalyticsWorkspaceName string = logAnalytics.name
output logAnalyticsWorkspaceId string = logAnalytics.id
output logAnalyticsCustomerId string = logAnalytics.properties.customerId
