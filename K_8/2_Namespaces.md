# Kubernetes Namespaces

## What are Namespaces?

As you already know, in Docker every container gets its own namespaces (PID, Network, Mount, etc.), which isolate it from the host system and other containers.

Kubernetes uses the concept of **Namespaces** for a different purpose.

A Kubernetes **Namespace** is a logical partition inside a cluster that separates Kubernetes resources such as Pods, Deployments, ReplicaSets, Services, ConfigMaps, etc.

The main purpose of namespaces is to **organize and isolate resources** inside a cluster.

---

## Why do we need Namespaces?

Suppose we have a Kubernetes cluster used by a startup.

- The cluster contains around **1000 Pods**.
- There are multiple teams:
  - Backend Team
  - Frontend Team
  - Database Team
- All these teams work together in the same cluster to achieve high availability and 100% uptime.

Now imagine a backend developer runs:

```bash
kubectl get pods
```

If everything were in the same namespace, Kubernetes would return **all 1000 Pods**, including frontend, backend, and database Pods.

Finding only the backend Pods would become difficult.

To solve this problem, Kubernetes provides **Namespaces**.

Each team can have its own namespace.

Example:

- backend namespace
- frontend namespace
- database namespace

This logically separates the resources while still using the same Kubernetes cluster.

---

## Default Namespace

When we create a cluster, Kubernetes already creates several namespaces.

Some important ones are:

| Namespace | Purpose |
|-----------|----------|
| default | Used for our applications if no namespace is specified. |
| kube-system | Contains Kubernetes system Pods like CoreDNS, kube-proxy, etc. |
| kube-public | Public resources accessible by all users. |
| kube-node-lease | Stores node heartbeat information. |

When we execute:

```bash
kubectl get pods
```

Kubernetes checks only the **default namespace**.

It does **not** show Pods running in other namespaces like `kube-system`.

This is why we don't see Kubernetes internal Pods by default.

---

## Viewing Pods from another Namespace

To see Pods from a specific namespace, explicitly mention the namespace name.

Example:

```bash
kubectl get pods -n backend
```

or

```bash
kubectl get pods --namespace=backend
```

To view Pods inside Kubernetes system namespace:

```bash
kubectl get pods -n kube-system
```

---

## Viewing all Namespaces

```bash
kubectl get namespaces
```

or

```bash
kubectl get ns
```

Example output:

```text
NAME              STATUS
default           Active
kube-system       Active
kube-public       Active
kube-node-lease   Active
backend           Active
frontend          Active
database          Active
```

---

## Creating a Namespace

### Using command

```bash
kubectl create namespace backend
```

or

```bash
kubectl create ns backend
```

---

## Namespace Manifest (manifest.yaml)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: backend
```

Create it using:

```bash
kubectl apply -f manifest.yaml
```

Verify:

```bash
kubectl get namespaces
```

---

## Creating Resources inside a Namespace

Example Deployment:

```bash
kubectl apply -f deployment.yaml -n backend
```

or mention the namespace directly inside the YAML.

Example:

```yaml
metadata:
  name: nginx-deployment
  namespace: backend
```

---

## Listing Pods from all Namespaces

Sometimes we want to see every Pod in the cluster.

Use:

```bash
kubectl get pods --all-namespaces
```

or

```bash
kubectl get pods -A
```

This displays Pods from every namespace.

---

## Changing the Current Namespace

Instead of writing `-n backend` every time, we can change the current namespace.

```bash
kubectl config set-context --current --namespace=backend
```

Now,

```bash
kubectl get pods
```

automatically shows Pods from the **backend** namespace.

To switch back:

```bash
kubectl config set-context --current --namespace=default
```

This is similar to switching Git branches.

Just like Git changes the current branch, Kubernetes changes the current namespace.

---

## Checking the Current Namespace

```bash
kubectl config view --minify | grep namespace
```

If nothing is shown, Kubernetes is using the **default** namespace.

---

## Deleting a Namespace

```bash
kubectl delete namespace backend
```

or

```bash
kubectl delete ns backend
```

Deleting a namespace deletes **all resources** inside that namespace.

---

# Important Clarification (Your Doubt)

One doubt was whether namespaces are added using **labels**.

**Answer: No.**

Namespaces and Labels are completely different concepts.

### Namespace

- Divides Kubernetes resources logically.
- Used for isolation between teams/projects.
- Every resource belongs to exactly one namespace (except cluster-wide resources).

### Labels

- Key-value pairs attached to resources.
- Used for selecting and grouping resources.
- Services, ReplicaSets, and Deployments use labels to identify Pods.

Example label:

```yaml
metadata:
  labels:
    app: backend
    env: production
