# Kubernetes ClusterIP

Now, let's talk about **ClusterIP**.

As you already know, **ClusterIP** is used for internal communication between applications running inside the Kubernetes cluster.

But before talking about ClusterIP, let's first understand **why Services are created**.

Normally, a Pod can communicate with another Pod even without a Service.

You might have a doubt:

> **How can one Pod communicate with another Pod without routers or anything like that?**

You may also think that **kube-proxy** is responsible for routing all Pod-to-Pod traffic. But that is **not** the case.

When one Pod communicates directly with another Pod using the Pod's IP address, the communication is handled by the **CNI (Container Network Interface) plugin**, such as **Flannel**, **Calico**, or **Cilium**.

These plugins configure the Linux networking so that Pods can reach each other across the cluster.

## Example

Suppose there are two Pods:

* A **Node.js Backend Pod**
* A **MongoDB Pod**

Now, the Backend Pod wants to communicate with the MongoDB Pod.

If we assume that:

* The MongoDB Pod is reliable.
* It never gets deleted.
* Its IP address never changes.

Then, if the Backend Pod knows the MongoDB Pod's IP address, it can connect directly using:

```text
mongodb://<MongoDB-Pod-IP>:27017/mydb
```

For example:

```text
mongodb://10.244.2.8:27017/mydb
```

In this case, the Backend Pod communicates directly with the MongoDB Pod **without using any Service**.

## Why is this not used in real applications?

This approach is rarely used in real applications because **Pods are temporary**.

Pods can be:

* Deleted
* Restarted
* Recreated

Whenever a new Pod is created, it usually gets a **new IP address**.

If the Backend application is still using the old Pod IP address, the connection will fail.

This is the main reason why Kubernetes provides **Services**. They give applications a stable way to communicate even when Pods are created, deleted, or restarted.




## Why Do We Need a Service?

As we discussed earlier, directly connecting to a Pod IP is not feasible because Pods are temporary. They can be deleted and recreated at any time, and whenever a new Pod is created, it usually gets a new IP address.

Now, suppose a Backend wants to communicate with MongoDB.

There may be multiple MongoDB Pods running. Some Pods may be deleted, some new Pods may be created, and their IP addresses may keep changing.

To solve this problem, we create a **Service** for MongoDB.

This Service keeps track of all the MongoDB Pods. It knows:

* Which Pods are currently running.
* Which Pod IP addresses are valid.
* Which Pods are no longer available.

Whenever Pods are created or deleted, the Service automatically updates the list of available Pods.

## How Communication Happens

When the Backend wants to communicate with MongoDB, it does **not** send the request directly to a MongoDB Pod.

Instead, it sends the request to the **MongoDB Service**.

The request flow looks like this:

```text id="q3d5dr"
Backend Pod
      │
      ▼
MongoDB Service
      │
      ▼
MongoDB Pod
```

The Service forwards the request to one of the healthy MongoDB Pods.

After the MongoDB Pod processes the request, the response comes back through the Service and finally reaches the Backend Pod.

Since there may be multiple MongoDB Pods, the Service also distributes requests among the healthy Pods. This makes the application more reliable.

## Does the Backend Need a Service?

In this scenario, the Backend is only **sending requests** to MongoDB.

Nobody inside the cluster needs a stable way to reach the Backend.

Therefore, the Backend **does not necessarily need a Service**.

## When Does the Backend Need a Service?

Now, suppose the situation changes.

Assume there are multiple Backend Pods, and now the MongoDB application (or some other application inside the cluster) needs to communicate with the Backend.

If there is **no Service** for the Backend, the MongoDB application does not have a stable address to reach it.

It does not know:

* Which Backend Pods are currently running.
* Which Pod IP addresses are valid.

To solve this problem, we create a **Backend Service**.

The Backend Service keeps track of all the Backend Pods, knows which Pods are healthy, and forwards requests to one of the available Backend Pods.

## Simple Rule to Remember

