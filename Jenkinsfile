pipeline {
    agent any
    tools {nodejs "NodeJS"}
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
        // stage('Setting up container') {
        //     steps{
        //         sh '''
        //         docker compose up --build -d
        //         '''
        //     }
        // }
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
        // Only run docker compose down when the build is successful
        success {
            script {
                sh '''
                docker compose down
                docker container prune -f
                '''
            }
        }
        failure {
            echo "Build failure"
        }
        // Clean up workspace
        cleanup {
            echo "Cleaning workspace"
            cleanWs()
        }
    }
}
