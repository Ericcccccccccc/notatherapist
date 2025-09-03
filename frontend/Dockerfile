FROM caddy:alpine

# Copy website files
COPY index.html style.css app.js /srv/

# Copy Caddyfile - the production one will be mounted as a volume
COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 80 443

CMD ["caddy", "run", "--config", "/etc/caddy/Caddyfile"]