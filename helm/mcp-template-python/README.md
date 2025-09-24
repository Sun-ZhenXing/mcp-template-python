# MCP Template Python - Helm Chart Configuration Guide

## Quick Start

### 1. Basic Deployment

```bash
# Validate configuration
make helm-lint

# Development environment deployment
make helm-install

# Update deployment
make helm-upgrade

# Uninstall
make helm-uninstall
```

### 2. Production Environment Deployment

```bash
# Initial deployment
make helm-install-prod

# Update deployment
make helm-upgrade-prod
```

## Core Configuration

### Image Configuration

```yaml
image:
  repository: docker.io/mcp-template-python
  tag: "latest"
  pullPolicy: IfNotPresent
```

### Service Configuration

```yaml
service:
  type: ClusterIP
  port: 3001
  targetPort: 3001
```

### Environment Variables

```yaml
env:
  MCP_DEFAULT_HOST: "0.0.0.0"
  MCP_DEFAULT_PORT: "3001"
```

### Health Checks

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 30

readinessProbe:
  httpGet:
    path: /health
    port: http
  initialDelaySeconds: 5
```

## Production Environment Configuration

### 1. Resource Configuration (Required)

```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

### 2. Image Registry

```yaml
image:
  repository: your-registry.com/mcp-template-python
  tag: "v1.0.0"
```

### 3. Auto Scaling

```yaml
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### 4. Ingress Configuration

```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: mcp-template-python.your-domain.com
      paths:
        - path: /
          pathType: ImplementationSpecific
```

## Configuration File Management

### ConfigMap Configuration

```yaml
configMap:
  enabled: true
  data:
    app.conf: |
      # Application configuration
      log_level=info
      debug=false
```

### Mounting Configuration Files

Add to `values.yaml`:

```yaml
volumeMounts:
  - name: config
    mountPath: /app/config
    readOnly: true

volumes:
  - name: config
    configMap:
      name: mcp-template-python-config
```

## Security Configuration

Application runs as non-root user:

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
    - ALL
```

## Pre-Deployment Checklist

### Development Environment

- [ ] Update image repository in `values.yaml`
- [ ] Confirm port configuration
- [ ] Set environment variables

### Production Environment

- [ ] Update image tag in `values-production.yaml`
- [ ] Set resource limits and requests
- [ ] Configure domain name and TLS
- [ ] Confirm replica count
- [ ] Check health check paths

## Common Commands

```bash
# Check deployment status
kubectl get pods -l app.kubernetes.io/name=mcp-template-python

# Check service
kubectl get svc mcp-template-python

# View logs
kubectl logs -l app.kubernetes.io/name=mcp-template-python

# Enter container
kubectl exec -it deployment/mcp-template-python -- /bin/bash

# View configuration
helm get values mcp-template-python
```

## Troubleshooting

### Common Issues

1. **Pod Startup Failure**
   - Check if image exists
   - Confirm resource configuration is reasonable
   - View Pod events: `kubectl describe pod <pod-name>`

2. **Health Check Failure**
   - Confirm application provides `/health` endpoint
   - Check port configuration is correct
   - Adjust probe delay times

3. **Service Inaccessible**
   - Confirm Service configuration
   - Check network policies
   - Verify Ingress configuration

### Getting Help

```bash
# View Chart information
helm show chart helm/mcp-template-python

# View all configuration options
helm show values helm/mcp-template-python

# Validate template rendering
helm template mcp-template-python helm/mcp-template-python
```

---

**Note**: Before production deployment, make sure to update the resource configuration and domain settings in `values-production.yaml`.
