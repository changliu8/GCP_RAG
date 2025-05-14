pipeline {
    agent { label 'gcp-node' }

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = "$serious-hall-459619-j3-fec998871be2.json"
    }
    
    stages {
        stage("Check and Install Ollama"){
            steps{
                script{
                    def ollamaInstalled = sh(
                        script: 'command -v ollama >/dev/null 2>&1 && echo yes || echo no',
                        returnStdout:true
                    ).trim()
                }

                if(ollamaInstalled == 'yes'){
                    echo "✅ Ollama is already installed. Skipping installtion."
                }
                else{
                    echo "📦 Ollama not found. Installing..."
                    sh '''
                        curl -fsSL https://ollama.com/install.sh | sh
                        echo '✅ Ollama installed successfully.'
                    '''
                }
            }
        }

        stage('Checkout') {
            steps {
                git url: 'https://github.com/changliu8/GCP_RAG.git', branch: 'main'
            }
        }
        
        stage('Creating Virtual Environment'){
            steps{
                sh "python -m venv RAG"
                sh "${workspace}/RAG/Scripts/activate"
            }
        }
        
        stage('Install dependencies') {
            steps {
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Setup GCP Credential') {
            steps {
                withCredentials([file(credentialsId: 'gcp-storage', variable: 'GCP_KEY')]) {
                    sh 'cp %GCP_KEY% %GOOGLE_APPLICATION_CREDENTIALS%'
                }
            }
        }
        
        stage('Download files') {
            steps {
                sh 'python download_faiss.py'
            }
        }
        
        stage("Generating answers"){
            steps{
                sh 'python gcp_rag.py "${params.Question}"'
            }
        }
    }
}