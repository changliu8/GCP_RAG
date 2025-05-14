pipeline {
    agent { label 'gcp-node' }

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = "serious-hall-459619-j3-fec998871be2.json"
    }
    
    stages {
        stage("Check and Install Ollama"){
            steps{
                sh '''
                    if ! command -v ollama >/dev/null 2>&1; then
                        echo "Installing Ollama..."
                        curl -fsSL https://ollama.com/install.sh | sh
                    else
                        echo "Ollama is already installed."
                    fi
                '''
            }
        }

        stage('Pulling LLM'){
            steps {
                sh '''
                    if ollama list | grep -q llama3; then
                        echo "llama3 already pulled."
                    else
                        echo "Pulling llama3..."
                        ollama pull llama3
                    fi
                '''
            }
        }

        stage('Checkout') {
            steps {
                git url: 'https://github.com/changliu8/GCP_RAG.git', branch: 'main'
            }
        }
        
        stage('Creating Virtual Environment'){
            steps{
                sh "python3.8 -m venv RAG"
                sh ". ${workspace}/RAG/bin/activate"
            }
        }
        
        stage('Install dependencies') {
            steps {
                sh 'python3.8 -m pip install -r requirements.txt'
            }
        }

        stage('Setup GCP Credential') {
            steps {
                withCredentials([file(credentialsId: 'gcp-storage', variable: 'GCP_KEY')]) {
                    sh '''
                        export GOOGLE_APPLICATION_CREDENTIALS=$WORKSPACE/serious-hall-459619-j3-fec998871be2.json
                        cp "$GCP_KEY" "$GOOGLE_APPLICATION_CREDENTIALS"
                    '''
                }
            }
        }
        
        stage('Download files') {
            steps {
                sh 'python3.8 download_faiss.py'
            }
        }
        
        stage("Generating answers"){
            steps{
                sh 'python3.8 gcp_rag.py "${params.Question}"'
            }
        }
    }
}