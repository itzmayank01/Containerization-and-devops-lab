# Kubernetes Deployments

This section demonstrates how to create and manage Kubernetes Deployments using YAML.

---

##  YAML Files

- [web.yaml](web.yaml)
- [we.yaml](we.yaml)

---

## Hands-on Practice

![img](./Hands%20on%20practice.png)
![img](./Hands%20on%20practice%201.png)
![img](./Hands%20on%20practice%202.png)
![img](./Hands%20on%20practice%203.png)
![img](./Hands%20on%20practice%204.png)

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
