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
		stage('Pulling code') {
			script {
				sh 'cd /home/production_2 && git pull origin jenkins-test'
			}
		}
        //stage('Setting up container') {
        //    steps{
        //        echo 'Setting up Container'
        //        sh '''
        //        docker compose up --build -d
        //        '''
        //    }
        //}
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
        //stage('Testing Stage'){
        //    steps {
        //        sh '''
        //        docker exec django_backend python manage.py test
        //        '''
        //    }
        //}
    }
}
