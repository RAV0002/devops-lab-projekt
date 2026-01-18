param location string = 'polandcentral'
param acrName string = 'acrprojekt${uniqueString(resourceGroup().id)}'

resource acr 'Microsoft.ContainerRegistry/registries@2025-11-01' = {
    name: acrName
    location: location
    sku: {
        name:'Basic'
    }
    properties:{
        adminUserEnabled: true
    }
}
output acrLoginServer string = acr.properties.loginServer
