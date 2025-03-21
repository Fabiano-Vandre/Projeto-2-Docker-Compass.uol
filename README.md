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


Obs: As regras de saída ou Outbound Rules deixaremos na forma padrão


### EC2 SG Inbound Rules

| Type  | Port | Source |  
| ----- | ---- | -------- |
| HTTP  | 80  | Load Balancer SG |

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

## 5. Criação do Secrets Manager
Agora criaremos um local para guardar os dados sensíveis do RDS
- Pesquise pelo serviço secret manager e clique em create secret

![secret1](https://github.com/user-attachments/assets/5303a352-cf53-499f-87e4-b77044259e1e)

- Preencha as informações do seu RDS e em "Encription Key" selecione a chave padrão do AWS
- Selecione seu RDS e clique em next

![secret2](https://github.com/user-attachments/assets/b6b0304a-0b7f-4414-a84a-c7b13e8359f1)

- Digite o nome do seu Secrets e clique em next

![secret3](https://github.com/user-attachments/assets/cb9aec80-f8a5-4608-8117-3729909500c4)

- Para ter mais segurança clique em automatic rotation e coloque as configurações acima
- Agora clique em create secret

![secretretrive](https://github.com/user-attachments/assets/a08ee3d6-7168-4e1c-b7c4-aac993f2c72b)

- Entre no seu secret e clique em retrieve secret value (Você usará esses valores no script)

## 6. Criação do Key pair
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
```
#!/bin/bash

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
```

## 7. Criação do Load Balancer Classic
Pesquise pelo serviço de Load Balancer e clique em create load balancer
- Procure pela opção "Classic Load Balancer e clique em create"

![lb1](https://github.com/user-attachments/assets/88a449bd-8187-4109-8433-3be2414b985b)

![lb2](https://github.com/user-attachments/assets/5ad6b592-eb14-4e7e-b306-185b32b82c26)

- Digite o nome do seu Load balancer no campo "Load Balancer Name"
- Em Network Mapping no campo VPC selecione a VPC criada para o projeo
- Em availability zones and subnets selecione as 2 AZs e em subnets escolha as públicas disponíveis
- Em security group selecione o sg criado para o Load Balancer (LB SG)
- No campo ping path digite apenas "/wp-admin/install.php" como mostrado no exemplo acima e clique em create load balancer

## 8. Instalação do Wordpress
Para instalar o Wordpress lançaremos uma instância em uma subnet pública
- Entre na área de instâncias EC2 e clique na opção "Launch instance from template"
- Escolha uma subnet pública e lance a instância
- Agora vá para o load balancer e clique em manage instances

![manage](https://github.com/user-attachments/assets/58bda22c-be95-4407-8100-667e5889ca10)

- Selecione e adicione a instância
- CLique encima do nome do seu load balancer

![dns](https://github.com/user-attachments/assets/23482f40-ad79-48a2-900b-2b8fcffe2ca9)

- Copie o DNS name e cole no seu navegador
- Aparecerá a seguinte tela:

![wp](https://github.com/user-attachments/assets/b993d590-71c5-42a9-a3bb-e97416bc311d)

- Após isso é só instalar a sua aplicação wordpress.

## 9. Criação do Auto Scaling Group
Pesquise pelo serviço de Auto Scaling Group e clique em create Auto Scaling Group
- Digite o nome do seu Auto Scaling Group e abaixo selecione o launch template que você criou
- Clique em Next

![asg1](https://github.com/user-attachments/assets/01fe7c27-9575-4c42-bc10-e03885b3cbf5)

- Em VPC selecione a VPC do projeto

![asg1](https://github.com/user-attachments/assets/585e5a9a-d042-438d-a8a0-315d935b9ba7)

- Em Availability zones and subnets escolha as 2 subnets privadas
- Clique em Next

![asg2v](https://github.com/user-attachments/assets/8d624805-d1da-49bf-9d70-6b4aebe2c5ba)

- Em Load Balancing selecione a opção Attach to an exising Load Balancer
- Abaixo escolha a opção Choose from Classic Load Balancer e selecione o Load Balancer criado para o projeto
- Clique em Next

![asg3](https://github.com/user-attachments/assets/7a98cdc9-1deb-4c5c-ad53-36f60e11fc7c)

- Em Desired capacity digite 2 para criar 2 instâncias
- Abaixo em "Min desired capacity" digite 2 e no campo ao lado digite 4

![disponibilidade](https://github.com/user-attachments/assets/80be7828-5dc0-4329-b920-11a54c927e71)

- Em instance maintenance policy escolha "Priorize Availability
- Clique em next até aparecer a opção create auto scaling group e clique nela

## 10. Criação do Dashboards
Para melhor visualização das requisições criaremos um dashboard
- Pesquise pelo serviço Cloudwatch e entre na área de Dashboards
- Clique em create dashboard
- Escolha a opção Stacked Line

![request](https://github.com/user-attachments/assets/79b3c834-6962-4c66-acca-28c397f98cad)

- Selecione a opção "ELB" e "Per-LB Metrics"
- Pesquise pela opção "Request-Count" do seu LB
- Escolha o seu Load balancer e salve o dashboard

 ## 11. Criação das ASG Policies
 Agora criaremos as políticas de escalabilidade do Auto Scaling group

 ![scalingpolicie](https://github.com/user-attachments/assets/16f54557-c5df-4024-a43c-746d6a6a8205)

- Clique no seu auto scaling group e selecione a opção "Automatic Scaling"
- Clique em create dynamic scaling policies
- Crie uma regra com configurações abaixo

![addintance](https://github.com/user-attachments/assets/8d4bd335-f394-4ad7-89df-eff65894d008)

- Para criar o alarme para adicionar instâncias clique em create alarm
- Clique em selecionar métrica

![alarm1](https://github.com/user-attachments/assets/8f65fffb-8466-4c0b-a9a8-72501b844197)

- Selecione as opções "ELB" e "Per-LB Metrics"
- Pesquise pela opção "Request-Count" do seu LB e selecione-a
- Agora coloque as seguintes configurações abaixo

![alarm1notificação](https://github.com/user-attachments/assets/50ec3968-c036-43a3-9830-972c858c4249)

![alarm1regra](https://github.com/user-attachments/assets/2447ff91-bacd-4348-81f3-807e69e84464)

- Clique em create alarm novamente
- Agora criaremos o alarme para remover instâncias clique em create alarm
- Crie um alarme com as regras abaixo

![alarm2](https://github.com/user-attachments/assets/81f2cc53-a917-4072-9d6c-b1ffd87f73b8)

- Clique em next
- Nos próximos passos utilize as configurações do alarme anterior

- Para criar a política de remover instâncias usaremos as seguintes configurações

![removeinstancesregra](https://github.com/user-attachments/assets/4b2caf66-622b-482f-ab06-25bc73bc9167)

## 12. Script para requisições
Agora para automatizar os testes das nossas políticas usaremos o seguinte script feito em python

```
import requests
import threading
import time

# URL do seu Load Balancer
LOAD_BALANCER_URL = "http://URLdoSeuLoadBalancer"

# Número total de requisições
TOTAL_REQUESTS = 30

# Número de threads simultâneas
NUM_THREADS = 10

def make_request():
    """Função que faz uma requisição GET ao Load Balancer"""
    try:
        response = requests.get(LOAD_BALANCER_URL, timeout=5)
        print(f"Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro: {e}")

def start_load_test():
    """Cria múltiplas threads para enviar requisições simultâneas"""
    threads = []
    for _ in range(TOTAL_REQUESTS):
        thread = threading.Thread(target=make_request)
        thread.start()
        threads.append(thread)

        # Limitar a taxa de requisições
        if len(threads) >= NUM_THREADS:
            for t in threads:
                t.join()  # Espera as threads terminarem
            threads = []  # Limpa a lista para criar novas threads

    # Espera todas as threads finalizarem
    for t in threads:
        t.join()

if __name__ == "__main__":
    print(f"Iniciando teste de carga em {LOAD_BALANCER_URL} com {TOTAL_REQUESTS} requisições.")
    start_time = time.time()
    
    start_load_test()
    
    print(f"Teste concluído em {time.time() - start_time:.2f} segundos.")
```

Dentro do diretório do projeto execute-o com o comando:

```
python request.py
```

Caso não tenha o python instalado será necessário instalá-lo
