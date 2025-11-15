1. Distributed Multi-Service Architecture

This project implements a distributed microservice architecture consisting of four independent services—API Gateway, Authentication Service, Data Service, and Cache Service—each running in separate Docker containers and deployed across multiple Ubuntu VMs.

2. Inter-Service Communication Over Network

All services communicate over REST APIs using well-defined interfaces. Inter-VM networking is configured so each service interacts through static IP addresses, enabling real distributed system behavior.

3. Automated Deployment Using SSH & Docker

Deployment is fully automated with SSH-based scripts that remotely build, transfer, and run Docker containers on each VM. This ensures fast, repeatable, and consistent deployments across different environments.

4. Health Checks, Logging, and Fault Tolerance

Each service exposes a /health endpoint to support automated validation. The system is designed to continue functioning even if one service fails, ensuring resilience and fault-tolerance.

5. Network Traffic Capture & Analysis

Wireshark and tcpdump are used to capture inter-service network traffic between VMs. PCAP files are analyzed to validate correct request flow, latency, and communication patterns across the distributed system.
