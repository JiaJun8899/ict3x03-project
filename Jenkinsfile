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
        stage('Semgrep Scan') {
            steps {
                echo 'SAST Scanning'
                sh 'semgrep scan'
            }
        }
		stage('Installing dependencies on NextJS') {
            steps {
                dir('./frontend') {
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
        //stage('Setting up container') {
        //    steps{
				//dir('/home/production_2') {
		//			echo 'Setting up Container'
		//			sh '''
		//			docker compose -f docker-compose.yml up --build -d
		//			'''
				//}
        //    }
        //}
        //stage('Testing Stage'){
        //    steps {
        //        sh '''
        //        docker exec django_backend python manage.py test
        //        '''
        //    }
        //}
		stage('Deployment stage, pulling code to production_2') {
			steps {
				echo 'Pulling code from github'
				script {
					dir('/home/production_2') {
						git branch:'jenkins-test', url:'https://github.com/JiaJun8899/ict3x03-project.git'
					}
				}
			}
		}
    }
}
