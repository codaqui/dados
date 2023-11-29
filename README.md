# Dados Codaqui

## Estrutura do Projeto

```text
.
|____terraform # Pasta para Arquivos de Infraestrutura
|____.editorconfig # Arquivo para Configurar Editores
|____README.md # Arquivo de Documentação
|____.github # Pasta para Arquivos de Configuração do GitHub
|____data
| |____manual.yaml # Arquivo de Dados Manuais
| |____automática # Arquivo que será commitado automaticamente
| | |____discord.yaml # Arquivo de Dados do Discord
| | |____whatsapp.yaml # Arquivo de Dados do WhatsApp
| | |____google.yaml # Arquivo de Dados do Google
```

## Indicadores

```mermaid
flowchart TD
    IND[Indicadores da Codaqui] --> FER(Ferramentas)
    FER --> FER1(Google Analytics)
    FER --> FER2(Google Ads)
    FER --> FER3(Discord)
    FER --> FER4(WhatsApp)
    IND --> EXP(Experiencia do Usuário)
    EXP --> EXP1(Alunos Trilha)
    EXP --> EXP2(Alunos Mentorado)
    EXP1 --> CERT(Certificado)
    EXP2 --> APO(Apoio a Comunidade)
    EXP1 --> APO
    EXP2 --> CERT
    APO --> BLOG(Blog)
    APO --> PROJ(Projeto)
```

## Linha do Tempo

```mermaid
flowchart TD
    P1[Parte1: Infraestrutura] -->|GithubActions| P11(Terraform)
    P11 --> |On/Off| P12(Serviços do Azure)

    P2(Parte2: Manual)
    P2 --> |GitHub| P21(YAML)
    P21 --> |Pasta/Data| P22(Dados Manuais)

    P3(Parte3: Automática)
    P3 --> |Coleta de Dados| P31(Ferramentas)
    P31 --> P32(Google)
    P31 --> P33(Discord)
    P31 --> P34(WhatsApp)
    P32 --> P35(Bucket/Yaml GitHub)
    P33 --> P35
    P34 --> P35

    P4(Parte4: Ciencia de Dados)

    P4 --> P41(Estudos Específicos)
```


## Desenvolvimento/Colaboração

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## TODO

- [ ] Estudar Terraform (Básico)
  - [ ] Criar um Arquivo de Infraestrutura (main.tf)
    - Criar apenas um único arquivo, para no futuro dividir conforme a necessidade do projeto.
  - [ ] Criar um Arquivo de Variáveis (variables.tf)
  - [ ] Verificar os serviços que serão utilizados no Azure
- [ ] Configurar GitHub Actions Básica
  - [ ] Criar uma Action de Hello World para testar
    - [ ] Criar uma Action de Terraform para testar
    - [ ] Criar uma Action que faça o `plan` da infraestrutura
        - [ ] Usar um serviço de Storage da Azure para salvar os estados.
    - [ ] Criar uma Action que faça o deploy da infraestrutura
    - [ ] Criar uma Action que destrua a infraestrutura
- [ ] Coleta de Dados
    - [ ] Github Actions
    - [ ] Azure Functions
- [ ] Visualização de Dados
    - Decidir ferramenta para fazer a visualização dos dados.
- [ ] Ciência de Dados
    - Decidir ferramentas e serviços para fazer a ciência de dados.