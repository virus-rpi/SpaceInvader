# Use the official PostgreSQL image as the base image
FROM postgres

# Set environment variables
ENV POSTGRES_USER=dbUser
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=ips

# Copy the SQL script to create the table
COPY db.sql /docker-entrypoint-initdb.d/

# Grant admin privileges to the user
RUN echo "ALTER USER dbUser WITH SUPERUSER;" >> /docker-entrypoint-initdb.d/db.sql
