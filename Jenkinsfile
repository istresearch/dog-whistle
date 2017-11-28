docker.image('python:2.7').inside {
  stage('Install package'){
      sh 'hostname'
      sh 'python setup.py sdist'
      sh 'pip install dist/dog-whistle-*.tar.gz'
  }
  stage('Test') {
      sh 'hostname'
      sh 'bash run_tests.sh'
      stash includes: 'dist/dog-whistle-*.tar.gz', name: 'built'
  }
}



milestone()


def userInput = true
def didTimeout = false
try {
    timeout(time: 15, unit: 'SECONDS') { 
        userInput = input(
        message: 'Would you like to deploy?', parameters: [
        [$class: 'BooleanParameterDefinition', defaultValue: true, description: '', name: 'Would you like to deploy?']
        ])
    }
} catch(err) { // timeout reached or input false
    def user = err.getCauses()[0].getUser()
    if('SYSTEM' == user.toString()) { // SYSTEM means timeout.
        didTimeout = true
    } else {
        userInput = false
        echo "Aborted by: [${user}]"
    }
}

node {
    // Mark build as successful if timed out. This implies it was a normal build that will not get
    // promoted.
    if (didTimeout) {
        currentBuild.result = 'SUCCESS'
        return
    } 
}

node {
  stage('Deploy') {
      sh 'hostname'
      unstash 'built'
      sh 'mv dist/*.tar.gz .'
      sh 'rm -rf dist *.egg-info'
      sh 'mkdir -p /data/blueocean/repo/pip/prod'
      sh 'cp *.tar.gz /data/blueocean/repo/pip/prod'
  }
}
