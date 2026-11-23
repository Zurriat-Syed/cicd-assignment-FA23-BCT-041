pipeline {
    agent any

    environment {
        IMAGE      = 'cicd-site'
        TEST_IMAGE = 'cicd-site-tests'
        NETWORK    = 'staging-net'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --oneline'
            }
        }

        stage('Package') {
            steps {
                sh 'docker build -t ${IMAGE}:${BUILD_NUMBER} -t ${IMAGE}:latest .'
            }
        }

        stage('Start Staging') {
            steps {
                sh '''
                    docker network create ${NETWORK} 2>/dev/null || true
                    docker rm -f staging 2>/dev/null || true
                    docker run -d --name staging --network ${NETWORK} --network-alias staging ${IMAGE}:${BUILD_NUMBER}
                    sleep 3
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    rm -rf results && mkdir -p results
                    docker build -t ${TEST_IMAGE} tests
                    docker run --rm --network ${NETWORK} -e BASE_URL=http://staging \
                        -v "$WORKSPACE/results:/results" ${TEST_IMAGE}
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'results/junit.xml'
                    archiveArtifacts artifacts: 'results/*', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker rm -f live 2>/dev/null || true
                    docker run -d --name live --restart unless-stopped -p 80:80 ${IMAGE}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f staging 2>/dev/null || true'
        }
        success {
            echo "Build ${BUILD_NUMBER}: tests passed and site deployed."
        }
        failure {
            echo "Build ${BUILD_NUMBER}: failed - deploy skipped, live site unchanged."
        }
    }
}
