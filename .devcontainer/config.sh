#!/bin/bash
set -e
# execute o comando chmod +x config.sh
sudo apt update
sudo apt install -y build-essential libpq-dev locales gpg
sudo mkdir -p /etc/apt/keyrings
wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc | sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg
echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" | sudo tee /etc/apt/sources.list.d/gierens.list
sudo chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list
sudo apt update
sudo apt install -y eza


sudo locale-gen pt_BR.UTF-8
sudo update-locale LANG=pt_BR.UTF-8

echo "alias ls='eza --icons'" >> ~/.zshrc
echo "eval \"\$(starship init zsh)\"" >> ~/.zshrc

ZSH_CUSTOM=${ZSH_CUSTOM:-~/.oh-my-zsh/custom}
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

# Instalar Starship
curl -fsSL https://starship.rs/install.sh | sh -s -- -y

sudo chown -R $USER:$USER /workspaces/

# Execute source ~/.zshrc para aplicar as mudanças