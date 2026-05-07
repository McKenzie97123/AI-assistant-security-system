# Instrukcja uruchomienia — Ubuntu 22.04

## Wymagania sprzętowe

- 4 CPU, 4 GB RAM, 20 GB dysk
- Na słabszej maszynie: `--memory=2048` w kroku 2 (wolniejsze budowanie)

---

## 1. Instalacja narzędzi

### Docker
```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" \
  | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker $USER
newgrp docker
```

### kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### minikube
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

---

## 2. Uruchomienie klastra

```bash
minikube start --driver=docker --cpus=4 --memory=4096
```

---

## 3. Budowanie obrazów Docker

Obrazy buduj **wewnątrz** minikube — bez tego Kubernetes ich nie znajdzie.

```bash
cd ~/AIsys

eval $(minikube docker-env)

docker build -t aisys/webapp:latest     src/webapp
docker build -t aisys/protection:latest src/protection
docker build -t aisys/bots:latest       src/bots
```

---

## 4. Klucz API dla strategii `llm` (opcjonalne)

Wymagane tylko przy testowaniu strategii `llm` (Claude Haiku). Pomiń jeśli zaczynasz od `ml`.

```bash
kubectl create secret generic anthropic-secret \
  --from-literal=api-key=sk-ant-TWOJ_KLUCZ \
  -n aisys-protection
```

---

## 5. Wdrożenie

```bash
./scripts/deploy.sh
```

Skrypt czeka automatycznie aż wszystkie pody będą gotowe.

---

## 6. Dostęp do interfejsów

```bash
# Grafana — dashboardy z metrykami
minikube service grafana-svc -n aisys-monitoring

# Prometheus — surowe metryki
minikube service prometheus-svc -n aisys-monitoring

# AI Proxy — punkt wejścia dla botów i ręcznych żądań
minikube service ai-protection-svc -n aisys-protection
```

Grafana: login `admin` / hasło `admin123`

---

## 7. Przeprowadzanie eksperymentów

```bash
# Składnia: ./scripts/experiment.sh <strategia> <liczba_podow_botow>

./scripts/experiment.sh rate_limit 3
./scripts/experiment.sh rules      3
./scripts/experiment.sh ml         3
./scripts/experiment.sh llm        3

# Test skalowalności ataku (strategia ml, rosnąca liczba botów)
./scripts/experiment.sh ml 1
./scripts/experiment.sh ml 5
./scripts/experiment.sh ml 10
```

Zmiany widoczne na żywo w Grafanie — dashboard odświeża się co 10 sekund.

---

## 8. Podgląd stanu klastra

```bash
# Wszystkie pody
kubectl get pods -A

# Logi proxy (decyzje blokowania)
kubectl logs -f deployment/ai-protection -n aisys-protection

# Logi botów
kubectl logs -f deployment/spam-bots -n aisys-bots
```

---

## 9. Zatrzymanie

```bash
minikube stop     # zatrzymuje klaster, zachowuje dane
minikube delete   # usuwa klaster całkowicie
```
