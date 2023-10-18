pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'building'
            }
        }
        stage('Test') {
            steps {
				echo 'testing'
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