pipeline {
    agent any
    stages {
        stage('Build Docker') {
            steps {
                sh '''
		  docker version
		'''
            }
        }
        stage('Check OWASP') {
            steps {
				echo 'Check OWASP Stage'
//				dependencyCheck additionalArguments: ''' 
//                    -o './'
//                    -s './'
//                    -f 'ALL' 
//                    --prettyPrint''', odcInstallation: 'OWASP Dependency-Check Vulnerabilities'

//				dependencyCheckPublisher pattern: 'dependency-check-report.xml' 
			}
		}
    }
}