```

Example namespace:

```yaml
metadata:
  namespace: backend
```

So, namespaces are **not created using labels**.

---

# Summary

- Kubernetes namespaces logically divide resources inside a cluster.
- They help separate teams such as backend, frontend, and database.
- `kubectl get pods` shows Pods only from the current namespace (default if not changed).
- Kubernetes system Pods run in namespaces like `kube-system`, so they are not shown by default.
- Use `-n <namespace>` to access resources in another namespace.
- Use `kubectl config set-context --current --namespace=<name>` to change the current namespace.
- Namespaces and Labels are different concepts; namespaces provide isolation, while labels are used for grouping and selecting resources.



# Why do we need Namespaces if we already have Labels? (My Doubt)

This was one of my biggest doubts while learning Kubernetes.

I thought:

> We already have labels like `app=backend`, `app=frontend`, etc. We can already filter Pods using:
>
> ```bash
> kubectl get pods -l app=backend
> ```
>
> Then why did Kubernetes introduce another concept called **Namespaces**? Aren't we adding an unnecessary layer?

At first, it feels like both are solving the same problem, but they are actually solving **different problems**.

---

## Labels are for Selection

Labels are simply **key-value pairs** attached to Kubernetes resources.

Example:

```yaml
labels:
  app: backend
```

Using labels, we can filter resources.

Example:

```bash
kubectl get pods -l app=backend
```

ReplicaSets and Services also use labels to identify which Pods they should manage.

Example:

```yaml
selector:
  matchLabels:
    app: backend
```

So labels answer the question:

> **"Which resources should I select?"**

They are **not** responsible for isolation or security.

---

## Namespaces are for Isolation

Namespaces are **not created just to filter Pods**.

Their primary purpose is to **isolate resources** inside the same Kubernetes cluster.

Suppose a company has:

- Backend Team
- Frontend Team
- Database Team

All three teams are working inside the same cluster.

Even if every Pod has labels like:

```text
app=backend
app=frontend
app=database
```

everything still belongs to the **same namespace** unless we explicitly create different namespaces.

Namespaces create logical boundaries between teams and their resources.

---

## Why not just use Labels?

Yes, technically we can filter backend Pods using:

```bash
kubectl get pods -l app=backend
```

This gives the same list of backend Pods.

But **this is only filtering**, not isolation.

Namespaces provide several additional features that labels cannot.

### 1. Isolation

If one developer accidentally deletes or modifies a resource, the impact is limited to that namespace.

Resources belonging to other namespaces remain unaffected.

---

### 2. Resource Names

Inside one namespace, resource names must be unique.

For example, you cannot have two Deployments named:

```text
api
api
```

inside the same namespace.

However, this is perfectly valid:

```text
backend namespace
└── Deployment: api

frontend namespace
└── Deployment: api
```

Both Deployments can have the same name because they belong to different namespaces.

Labels cannot provide this separation.

---

### 3. Security (RBAC)

Permissions in Kubernetes are commonly assigned per namespace.

For example:

- Backend developers can access only the `backend` namespace.
- Frontend developers can access only the `frontend` namespace.

If everything is in one namespace and only labels are used, users can still view all resources unless additional restrictions are configured.

---

### 4. Resource Quotas

Namespaces allow administrators to set limits such as:

- Maximum CPU
- Maximum Memory
- Maximum number of Pods

Example:

```text
backend namespace
CPU: 10 cores
Memory: 20 GB
```

Labels cannot enforce these limits.

---

### 5. Better Organization

Namespaces divide a large cluster into smaller logical environments.

Instead of managing one namespace containing thousands of resources, each team manages only its own namespace.

---

## So what is the actual difference?

The following two commands may look similar:

```bash
kubectl get pods -l app=backend
```

and

```bash
kubectl get pods -n backend
```

However, they are **not doing the same thing**.

The first command:

- Searches all resources in the current namespace.
- Filters them based on the label `app=backend`.

The second command:

- Looks only inside the `backend` namespace.
- It does not care about labels.

Namespaces define **where resources live**.

Labels define **which resources to select**.

---

## Final Conclusion

My initial doubt was:

> "If labels can already group backend Pods, why do we need namespaces?"

The answer is:

**Labels are for grouping and selecting resources.**

**Namespaces are for isolating resources.**

Filtering Pods is only a small part of Kubernetes.

Namespaces additionally provide:

- Isolation between teams
- Security (RBAC)
- Resource quotas
- Avoiding naming conflicts
- Better organization of large clusters

So, Kubernetes did **not** create namespaces to replace labels.

Instead, labels and namespaces complement each other.

- **Labels → "Which resources?"**
- **Namespaces → "Which isolated environment?"**



# Kubernetes Example: Deploying a Backend Express Server

Suppose I have already built my Express.js application, created a Docker image, and pushed it to Docker Hub.

Example Docker image:

```text
sowreesh/backend-express:latest
```

Now I want to deploy it in Kubernetes.

In Kubernetes, these resources are separate:

- Namespace
- Deployment
- Service

A **Deployment automatically creates and manages ReplicaSets**, and the **ReplicaSet automatically creates and manages Pods**.

The **Service is a separate resource** used to expose the Pods.

The workflow is:

```text
Namespace
      │
      ▼
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pods
      ▲
      │
 Service
