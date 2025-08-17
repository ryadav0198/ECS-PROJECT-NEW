pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "269172689648"
        ECR_REPO = "myapp/dev"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/ryadav0198/ECS-PROJECT-NEW.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $ECR_REPO:$IMAGE_TAG .'
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh 'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com'
                }
            }
        }

        stage('Tag & Push to ECR') {
            steps {
                script {
                    sh '''
                    docker tag $ECR_REPO:$IMAGE_TAG $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO:$IMAGE_TAG
                    '''
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    sh '''
                    aws ecs update-service \
                        --cluster Web-Page-Cluster \
                        --service My-app-services \
                        --force-new-deployment \
                        --region $AWS_DEFAULT_REGION
                    '''
                }
            }
        }
    }
}

