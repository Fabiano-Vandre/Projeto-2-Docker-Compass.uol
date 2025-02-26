#!/bin/bash
sudo dnf check-update
sudo dnf upgrade -y
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
