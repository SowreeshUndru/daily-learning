# Kubernetes Day 4 - Services (LoadBalancer & ClusterIP)

## LoadBalancer Service

A **LoadBalancer Service** is used to expose an application to the outside world. It is important to understand that a LoadBalancer is **not a component of Kubernetes itself**. Instead, it is a resource provided by the **cloud provider** (such as AWS, Azure, or GCP).

Even if we create a `service.yaml` file with:

```yaml
spec:
  type: LoadBalancer
```

Kubernetes **does not create the load balancer by itself**. Instead, Kubernetes sends a request to the cloud provider, and the cloud provider provisions an external load balancer.

For example:

* AWS → Elastic Load Balancer (ELB)
* Google Cloud → Cloud Load Balancer
* Microsoft Azure → Azure Load Balancer

The external load balancer then forwards incoming traffic to the Kubernetes Service, which in turn routes the traffic to the appropriate Pods.

### Important Points

* A LoadBalancer Service depends on the cloud provider.
* The cloud provider creates and manages the actual load balancer.
* The load balancer is a **separate cloud resource**.
* Cloud providers charge separately for the load balancer.

### Cost Note

One common misconception is that deleting a Kubernetes cluster will always delete the cloud load balancer as well.

In practice, you should always verify that the load balancer has been removed. If an external load balancer is left behind (for example, because cleanup failed or resources were deleted incorrectly), the cloud provider may continue charging for it.

**Always check your cloud console after deleting Services or clusters to ensure no unused load balancers remain.**

---

## ClusterIP Service

Until now, we discussed how **external users** can access applications running inside Kubernetes using NodePort or LoadBalancer Services.

However, many applications consist of multiple services that need to communicate **within the cluster**. For example:

* Frontend → Backend
* Backend → Database
* Backend → Redis
* Backend → Machine Learning Server

In these scenarios, exposing services to the Internet is unnecessary. Instead, Kubernetes provides the **ClusterIP Service**, which is the default Service type.

A ClusterIP Service creates a **stable internal IP address** that is accessible only from within the Kubernetes cluster. Other Pods can use this stable IP (or the Service's DNS name) to communicate with the application.

Since Pod IP addresses can change whenever Pods are recreated, applications should communicate through the Service rather than directly using Pod IPs.

### Common Use Cases

* Internal communication between microservices.
* Database services.
* Redis or cache servers.
* Internal APIs.
* Machine Learning inference servers.
* Any application that should only be accessible inside the cluster.

Although **ClusterIP** is the default and most common Service type for internal communication, users typically interact with applications through **LoadBalancer** Services in cloud environments or **NodePort** Services for testing and learning.

---

## Service YAML Overview

```yaml
apiVersion: v1
kind: Service

metadata:
  name: my-service

spec:
  selector:
    app: my-app

  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080

  type: LoadBalancer
```

### Explanation

* **apiVersion** – Specifies the Kubernetes API version.
* **kind** – Specifies the Kubernetes object type (`Service`).
* **metadata** – Contains information such as the Service name.
* **spec** – Defines the Service configuration.
* **selector** – Selects the Pods (using labels) that will receive traffic.
* **ports** – Defines how traffic is forwarded.

  * **port** – Port exposed by the Service.
  * **targetPort** – Port on which the container is listening.
  * **protocol** – Network protocol (TCP by default).
* **type** – Specifies how the Service is exposed (`ClusterIP`, `NodePort`, or `LoadBalancer`).
