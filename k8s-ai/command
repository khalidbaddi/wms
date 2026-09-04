python3 --version
python --version
apt update
apt install python3 -y
python3 --version
python3
exit()
apt install python3-pip -y
pip3 --version

python3 -m venv venv
source venv/bin/activate

pip install langchain faiss-cpu sentence-transformers fastapi uvicorn transformers torch
uvicorn app:app --host 0.0.0.0 --port 8000

docker build -t k8s-ai:v1 .
docker run -p 8000:8000 k8s-ai:v1

mkdir k8sdeploy
cd k8sdeploy
touch deployment.yaml
touch service.yaml

kubectl get svc
http://NODE-IP:NODEPORT
uvicorn app:app --host 0.0.0.0 --port 8000
http://172.30.1.12:8000
curl http://localhost:8000
uvicorn app:app --host 0.0.0.0 --port 8000 --reload





