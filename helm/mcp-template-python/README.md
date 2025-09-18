# MCP Template Python - Helm Chart 配置说明

## 快速开始

### 1. 基础部署

```bash
# 验证配置
make helm-lint

# 开发环境部署
make helm-install

# 更新部署
make helm-upgrade

# 卸载
make helm-uninstall
```

### 2. 生产环境部署

```bash
# 首次部署
make helm-install-prod

# 更新部署
make helm-upgrade-prod
```

## 核心配置

### 镜像配置

```yaml
image:
  repository: docker.io/mcp-template-python
  tag: "latest"
  pullPolicy: IfNotPresent
```

### 服务配置

```yaml
service:
  type: ClusterIP
  port: 3001
  targetPort: 3001
```

### 环境变量

```yaml
env:
  MCP_DEFAULT_HOST: "0.0.0.0"
  MCP_DEFAULT_PORT: "3001"
```

### 健康检查

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

## 生产环境配置要点

### 1. 资源配置（必须设置）

```yaml
resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 250m
    memory: 256Mi
```

### 2. 镜像仓库

```yaml
image:
  repository: your-registry.com/mcp-template-python
  tag: "v1.0.0"
```

### 3. 自动扩展

```yaml
autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

### 4. Ingress 配置

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

## 配置文件管理

### ConfigMap 配置

```yaml
configMap:
  enabled: true
  data:
    app.conf: |
      # 应用配置
      log_level=info
      debug=false
```

### 挂载配置文件

在 `values.yaml` 中添加：

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

## 安全配置

应用运行在非 root 用户下：

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  capabilities:
    drop:
    - ALL
```

## 部署前检查清单

### 开发环境

- [ ] 修改 `values.yaml` 中的镜像仓库
- [ ] 确认端口配置
- [ ] 设置环境变量

### 生产环境

- [ ] 更新 `values-production.yaml` 中的镜像标签
- [ ] 设置资源限制和请求
- [ ] 配置域名和 TLS
- [ ] 确认副本数量
- [ ] 检查健康检查路径

## 常用命令

```bash
# 查看部署状态
kubectl get pods -l app.kubernetes.io/name=mcp-template-python

# 查看服务
kubectl get svc mcp-template-python

# 查看日志
kubectl logs -l app.kubernetes.io/name=mcp-template-python

# 进入容器
kubectl exec -it deployment/mcp-template-python -- /bin/bash

# 查看配置
helm get values mcp-template-python
```

## 故障排除

### 常见问题

1. **Pod 启动失败**
   - 检查镜像是否存在
   - 确认资源配置是否合理
   - 查看 Pod 事件：`kubectl describe pod <pod-name>`

2. **健康检查失败**
   - 确认应用是否提供 `/health` 端点
   - 检查端口配置是否正确
   - 调整探针延迟时间

3. **服务无法访问**
   - 确认 Service 配置
   - 检查网络策略
   - 验证 Ingress 配置

### 获取帮助

```bash
# 查看 Chart 信息
helm show chart helm/mcp-template-python

# 查看所有配置选项
helm show values helm/mcp-template-python

# 验证模板渲染
helm template mcp-template-python helm/mcp-template-python
```

---

**注意**：生产环境部署前，请务必更新 `values-production.yaml` 中的资源配置和域名设置。
