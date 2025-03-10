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
- Selecione o tipo de instância como "db.t3.micro"

![rds2](https://github.com/user-attachments/assets/7c8de3e2-0e16-492d-be43-7e21d88ed99a)

- Na área Connectivity selecione a VPC criada para o projeto e no campo VPC Security groups selecione o Security group criado para o RDS

![RDS3](https://github.com/user-attachments/assets/accb34e2-fe76-4f52-a648-5e7560c1cd5d)


- Clique na área Additional Configuration e digite nela o nome do seu banco de dados (Que será usado para conectá-lo ao Wordpress)

## 5. Criação do Key pair
Efetuaremos agora a criação de um par de chaves para maior segurança das instâncias
- Pesquiser pelo serviço "Key pair" e clique em create key pair

![oficial](https://github.com/user-attachments/assets/459ce304-dba7-49e6-ac53-1b23c7bd5f04)


- Digite o nome do seu par de chaves
- Em key type escolha RSA
- Em key file format escolha a opção ".pem" e clique em create key pair

## 6. Criação do Launch Template
Agora criaremos um modelo de instância EC2, na aba de pesquisa digite Launch template, clique nele e em create launch template
- Digite o nome do seu launch template e a descrição dele
- Escolha o modelo "Amazon Linux Machine 2023 AMI"

![ec21](https://github.com/user-attachments/assets/3803c107-c5a0-4bf0-ba97-e30372f0bce4)

- Em instance type selecione a opção t2.micro
- Em key pair selecione a chave criada anteriormente
- Na área network settings, escolha a VPC criada para o EC2 no campo security group
- Se você for um compasser, na área "Resource tags" coloque as tags disponibilizadas para lançamento das instâncias EC2, caso contrário você pode pular esta etapa
- Em "Additional configuration" procure o campo user data e coloque o seguinte script:
`#!/bin/bash

sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

sudo yum install -y amazon-efs-utils
sudo systemctl start amazon-efs-utils
sudo systemctl enable amazon-efs-utils

sudo mkdir /mnt/efs

sudo echo "ID de seu EFS:/ /mnt/efs nfs4 nfsvers=4.1,rsize=1048576,wsize=1048576,hard,timeo=600,retrans=2,noresvport,_netdev 0 0" >> /etc/fstab
sudo mount -a

sudo mkdir /mnt/efs/wordpress


sudo cat <<EOF > /mnt/efs/docker-compose.yaml
version: '3.8'
services:
  wordpress:
    image: wordpress:latest
    restart: always
    ports:
      - 80:80
    environment:
      WORDPRESS_DB_HOST: <endpoint de seu RDS>
      WORDPRESS_DB_NAME: <nome de seu RDS>
      WORDPRESS_DB_USER: <usuário de seu RDS>
      WORDPRESS_DB_PASSWORD: <senha de seu RDS>
    volumes:
      - /mnt/efs/wordpress:/var/www/html
EOF

docker-compose -f /mnt/efs/docker-compose.yaml up -d
`
