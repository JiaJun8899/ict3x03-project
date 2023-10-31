pipeline {
    agent any
    tools {nodejs "NodeJS"}
    environment {
        SEMGREP_APP_TOKEN = credentials('SEMGREP_APP_TOKEN')
    }
    stages {
        stage('Test Docker') {
            steps {
                sh '''
                docker version
                '''
            }
        }
        stage('Installing dependencies on NextJS') {
            steps {
                dir('frontend') {
                    sh '''
                    npm install
                    '''
                }
            }
        }
        stage('Semgrep Scan') {
            steps {
                echo 'SAST Scanning'
                sh 'semgrep scan'
            }
        }
        stage('Setting up container') {
            steps{
                echo 'Setting up Container'
                sh '''
                docker compose up --build -d
                '''
            }
        }
        stage('Check OWASP') {
            steps {
                echo 'Check OWASP Stage'
                // Add your OWASP Dependency-Check configuration here if needed
                dependencyCheck additionalArguments: ''' 
                     -o './'
                     -s './'
                     -f 'ALL' 
                     --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                dependencyCheckPublisher pattern: 'dependency-check-report.xml' 
            }
        }
        stage('Testing Stage'){
            steps {
                sh '''
                docker exec django_backend python manage.py test
                '''
            }
        }
    }
    post {
        //Only run docker compose down when the build is successful
        always {
            script {
                // Containers are running, check their status
                def frontendContainer = sh(script: 'docker inspect -f "{{.State.Status}}" nexjs_frontend', returnStdout: true).trim()
                def backendContainer = sh(script: 'docker inspect -f "{{.State.Status}}" django_backend', returnStdout: true).trim()
                def dbContainer = sh(script: 'docker inspect -f "{{.State.Status}}" backend_database', returnStdout: true).trim()
                // Check if any container's status is not "Up"
                if (frontendContainer != 'running' || backendContainer != 'running' || dbContainer != 'running') {
                        // At least one container is running but not "Up," send an email
                    emailext subject: "Docker Container Status Issue",
                        body: "One or more Docker containers are not in an 'Up' state. Please investigate.",
                        to: '2100755@sit.singaporetech.edu.sg'
                    sh '''
                    docker compose down
                    docker container prune -f
                    '''
                } else {
                    // All containers are running and are "Up"
                    echo "All Docker containers are running and in 'Up' state."
                    emailext subject: "Jenkins built is successful!",
                        body: "The most recent commit has no issue!",
                        to: '2100755@sit.singaporetech.edu.sg'
                    sh '''
                    docker compose down
                    docker container prune -f
                    '''
                }
            }
        }
        // If the build has failed, send an email to notify
        failure {
            script {
                emailext body: '$DEFAULT_CONTENT', subject: '$DEFAULT_SUBJECT', to: '2100755@sit.singaporetech.edu.sg'   
        }
    }
}
}
