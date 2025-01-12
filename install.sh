sudo apt update
sudo apt upgrade

python -m venv --system-site-packages env_DIYHomeAssistantClient
source env_DIYHomeAssistantClient/bin/activate

pip install -r requirements.txt