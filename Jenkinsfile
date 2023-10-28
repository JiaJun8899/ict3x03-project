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
                sh 'semgrep ci'
            }
        }
        stage('Setting up container') {
            steps{
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
                echo 'TBD -> Test cases by SE'
            }
        }
    }
    post {
        //Only run docker compose down when the build is successful
        always {
            script {
                sh '''
                docker compose down
                docker container prune -f
                '''
            }
        }
        failure {
            echo 'Something went wrong'
        }
    }
}
