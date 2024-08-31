import { execSync, ExecSyncOptions } from 'child_process';

class BuildAndPush {
  private accountId: string;
  private region: string;
  private repositoryName: string;
  private imageUri: string;

  constructor() {
    this.accountId = process.env.CDK_DEFAULT_ACCOUNT || '783764617885';
    this.region = process.env.CDK_DEFAULT_REGION || 'eu-west-2';
    
    if (!this.accountId || !this.region) {
      throw new Error('CDK_DEFAULT_ACCOUNT or CDK_DEFAULT_REGION environment variables are not set.');
    }

    this.repositoryName = 'insurance-policy-repo';
    this.imageUri = `${this.accountId}.dkr.ecr.${this.region}.amazonaws.com/${this.repositoryName}:latest`;
  }

  run() {
    try {
      const options: ExecSyncOptions = { stdio: 'inherit'};

      // Build the Docker image using docker-compose
      execSync('docker-compose -f server/docker-compose.yml build', options);

      try {
        // Tag the Docker image
        execSync(`docker tag insurance-policy:latest ${this.imageUri}`, options);
      } catch (error) {
        console.error('Error tagging the Docker image:', error);
        throw error;
      }

      // Authenticate Docker with ECR
      execSync(
        `aws ecr get-login-password --region ${this.region} | docker login --username AWS --password-stdin ${this.accountId}.dkr.ecr.${this.region}.amazonaws.com`,
        options
      );

      // Push the image to ECR
      execSync(`docker push ${this.imageUri}`, options);

      console.log(`Docker image pushed to: ${this.imageUri}`);
    } catch (error) {
      console.error('Error during build and push:', error);
    }
  }
}

// Run the build and push process
new BuildAndPush().run();
