@description('Azure region for all resources')
param location string = resourceGroup().location

@description('Environment suffix: dev, staging, prod')
@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

@description('Base name prefix for resources (lowercase, no spaces)')
param namePrefix string = 'retailde'

@description('ADLS container for medallion lake')
param lakeContainerName string = 'retaildatalake'

@description('ADLS container for source feeds')
param sourceContainerName string = 'sources'

var uniqueSuffix = uniqueString(resourceGroup().id)
var lakeStorageName = toLower('st${namePrefix}lake${environment}${substring(uniqueSuffix, 0, 4)}')
var sourceStorageName = toLower('st${namePrefix}src${environment}${substring(uniqueSuffix, 0, 4)}')
var keyVaultName = toLower('kv-${namePrefix}-${environment}')
var dataFactoryName = 'adf-${namePrefix}-${environment}'
var databricksName = 'dbw-${namePrefix}-${environment}'

resource lakeStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: lakeStorageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    isHnsEnabled: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource sourceStorage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: sourceStorageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    isHnsEnabled: true
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

resource lakeContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${lakeStorage.name}/default/${lakeContainerName}'
  properties: { publicAccess: 'None' }
}

resource sourceContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-05-01' = {
  name: '${sourceStorage.name}/default/${sourceContainerName}'
  properties: { publicAccess: 'None' }
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A', name: 'standard' }
    enableRbacAuthorization: true
    enabledForTemplateDeployment: true
  }
}

resource dataFactory 'Microsoft.DataFactory/factories@2018-06-01' = {
  name: dataFactoryName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    globalParameters: {
      environment: { type: 'String', value: environment }
      storageAccountName: { type: 'String', value: lakeStorage.name }
      storageContainerName: { type: 'String', value: lakeContainerName }
      sourceStorageAccountName: { type: 'String', value: sourceStorage.name }
      sourceContainerName: { type: 'String', value: sourceContainerName }
      landingPathPrefix: { type: 'String', value: 'landing' }
      databricksWorkspaceUrl: { type: 'String', value: 'CONFIGURE_AFTER_DATABRICKS_DEPLOY' }
      databricksClusterId: { type: 'String', value: 'CONFIGURE_AFTER_CLUSTER_CREATE' }
      keyVaultName: { type: 'String', value: keyVault.name }
    }
  }
}

resource databricks 'Microsoft.Databricks/workspaces@2024-05-01' = {
  name: databricksName
  location: location
  sku: { name: 'standard' }
  properties: {
    managedResourceGroupId: subscriptionResourceId('Microsoft.Resources/resourceGroups', '${databricksName}-managed-rg')
    parameters: {
      enableNoPublicIp: { value: true }
    }
  }
}

output lakeStorageAccountName string = lakeStorage.name
output lakeStorageAccountUrl string = 'https://${lakeStorage.name}.dfs.core.windows.net'
output sourceStorageAccountName string = sourceStorage.name
output sourceStorageAccountUrl string = 'https://${sourceStorage.name}.dfs.core.windows.net'
output keyVaultName string = keyVault.name
output dataFactoryName string = dataFactory.name
output databricksWorkspaceName string = databricks.name
output databricksWorkspaceUrl string = databricks.properties.workspaceUrl
