# Use the official PostgreSQL image as the base image
FROM postgres

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=123456
ENV POSTGRES_DB=ips

# Copy the SQL script to create the table
COPY db.sql /docker-entrypoint-initdb.d/
