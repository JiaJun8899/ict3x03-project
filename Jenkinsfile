pipeline {
    agent {
	    docker { image 'node:16-alpine' }
	}
    stages {
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
