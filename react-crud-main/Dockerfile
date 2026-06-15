FROM node:16 AS builder
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH

# install deps
COPY package.json tsconfig.json ./
RUN npm install --silent

# copy source and build
COPY public ./public
COPY src ./src
RUN npm run build

# nginx stage
FROM nginx:stable-alpine
COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]