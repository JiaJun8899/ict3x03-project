pipeline {
    agent any
    tools {
        nodejs "NodeJS"
    }
    stages {
        stage('Build NextJS') {
            steps {
                dir('frontend') {
                    sh 'npm install'
                }
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