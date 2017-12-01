node{
  stage('Get Build Number'){
    def buildNumberInput = input(
        id: 'BuildNumber', message: 'What build number to deploy: ', ok: 'select', parameters: [string(description: '.....', name: 'LIB_TEST')]
    )
    echo ("Password was: " + buildNumberInput)
  }
}
