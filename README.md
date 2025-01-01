# SoundExtract

This project demonstrates the development, deployment, and orchestration of a microservices-based architecture using modern technologies such as Kubernetes, Docker, RabbitMQ, and MongoDB with GridFS. The repository contains code and configurations for multiple services, including authentication, gateway, notification, and a converter service, showcasing both synchronous and asynchronous interservice communication.

---

## ⭐️ Contents

- **Overview**
- **Installation & Setup**
- **Services**
  - Auth Service
  - Gateway Service
  - Converter Service
  - Notification Service
- **Technologies Used**
- **Consistency Models**
  - Strong Consistency
  - Eventual Consistency
- **Deployment**
- **Kubernetes Configurations**
- **Architecture Overview**
- **References**

---

## Overview
This project provides a complete end-to-end microservices implementation, covering:
- Service design and interservice communication
- Deployment strategies with Docker and Kubernetes
- Scalable and fault-tolerant architectures using Kubernetes StatefulSets and Ingress
- Integration of messaging queues with RabbitMQ
- Persistent data storage using MongoDB with GridFS

---

## Installation & Setup

### Prerequisites
- Docker
- Kubernetes cluster (e.g., Minikube, k3s, or cloud-managed Kubernetes like GKE, AKS, or EKS)
- kubectl CLI
- RabbitMQ
- MongoDB

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/selikapro/microservices.git
   cd microservices
   ```

2. Build Docker images for all services:
   ```bash
   docker build -t auth-service ./auth
   docker build -t gateway-service ./gateway
   docker build -t converter-service ./converter
   docker build -t notification-service ./notification
   ```

3. Deploy services to Kubernetes:
   ```bash
   kubectl apply -f k8s/
   ```

4. Verify deployments:
   ```bash
   kubectl get pods
   ```

5. Configure RabbitMQ and MongoDB as needed:
   - Use `kubectl apply -f k8s/rabbitmq.yml` to deploy RabbitMQ.
   - Use `kubectl apply -f k8s/mongo.yml` to deploy MongoDB.

---

## Services

### Auth Service
- Implements user authentication and JWT-based authorization.
- Exposes REST endpoints for user login and registration.
- Configured with a Dockerfile and deployed via Kubernetes.

### Gateway Service
- Acts as a central entry point to the microservices architecture.
- Manages routing and load balancing of requests.
- Integrated with Kubernetes Ingress for external access.

### Converter Service
- Handles specific data processing tasks.
- Interacts with other services synchronously and asynchronously.
- Uses RabbitMQ for messaging.

### Notification Service
- Sends notifications via email or other channels.
- Consumes events published to RabbitMQ queues.

---

## Technologies Used
- **Docker**: Containerization of microservices.
- **Kubernetes**: Deployment, scaling, and management of services.
- **RabbitMQ**: Message broker for asynchronous communication.
- **MongoDB with GridFS**: Database for storing and managing large files.
- **Kubernetes StatefulSets**: Managing stateful applications.
- **Kubernetes Ingress**: Exposing services to the outside world.

---

## Consistency Models

### Strong Consistency
- Ensures data consistency across services during synchronous interservice communication.

### Eventual Consistency
- Guarantees eventual synchronization of data across services using RabbitMQ and asynchronous events.

---

## Deployment

### Steps
1. Build Docker images and push them to a container registry (e.g., Docker Hub, AWS ECR, or GCP Container Registry).
   ```bash
   docker push your-registry/auth-service
   docker push your-registry/gateway-service
   docker push your-registry/converter-service
   docker push your-registry/notification-service
   ```

2. Deploy each service using the provided Kubernetes YAML files.

3. Monitor logs to ensure services are running:
   ```bash
   kubectl logs -f <pod-name>
   ```

---

## Architecture Overview

- **RabbitMQ**:
  - Central message broker for asynchronous interservice communication.

- **MongoDB & GridFS**:
  - Handles persistent data and large file storage.

- **Synchronous Communication**:
  - Direct HTTP/REST calls between services.

- **Asynchronous Communication**:
  - Event-driven architecture using RabbitMQ.

---

## References
- [Kubernetes API Reference](https://kubernetes.io/docs/reference/)
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [MongoDB GridFS](https://www.mongodb.com/docs/manual/core/gridfs/)

---

