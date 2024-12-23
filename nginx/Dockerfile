FROM nginx:1.25-alpine

# Install OpenSSL to generate certificates
RUN apk add --no-cache openssl

# Create SSL directory
RUN mkdir -p /etc/nginx/ssl

# Generate self-signed certificates
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/devalerts.key \
    -out /etc/nginx/ssl/devalerts.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

