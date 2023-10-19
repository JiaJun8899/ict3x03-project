pipeline {
    agent any
    stages {
        stage('Verify Docker') {
            steps {
                sh '''
		  docker version
		'''
            }
        }
	stage('Prune Docker Data') {
	    steps {
		sh 'docker system prune -a --volumes -f'
	    }
	}
	stage('Start Containers') {
	    steps {
	        sh 'docker compose up --build -d --wait'
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
