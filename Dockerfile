# Usa a imagem oficial do n8n como base
FROM n8nio/n8n:latest

# Troca para usuário root para poder instalar coisas
USER root

# Instala o Python 3
RUN apk add --update --no-cache python3 py3-pip

# Volta para o usuário padrão do n8n (segurança)
USER node