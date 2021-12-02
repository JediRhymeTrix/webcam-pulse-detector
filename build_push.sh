docker build -t inference .
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 720650668093.dkr.ecr.us-east-2.amazonaws.com
docker tag inference:latest 720650668093.dkr.ecr.us-east-2.amazonaws.com/inference:latest
docker push 720650668093.dkr.ecr.us-east-2.amazonaws.com/inference:latest