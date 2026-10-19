# 🔍 Troubleshooting Guide

Common issues and how to resolve them.

## 🐳 Docker Issues

### "Docker daemon not running"
`devspeed` requires Docker to be active. 
- **Windows/Mac**: Ensure Docker Desktop is started.
- **Linux**: Run `sudo systemctl start docker`.
- **Verification**: Run `docker ps` in your terminal.

### Port Conflicts
If you see an error like `Bind for 0.0.0.0:5432 failed: port is already allocated`:
1. Identify the process using the port:
   - **Mac/Linux**: `lsof -i :5432`
   - **Windows**: `netstat -ano | findstr :5432`
2. Either kill the process or change the port in your `devspeed.yaml`:
   ```yaml
   services:
     postgres:
       port: 5433 # Changed from 5432
   ```
3. Run `devspeed up` again.

## 📄 Configuration Issues

### "Invalid YAML"
Ensure your `devspeed.yaml` follows the correct indentation. Avoid using tabs.
- **Tip**: Use a YAML validator or the `devspeed doctor` command to find the error.

### "Stack not found"
If a stack from `devspeed list` isn't working:
1. Update `devspeed`: `pip install --upgrade devspeed`.
2. Check if you have the necessary Docker images available.

## 🚀 Performance Tips

### Slow Container Start
If your containers take too long to start, check the `healthcheck` logs:
```bash
docker inspect <container_id> --format='{{json .State.Health}}'
```
You can adjust the health check intervals in the stack definition if you are creating a custom plugin.
