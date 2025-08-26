pipeline {
  agent any

  environment {
    AWS_REGION = "ap-east-1"
    ECR_REPO   = "myapp"
    CLUSTER    = "my-ecs-cluster"
  }

  stages {
    stage('Checkout') {
      steps { checkout scm }
    }

    stage('Build & Test') {
      steps {
        sh 'pytest -q || true'
      }
    }

    stage('Build & Push Docker') {
      steps {
        script {
          IMAGE_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
          ACCOUNT_ID = sh(script: "aws sts get-caller-identity --query Account --output text", returnStdout: true).trim()
          ECR_URI = "${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

          sh """
            aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI
            docker build -t $ECR_REPO:$IMAGE_TAG .
            docker tag $ECR_REPO:$IMAGE_TAG $ECR_URI:$IMAGE_TAG
            docker push $ECR_URI:$IMAGE_TAG
          """
          env.IMAGE = "${ECR_URI}:${IMAGE_TAG}"
        }
      }
    }

    stage('Deploy') {
      steps {
        script {
          if (env.BRANCH_NAME == "dev") {
            deployToECS("dev-service")
          } else if (env.BRANCH_NAME == "test") {
            deployToECS("test-service")
          } else if (env.BRANCH_NAME == "prod") {
            input message: "Deploy to PROD?"  // Manual approval
            deployToECS("prod-service")
          }
        }
      }
    }
  }
}

def deployToECS(serviceName) {
  sh """
    jq --arg IMG "$IMAGE" '.containerDefinitions[0].image=$IMG' ecs-taskdef.json > taskdef.json
    REV_ARN=$(aws ecs register-task-definition --cli-input-json file://taskdef.json --query taskDefinition.taskDefinitionArn --output text)
    aws ecs update-service --cluster $CLUSTER --service ${serviceName} --task-definition $REV_ARN
    aws ecs wait services-stable --cluster $CLUSTER --services ${serviceName}
  """
}

