node{
  stage('Get Build Number'){
    def buildNumberInput = input(
        id: 'buildNumber', message: 'dog-whistle build number: ', ok: 'ok', parameters: [description: '.....', name: 'buildNumber']
    )
    echo ("Password was: " + buildNumberInput)
  }
}
