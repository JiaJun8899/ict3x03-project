pipeline {
    agent any
    stages {
        stage('Test Docker') {
            steps {
                sh '''
                docker version
                docker compose version
                '''
            }
        }
        stage('Build Container') {
            steps {
                echo 'TBD -> Setting up env for testing'
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
        always {
            echo 'TBD -> shutdown docker compose'
        }
    }
}
