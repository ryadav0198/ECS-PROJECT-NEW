pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "us-east-1"
        AWS_ACCOUNT_ID     = "269172689648"
        ECR_REPO           = "myapp/dev"                 // ECR repo name
        IMAGE_TAG          = "latest"                    // you can also use "${BUILD_NUMBER}"
        CLUSTER_NAME       = "my-ecs-cluster"            // replace with your ECS cluster name
        SERVICE_NAME       = "my-ecs-service"            // replace with your ECS service name
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/ryadav0198/ECS-PROJECT-NEW.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
            }
        }

        stage('Login to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_DEFAULT_REGION}") {
                    sh '''
                    aws ecr get-login-password --region $AWS_DEFAULT_REGION | \
                    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_DEFAULT_REGION}") {
                    sh '''
                    docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                withAWS(credentials: 'aws-creds', region: "${AWS_DEFAULT_REGION}") {
                    sh '''
                    echo "Forcing ECS service to use the new image..."
                    aws ecs update-service \
                        --cluster $CLUSTER_NAME \
                        --service $SERVICE_NAME \
                        --force-new-deployment \
                        --region $AWS_DEFAULT_REGION
                    '''
                }
            }
        }
    }
}

