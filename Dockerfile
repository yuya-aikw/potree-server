# Stage 1
FROM node:20 AS builder

# clone Potree repository
WORKDIR /potree
RUN git clone https://github.com/potree/potree.git .

# build
RUN npm install

# Stage 2
FROM nginx:alpine

# copy Potree files from the builder stage
COPY --from=builder /potree /usr/share/nginx/potree

# copy Nginx configuration
# COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]