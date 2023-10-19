pipeline {
    agent none
    stages {
	stage('Docker Frontend') {
	    steps {
		docker { image 'node:16-alpine' }
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
