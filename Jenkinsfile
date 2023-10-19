pipeline {
    agent none
    stages {
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
