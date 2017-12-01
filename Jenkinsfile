node{
  stage('Get Build Number'){
    def buildNumberInput = input(
        id: 'buildNumber', message: 'What build number to deploy: ', ok: 'select', parameters: [$class: 'StringParameterDefinition', description: 'Build number', name: 'buildNumber']
    )
    echo ("Password was: " + buildNumberInput)
  }
}
