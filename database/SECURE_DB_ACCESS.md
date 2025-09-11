# Secure Database Access Guide

## Security Considerations

**NEVER expose PostgreSQL port 5432 directly to the internet!** This can lead to:
- Brute force attacks on database credentials
- Potential data breaches
- Resource exhaustion attacks
- Unauthorized data access

## Secure Connection Methods

### Method 1: SSH Tunnel (RECOMMENDED)

Create an SSH tunnel from your local machine to your VM:

```bash
# Open SSH tunnel on your local machine
ssh -L 5432:localhost:5432 eric@your-vm-ip-address

# Keep this terminal open while using pgAdmin
```

Then in pgAdmin:
- Host: `localhost` (not your VM IP)
- Port: `5432`
- Database: `notatherapist_db`
- Username: `notatherapist`
- Password: `notatherapist_secure_pwd_2024`

### Method 2: Docker Exec (Most Secure for Administration)

Connect directly on the VM without any network exposure:

```bash
# SSH into your VM first
ssh eric@your-vm-ip-address

# Then connect to PostgreSQL
docker exec -it notatherapist-postgres psql -U notatherapist -d notatherapist_db
```

### Method 3: pgAdmin in Docker (For Regular Use)

Deploy pgAdmin as a Docker container on the same network:

```yaml
# Add to docker-compose.yml (for secure internal access)
pgadmin:
  image: dpage/pgadmin4:latest
  container_name: notatherapist-pgadmin
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@notatherapist.com
    PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-changeme}
    PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION: 'True'
    PGADMIN_CONFIG_CONSOLE_LOG_LEVEL: 10
  ports:
    - "8080:80"  # Access pgAdmin at http://localhost:8080
  volumes:
    - pgadmin_data:/var/lib/pgadmin
  networks:
    - notatherapist-network
  depends_on:
    - postgres
```

Then connect pgAdmin to PostgreSQL using internal Docker network:
- Host: `postgres` (Docker service name)
- Port: `5432`
- Database: `notatherapist_db`
- Username: `notatherapist`
- Password: from .env file

### Method 4: Bastion Host / Jump Server

For production environments, use a dedicated bastion host:

1. Create a separate, hardened VM as bastion
2. Only allow SSH to bastion from specific IPs
3. Connect to database VM only through bastion
4. Use SSH tunneling through bastion

## Security Best Practices

1. **Strong Passwords**: Use long, random passwords (already configured in .env)

2. **Network Isolation**: Keep database in internal Docker network (already configured)

3. **Firewall Rules**: 
   ```bash
   # Only allow PostgreSQL from localhost
   sudo ufw deny 5432
   sudo ufw allow from 127.0.0.1 to any port 5432
   ```

4. **SSL/TLS Connections**: Enable SSL for PostgreSQL connections (for production)

5. **Regular Updates**: Keep PostgreSQL and all containers updated

6. **Audit Logging**: Enable PostgreSQL logging for security audits

7. **Backup Encryption**: Encrypt database backups at rest

## Quick SSH Tunnel Setup for pgAdmin

1. **On your local machine**, create the tunnel:
   ```bash
   ssh -L 5432:localhost:5432 -N -f eric@your-vm-ip
   ```
   - `-L 5432:localhost:5432` - Forward local port 5432 to remote localhost:5432
   - `-N` - Don't execute remote command
   - `-f` - Run in background

2. **In pgAdmin**, connect to:
   - Host: `127.0.0.1`
   - Port: `5432`
   - Username: `notatherapist`
   - Password: `notatherapist_secure_pwd_2024`

3. **To close the tunnel**:
   ```bash
   # Find the SSH process
   ps aux | grep "ssh -L 5432"
   # Kill it
   kill <process-id>
   ```

## Current Security Status

✅ Database NOT exposed to external network
✅ Using Unix sockets for internal connections
✅ Strong passwords in environment variables
✅ Network isolation via Docker networks
✅ .env file excluded from git

## For Development Only

If you absolutely need to expose the port temporarily for local development:

1. Uncomment the ports section in docker-compose.yml
2. Restart the container
3. **IMMEDIATELY** revert when done
4. Never commit this change to git

Remember: The database contains user inputs and must be protected!