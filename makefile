
env:
	. .env && for f in k8s/*.yml; do \
	  envsubst < "$$f" | kubectl apply -f -; \
	done