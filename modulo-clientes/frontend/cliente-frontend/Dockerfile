FROM node:20-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências
COPY package*.json ./
COPY pnpm-lock.yaml ./

# Instala o pnpm globalmente
RUN npm install -g pnpm

# Instala as dependências
RUN pnpm install

# Copia o código da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 3000

# Comando para executar a aplicação em modo de desenvolvimento
CMD ["pnpm", "run", "dev", "--host"]

