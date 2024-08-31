# Overview

**Insurance Policy Management API** is a FastAPI app for managing insurance policies. It includes endpoints for policy management, health checks, and supports deployment via Docker and AWS CDK.

## Setup Instructions

### Prerequisites

- Docker
- AWS CLI
- Node.js (for AWS CDK)
- Poetry (for Python)

### Clone the Repository

```sh
git https://github.com/abrarmudhir/insurance-policy-api.git
cd insurance-policy-api
```

### Install Dependencies

- **Python**:
  ```sh
  poetry install
  ```

- **Node.js**:
  ```sh
  npm install
  ```

### Build and Run Locally with Docker

1. Navigate to the server directory:
   ```sh
   cd server
   ```

2. Build the Docker image:
   ```sh
   docker-compose -f docker-compose.yml build
   ```

3. Start the Docker containers:
   ```sh
   docker-compose up -d
   ```

4. View logs:
   ```sh
   docker-compose logs -f --tail=200
   ```

5. Rebuild if needed:
   ```sh
   docker-compose up --build
   ```

## Running Tests

### Unit Tests

```sh
npm run test
```

### Integration Tests

```sh
poetry run pytest
```

## API Documentation

### Endpoints

- **Health Check**
  - **URL**: `/api/health`
  - **Method**: GET
  - **Response**: `{"status": "ok"}`

- **Get Policies**
  - **URL**: `/api/policies`
  - **Method**: GET
  - **Query Parameters**:
    - `skip` (optional, default: 0): Number of policies to skip.
    - `limit` (optional, default: 10): Number of policies to return.
  - **Response**: List of policies.

- **Get Policy by ID**
  - **URL**: `/api/policies/{policy_id}`
  - **Method**: GET
  - **Path Parameter**:
    - `policy_id`: ID of the policy.
  - **Response**: Policy details.

## Deployment Instructions

### Local Deployment with Docker

1. Build and tag the Docker image:
   ```sh
   docker-compose -f server/docker-compose.yml build
   docker tag server-api:latest insurance-policy:latest
   docker tag insurance-policy:latest <account_id>.dkr.ecr.eu-west-2.amazonaws.com/insurance-policy-repo:latest
   ```

2. Authenticate Docker to AWS ECR:
   ```sh
   aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.eu-west-2.amazonaws.com
   ```

3. Push the image to ECR:
   ```sh
   docker push <account_id>.dkr.ecr.eu-west-2.amazonaws.com/insurance-policy-repo:latest
   ```

### AWS CDK Deployment

1. Deploy the stack:
   ```sh
   npx cdk deploy
   ```

2. Compare stack states:
   ```sh
   npx cdk diff
   ```

3. Generate the CloudFormation template:
   ```sh
   npx cdk synth
   ```

## Health Endpoint

Access Health Endpoint:
```
http://insurance-policy-alb-<ARN>.eu-west-2.elb.amazonaws.com/api/health
```

Access Policy Endpoint:
```
http://insurance-policy-alb-<ARN>.eu-west-2.elb.amazonaws.com/api/policies
```

## Future Enhancements

- **Enhanced Filtering**: Advanced policy search capabilities.
- **User Authentication**: Add user authentication and authorization.
- **Rate Limiting**: Implement rate limiting.
- **CI/CD Pipeline**: Automate testing, building, and deployment.