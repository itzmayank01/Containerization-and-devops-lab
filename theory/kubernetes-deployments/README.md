# Kubernetes Deployments

This section demonstrates how to create and manage Kubernetes Deployments using YAML.

---

##  YAML Files

- [web.yaml](web.yaml)
- [we.yaml](we.yaml)

---

##  Hands-on Practice

![Practice 1](./Hands_on_practice.png)
![Practice 2](./Hands_on_practice_1.png)
![Practice 3](./Hands_on_practice_2.png)
![Practice 4](./Hands_on_practice_3.png)
![Practice 5](./Hands_on_practice_4.png)

---

##  What I Learned

- How Deployments manage Pods  
- Rolling updates & scaling  
- ReplicaSets behavior  
- Declarative configuration using YAML  

---

##  Commands Used

```bash
kubectl apply -f web.yaml
kubectl get deployments
kubectl describe deployment web
kubectl delete deployment web
