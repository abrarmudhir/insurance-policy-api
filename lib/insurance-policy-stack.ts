import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Bucket, BucketEncryption } from 'aws-cdk-lib/aws-s3';
import { InstanceClass, InstanceSize, InstanceType, Peer, Port, SubnetType, Vpc } from 'aws-cdk-lib/aws-ec2';
import { Cluster, FargateTaskDefinition, ContainerImage, FargateService, DeploymentControllerType } from 'aws-cdk-lib/aws-ecs';
import * as ecs from 'aws-cdk-lib/aws-ecs'; // Import the ECS module
import { LogGroup, RetentionDays } from 'aws-cdk-lib/aws-logs';
import { Repository } from 'aws-cdk-lib/aws-ecr';
import { ApplicationLoadBalancer, ApplicationProtocol, ApplicationTargetGroup, ListenerAction, Protocol, TargetType } from 'aws-cdk-lib/aws-elasticloadbalancingv2';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { DatabaseInstance, DatabaseInstanceEngine, Credentials, PostgresEngineVersion } from 'aws-cdk-lib/aws-rds';
import { Role, ServicePrincipal, ManagedPolicy, PolicyStatement as IAMPolicyStatement, Effect, PolicyStatement, Policy } from 'aws-cdk-lib/aws-iam';

export class InsurancePolicyStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = new Vpc(this, 'InsurancePolicyVpc', {
      vpcName: 'insurance-policy-vpc',
      maxAzs: 2,
      natGateways: 1,
      subnetConfiguration: [
        {
          subnetType: SubnetType.PUBLIC,
          name: 'PublicSubnet',
          cidrMask: 24,
        },
        {
          subnetType: SubnetType.PRIVATE_WITH_EGRESS,
          name: 'PrivateSubnet',
          cidrMask: 24,
        },
      ],
    });

    const bucket = new Bucket(this, 'InsurancePolicyBucket', {
      bucketName: 'insurance-policy-bucket',
      encryption: BucketEncryption.S3_MANAGED
    });

    const dbSecret = new Secret(this, 'DatabaseSecret', {
      secretName: 'insurance-policy-db-credentials',
      generateSecretString: {
        secretStringTemplate: JSON.stringify({
          username: 'policyadmin',
        }),
        generateStringKey: 'password',
        excludeCharacters: '"@/\\'
      }
    });

    const dbInstance = new DatabaseInstance(this, 'InsurancePolicyDB', {
      instanceType: InstanceType.of(InstanceClass.T3, InstanceSize.MICRO),
      engine: DatabaseInstanceEngine.postgres({ version: PostgresEngineVersion.VER_16_4 }),
      vpc: vpc,
      credentials: Credentials.fromSecret(dbSecret),
      databaseName: 'insurance_db',
      publiclyAccessible: true,
      deletionProtection: false,
      backupRetention: cdk.Duration.days(1),
      port: 5432,
      vpcSubnets: {
        subnetType: SubnetType.PUBLIC  // CHANGE THIS
      },
    });

    // CHANGE THIS: FOR TESTING ONLY
    dbInstance.connections.allowFrom(Peer.anyIpv4(), Port.tcp(5432));

    const cluster = new Cluster(this, 'InsurancePolicyCluster', {
      clusterName: 'insurance-policy-cluster',
      vpc: vpc,
      defaultCloudMapNamespace: { name: 'insurance.local' }
    });

    const logGroup = new LogGroup(this, 'InsurancePolicyLogGroup', {
      logGroupName: 'insurance-policy-loggroup',
      retention: RetentionDays.ONE_WEEK
    });

    const repository = new Repository(this, 'InsurancePolicyRepository', {
      repositoryName: 'insurance-policy-repo',
    });

    const taskDefinition = new FargateTaskDefinition(this, 'InsurancePolicyTaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });
    taskDefinition.addContainer('InsurancePolicyContainer', {
      containerName: 'insurance-policy-container',
      image: ContainerImage.fromEcrRepository(repository),
      logging: new ecs.AwsLogDriver({
        streamPrefix: 'InsurancePolicy',
        logGroup: logGroup,
      }),
      portMappings: [{ containerPort: 8050 }],
    });

    const secretAccessPolicy = new PolicyStatement({
      actions: ['secretsmanager:GetSecretValue'],
      resources: [dbSecret.secretArn],
      effect: Effect.ALLOW,
    });
    
    const policy = new Policy(this, 'SecretAccessPolicy', {
      policyName: 'insurance-policy-policy',
      statements: [secretAccessPolicy],
    });
    taskDefinition.taskRole.attachInlinePolicy(policy);

    const fargateService = new FargateService(this, 'InsurancePolicyService', {
      serviceName: 'insurance-policy-service',
      cluster: cluster,
      taskDefinition: taskDefinition,
      desiredCount: 1,
      assignPublicIp: true,
      deploymentController: {
        type: DeploymentControllerType.ECS,
      }
    });

    const loadBalancer = new ApplicationLoadBalancer(this, 'InsurancePolicyALB', {
      vpc: vpc,
      internetFacing: true,
      loadBalancerName: 'insurance-policy-alb',
      vpcSubnets: {
        subnetType: SubnetType.PUBLIC
      },
    });

    const targetGroup = new ApplicationTargetGroup(this, 'InsurancePolicyTargetGroup', {
      vpc,
      port: 8050,
      protocol: ApplicationProtocol.HTTP,
      targetType: TargetType.IP,
      healthCheck: {
        path: '/api/health',
        protocol: Protocol.HTTP,
        interval: cdk.Duration.seconds(30),
        timeout: cdk.Duration.seconds(5),
        healthyThresholdCount: 2,
        unhealthyThresholdCount: 2,
      },
    });
    fargateService.attachToApplicationTargetGroup(targetGroup);

    loadBalancer.addListener('InsurancePolicyListener', {
      port: 80,
      open: true,
      defaultTargetGroups: [targetGroup],
    });

    new cdk.CfnOutput(this, 'LoadBalancerDNS', {
      exportName: 'insurance-policy-dns',  
      value: loadBalancer.loadBalancerDnsName,
      description: 'The DNS name of the load balancer',
    });

    new cdk.CfnOutput(this, 'FargateServiceArn', {
      exportName: 'insurance-policy-arn',  
      value: fargateService.serviceArn,
    });

    new cdk.CfnOutput(this, 'FargateServiceUrl', {
      exportName: 'insurance-policy-url',  
      value: `http://${fargateService.serviceArn}.amazonaws.com`,
    });
  }
}