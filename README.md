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
