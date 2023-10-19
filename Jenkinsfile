pipeline {
    agent any
    stages {
        stage('Test Docker') {
            step {
                sh '''
                docker version
                '''
            }
        }
        stage('Build Test Docker') {
            agent {
                docker { image 'node:16-alpine' }
            } 
            steps {
                echo 'Done'
            }
        }
        stage('Check OWASP') {
            steps {
                echo 'Check OWASP Stage'
                // Add your OWASP Dependency-Check configuration here if needed
                // dependencyCheck additionalArguments: ''' 
                //     -o './'
                //     -s './'
                //     -f 'ALL' 
                //     --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'
                // dependencyCheckPublisher pattern: 'dependency-check-report.xml' 
            }
        }
    }
}
