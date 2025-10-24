mkdir -p ~/.streamlit

echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml

curl -fsSL https://ollama.com/install.sh | sh


echo "Téléchargement du modèle Mistral 7B Instruct..."
ollama pull mistral:7b-instruct
