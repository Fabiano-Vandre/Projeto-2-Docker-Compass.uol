# Projeto-2-Docker-Compass.uol
## Descrição da Atividade
1. Instalação e configuração do DOCKER ou
CONTAINERD no host EC2;
SEGUIR DESENHO
TOPOLOGIA DISPOSTA.
Ponto adicional para o trabalho utilizar
a instalação via script de Start Instance
(user_data.sh)
2. Efetuar Deploy de uma aplicação
Wordpress com:
container de aplicação
RDS database Mysql
3. Configuração da utilização do serviço
EFS AWS para estáticos do container de
aplicação Wordpress
4. Configuração do serviço de Load
Balancer AWS para a aplicação
Wordpress

## Pré requisitos
- Docker
- Conta AWS

## 1. Criação da VPC
Para esse projeto criaremos uma VPC com as seguintes configurações:

![Captura de tela 2025-02-28 151626](https://github.com/user-attachments/assets/a6fe7642-1c9f-4481-933d-81492870aec6)
![Captura de tela 2025-03-10 100658](https://github.com/user-attachments/assets/7b7ad088-3870-4d16-8ab3-4d2017b68457)

O nome da VPC fica a critério do usuário da conta escolher

## 2. Criação dos Security Group
Agora faremos a criação dos security group dos serviços com as configurações abaixo

### Load Balancer SG Inbound Rules

| Type  | Port | Source |  
| ----- | ---- | -------- |
| HTTP  | 80  | 0.0.0.0/0 |
| HTPS  | 443  | 0.0.0.0/0 |


Obs: As regras de saída ou Outbound Rules deixaremos na forma padrão


### EC2 SG Inbound Rules

| Type  | Port | Source |  
| ----- | ---- | -------- |
| HTTP  | 80  | Load Balancer SG |
| HTPS  | 443  | Load Balancer SG |

### EFS SG Inbound Rules

| Type  | Port | Source |  
| ----- | ---- | -------- |
| NFS  | 2049  | EC2 SG |

### RDS SG Inbound Rules

| Type  | Port | Source |  
| ----- | ---- | -------- |
| MySQL/Aurora  | 3306  | EC2 SG |

## 3. Criação do EFS
Para criar o EFS pesquise pelo serviço EFS e após entrar nele clique em create file system
- Após isso clique em customize
- Aparecerá a seguinte tela

![efs1](https://github.com/user-attachments/assets/cf016ad5-1c77-47a7-84e8-e4029ce6ab0a)


- Escreva o nome do seu file system e clique em next

![efs2](https://github.com/user-attachments/assets/900b6e36-28ca-41d1-82ca-1fd5bffe6dc4)


- Selecione a VPC criada para o projeto e nos mount target escolha as 2 subredes privadas
- Ainda nos mount target selecione em todos eles o security group criado para o EFS
- Clique em next até aparecer a tela de review das configurações
- Revise se todas as configurações estão corretas e clique em create

## 4. Criação do RDS
Pesquise pelo serviço RDS, após entrar nele clique em create database
- Após isso escolha a opção MySQL e em templates selecione "Free Tier"

![rds1](https://github.com/user-attachments/assets/ce248109-8617-4c1a-8d1a-5308ab90a2df)


- Escreva o identificador do seu banco de dados no campo "DB-cluster-identifier"
- Digite uma senha no campo "Master Password"
- Selecione o tipo de instância como ""

![rds2](https://github.com/user-attachments/assets/7c8de3e2-0e16-492d-be43-7e21d88ed99a)

- Na área Connectivity selecione a VPC criada para o projeto e no campo VPC Security groups selecione o Security group criado para o RDS

![RDS3](https://github.com/user-attachments/assets/accb34e2-fe76-4f52-a648-5e7560c1cd5d)


- Clique na área Additional Configuration e digite nela o nome do seu banco de dados (Que será usado para conectá-lo ao Wordpress)

## 5. Criação do Launch Template
