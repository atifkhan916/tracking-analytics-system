Key features of this network setup:

VPC with public and private subnets across two availability zones
Internet Gateway for public internet access
NAT Gateway for private subnet internet access
Separate route tables for public and private subnets
Remote state storage in S3 with state locking using DynamoDB
Properly tagged resources for easy management


terraform plan -var-file="terraform.tfvars" -var-file="secrets.tfvars"
terraform apply -var-file="terraform.tfvars" -var-file="secrets.tfvars"

or 

export TF_VAR_db_password="your-secure-password-here"
terraform plan -var-file="terraform.tfvars"


This FastAPI application provides:

Data Models:

TrackingEvent: For user activity data
MarketingTouchpoint: For marketing campaign data


API Endpoints:

/health: Health check endpoint
/tracking/events/: Create and list tracking events
/marketing/touchpoints/: Create and list marketing touchpoints
/analytics/user/{user_id}: Get user analytics


local setup

# .env
DB_NAME=tracking-analytics
DB_USER=dbadmin
DB_PASSWORD=dbpassword

Start the services:
docker-compose up -d

View logs:
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app


# Access the services:
FastAPI app: http://localhost:8000
Database: localhost:5432


# Stop the services:
docker-compose down

# Clean up everything including volumes:
docker-compose down -v


Features:

Database:

PostgreSQL 14
Persistent storage
Health checks
Environment variable configuration


Application:

Hot reload for development
Automatic migrations
Seed data population
Volume mounted code for live changes


Network:

Automatic network creation
Service discovery (db hostname)
Exposed ports for local access


Development:

Environment variables


Code hot reloading
Easy database access

CI/CD pipeline
----------------
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
DB_NAME_DEV
DB_PASSWORD_DEV
DB_USER_DEV