> **Whenever an application needs a stable way to receive requests from other applications, it should have a Service.**

## Backend vs MongoDB

In a normal application:

* The Backend **initiates** the request to MongoDB.
* MongoDB **only sends back the response**.
* MongoDB does **not** initiate requests to the Backend.

Therefore, in this specific scenario, **only the MongoDB application needs a Service**.

However, if the Backend also needs to receive requests from:

* Webhooks
* A Frontend
* An Ingress
* External users
* Other applications inside the cluster

then the Backend should also have its own Service.


## Backend Service vs MongoDB Service

In a normal application, the Backend always initiates the request to MongoDB, and MongoDB only sends back the response. MongoDB does **not** initiate requests to the Backend.

Therefore, in this scenario, MongoDB needs a **Service** so that the Backend has a stable way to reach it.

The Backend does **not necessarily need a Service** if no other application or user needs to communicate with it. If the Backend is only sending requests and nothing needs to reach it, then a Backend Service is not required.

However, in most real-world applications, users need to access the Backend through a browser, mobile app, or API client. In that case, the Backend also needs a Service.

If the Backend needs to receive requests from external users, we usually expose it using a **LoadBalancer Service** (or an **Ingress** with a Service behind it).

> **Important:** A **LoadBalancer Service** already contains a **ClusterIP** internally. The LoadBalancer is simply another way for external users to reach the Backend. Inside the cluster, the Service still uses its ClusterIP to forward requests to the Backend Pods.

### Typical Application Architecture

* **MongoDB** has a **ClusterIP Service** because it is only accessed from inside the cluster.
* **Backend** has a **LoadBalancer Service** (or **NodePort/Ingress**) because it needs to receive requests from external users.
* The **Backend** communicates with **MongoDB** using the **MongoDB ClusterIP Service**.

Therefore, the Backend does **not** need a separate **ClusterIP Service** in addition to the **LoadBalancer Service**, because the **LoadBalancer Service already includes a ClusterIP internally**.
Until now, we have understood how Services work. Now, let's see how the connection string looks in different scenarios.

### Case 1: No Service

Assume the Pods are reliable, they never get deleted, and their IP addresses never change.

Suppose there is a Backend Pod and a MongoDB Pod.

If there is **no Service**, then the backend connects directly to the MongoDB Pod using its Pod IP address.

The connection string looks like:

`mongodb://<MongoDB-Pod-IP>:27017/mydb`

For example:

`mongodb://10.244.2.8:27017/mydb`

Now, suppose the Backend Pod and the MongoDB Pod are in the **same namespace**.

The connection string is still:

`mongodb://10.244.2.8:27017/mydb`

Now, suppose they are in **different namespaces**.

The connection string is **still the same**:

`mongodb://10.244.2.8:27017/mydb`

This is because the backend is directly using the Pod IP address. It does not matter which namespace the Pod belongs to. The CNI plugin (such as Flannel, Calico, or Cilium) handles Pod-to-Pod networking across the cluster.

So, when using **Pod IP addresses**, the namespace does not change the connection string.

---

### Case 2: Using Services

Now, suppose we create a Service for MongoDB.

If the Backend and MongoDB are in the **same namespace**, the backend connects using the Service name.

The connection string looks like:

`mongodb://mongodb-service:27017/mydb`

Here, `mongodb-service` is the name of the MongoDB Service.

Kubernetes DNS automatically converts this Service name into the Service's ClusterIP.

---

Now, suppose the Backend and MongoDB are in **different namespaces**.

The backend must include the namespace in the Service name.

The connection string becomes:

`mongodb://mongodb-service.database:27017/mydb`

where:

* `mongodb-service` is the Service name.
* `database` is the namespace name.

You can also use the fully qualified DNS name:

`mongodb://mongodb-service.database.svc.cluster.local:27017/mydb`

However, in most applications, using:

`mongodb://mongodb-service.database:27017/mydb`

is sufficient.
