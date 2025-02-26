#!/bin/bash
sudo yum check-update
sudo yum upgrade -y
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
