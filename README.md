# NutrifAI - Lambda AI-Powered Diet Generator
This repository contains an AWS Lambda function utilizing Gemini to generate personalized diet plans. The deployment is managed using Terraform and integrates with other AWS services.

## Key Features

- **AWS Lambda**: Core serverless function to handle requests and generate diet plans with Gemini.
- **AI Model**: Processes user input to generate personalized diet recommendations

## Requirements

To use this project, ensure you have the following installed:
- [Terraform](https://www.terraform.io/downloads)
- [AWS CLI](https://aws.amazon.com/cli/) configured with appropriate permissions

Ensure that your AWS credentials are configured correctly using `aws configure`

## Instructions to Deploy Locally

### 1. Clone the repository
```bash
git clone https://github.com/Nutrifai/lambda-ai.git
cd infra
```

### 2. Initialize Terraform
Before running any commands, initialize Terraform in the project directory.
```bash
terraform init
```

### 3. Plan the Deployment
Generate and review an execution plan to understand the resources that will be created or updated.
```bash
terraform plan
```

### 4. Apply the Configuration
To deploy the resources to AWS, run:
```bash
terraform apply -auto-approve
```

### Outputs
After deploying the infrastructure, Terraform will output useful information such as the API Gateway URL and Lambda function ARN. You can customize these outputs in the `outputs.tf` files.