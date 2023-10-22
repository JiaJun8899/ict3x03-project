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
        stage('Set up frontend') {
            steps {
                dir('frontend') {
                    sh '''
                    npm install
                    '''
                }
                
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
