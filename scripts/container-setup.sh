
#!/bin/bash

## Configure Docker Container
sudo apt-get update -y
sudo apt install docker.io -y
sudo apt-get install git -y

# Clone repo in news-bot folder
sudo systemctl enable --now docker
sudo usermod -aG docker donald
