## Desafio Técnico CodeHB

#### Solução

A solução proposta foi desenvolvida em python rodando no azure functions. Os arquivos json baixados da API estão sendo armazendos em um blob storage e a execução ocorre a cada 24 horas sendo disparada pelo data factory.

O código foi desenvolvido tendo como premissa a legibilidade, visando permitir a uma pessoa com conhecimento básico em python entender seu objetivo.

Optei por utilizar uma função recursiva para realizar a paginação dos dados, isso torna a solução mais enxuta e evita o uso de estruturas de repetição que na minha opinião são um anti-pattern quando manipulamos grande volumes de dados (computação distribuida).

Para gerar o json final, utilizei uma técnica chamada flattening, que visa nivelar um objeto JSON complexo (diversos níveis) e gerar um objeto com apenas um nível de profundidade.

Será gerado um único arquivo para cada dia, a execução ocorrerá às 00:00 AM.

#### Artefatos Utilizados

- Resource Group: 
    - codehb
- Storage Account
    - nome: codehb
    - container: results/YYYY/MM/DD
- Function App
    - nome: codehb-function
    - function: daily_trigger
    - application insights: codehb-function
- Data Factory: 
    - nome: datafactory-codehb
    - pipeline: pipeline_download_escolas
    - linked service: LF_AF_ESCOLAS
- App Service Plan:
    - nome: BrazilSouthLinuxDynamicPlan
    
    
Preparado por:

Daniel Queiroz