```

---

# Step 1: Create Namespace

**namespace.yaml**

```yaml
apiVersion: v1
kind: Namespace

metadata:
  name: backend
```

Create it:

```bash
kubectl apply -f namespace.yaml
```

Verify:

```bash
kubectl get namespaces
```

---

# Step 2: Create Deployment

**deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: backend-deployment
  namespace: backend

spec:
  replicas: 3

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:
      containers:
      - name: backend-container
        image: sowreesh/backend-express:latest

        ports:
        - containerPort: 3000
```

Apply it:

```bash
kubectl apply -f deployment.yaml
```

Verify:

```bash
kubectl get deployments -n backend
```

---

# What happens internally?

After creating the Deployment, Kubernetes automatically creates:

```text
Deployment
      │
      ▼
ReplicaSet
      │
      ▼
Pod 1

Pod 2

Pod 3
```

You never create the ReplicaSet manually in normal applications.

The Deployment manages the ReplicaSet.

The ReplicaSet manages the Pods.

Verify ReplicaSets:

```bash
kubectl get replicasets -n backend
```

Verify Pods:

```bash
kubectl get pods -n backend
```

---

# Step 3: Create Service

The Pods have dynamic IP addresses.

Whenever a Pod is recreated, its IP changes.

Applications should not communicate directly with Pod IPs.

Instead, Kubernetes provides a **Service**, which gives a stable IP and DNS name.

**service.yaml**

```yaml
apiVersion: v1
kind: Service

metadata:
  name: backend-service
  namespace: backend

spec:
  selector:
    app: backend

  ports:
  - port: 80
    targetPort: 3000

  type: ClusterIP
```

Create it:

```bash
kubectl apply -f service.yaml
```

Verify:

```bash
kubectl get services -n backend
```

---

# How Service finds Pods

Notice the selector:

```yaml
selector:
  app: backend
```

The Deployment created Pods using:

```yaml
template:
  metadata:
    labels:
      app: backend
```

Every Pod has:

```text
app=backend
```

The Service simply searches for Pods having:

```text
app=backend
```

and forwards traffic to them.

---

# Complete Flow

```text
namespace.yaml
      │
      ▼
Creates Namespace

backend
      │
      ▼
deployment.yaml
      │
      ▼
Creates Deployment
      │
      ▼
Deployment creates ReplicaSet
      │
      ▼
ReplicaSet creates 3 Pods
      │
      ▼
Pods

app=backend
```

Now,

```text
service.yaml
      │
      ▼
Creates Service
      │
      ▼
Selector

app=backend
      │
      ▼
Finds all backend Pods
      │
      ▼
Routes traffic to them
```

---

# Resource Relationship

```text
Namespace
│
├── Deployment
│      │
│      ▼
│   ReplicaSet
│      │
│      ▼
│    Pod 1
│    Pod 2
│    Pod 3
│
└── Service
       │
       ▼
Selects Pods using:

app=backend
```

---

# Commands to Verify Everything

View namespaces:

```bash
kubectl get namespaces
```

View deployments:

```bash
kubectl get deployments -n backend
```

View ReplicaSets:

```bash
kubectl get replicasets -n backend
```

View Pods:

```bash
kubectl get pods -n backend
```

View Services:

```bash
kubectl get services -n backend
```

View all resources:

```bash
kubectl get all -n backend
```

---

# Important Points

- **Namespace** is created separately.
- **Deployment** is created separately.
- **Deployment automatically creates and manages a ReplicaSet.**
- **ReplicaSet automatically creates and manages Pods.**
- **Service is a separate resource.**
- **Service never creates Pods.**
- **Service finds Pods using labels (`selector`).**
- **Pods are created using the Deployment's `template`.**
- In real-world Kubernetes projects, these resources are usually kept in separate YAML files:
  - `namespace.yaml`
  - `deployment.yaml`
  - `service.yaml`
```