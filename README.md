## This is only for my personal note

1. Create a GCP VM:

2. Install java 17 on the node
   apt install openjdk-17-jdk openjdk-17-jre

3. Create Public/Private Key Pair for Jenkins launch agent
   ssh-keygen -t rsa -b 4096

4. Copy public key to authorized_keys under ~/.ssh

5. Add username and private key to Jenkins as Credential

6. Luanch Agent

7. Execute the Jenkins Job, it takes your question as input!

Example :

GCP_RAG_pipeline.png
