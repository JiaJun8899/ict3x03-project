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
	            sh 'npm run dev'
                }
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
