FROM node:22-alpine

WORKDIR /app

copy package.json package-lock.json .
RUN npm install
#kopio kaiken build-kontekstista
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]