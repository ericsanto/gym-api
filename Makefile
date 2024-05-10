APP = eric096/django-api-gym:1

setup-dev:
	@kind create cluster --name web --config /home/ericj/gym_api/kubernetes/configCluster.yaml
	@kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
	@sleep 40
	@kubectl wait --namespace ingress-nginx \
	--for=condition=ready pod \
	--selector=app.kubernetes.io/component=controller \
	--timeout=270s

delete-setup:
	@kind delete clusters web

deploy-dev:
	@docker build -t $(APP) .
	@docker push $(APP)
	@kubectl apply -f kubernetes/db
	@kubectl apply -f kubernetes/django
	@kubectl apply -f kubernetes/ingress.yaml
	#Deleta o pod antigo e cria um novo
	@kubectl rollout restart deploy django-deployment 

dev: setup-dev deploy-dev