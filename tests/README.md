# LogMonitorSystem 测试指南

本目录包含 LogMonitorSystem 的测试脚本。

## 测试脚本

### 1. 综合系统测试
- **文件**: `test_system.py`
- **目的**: 测试系统所有功能，包括日志创建、查询、告警生成、告警处理和每日统计

## 如何运行测试

### 前提条件
1. 确保所有服务已启动：
   - Django 开发服务器
   - Celery Worker
   - Celery Beat
   - MySQL 数据库
   - Redis 服务器

2. 安装必要的包：
   ```bash
   pip install requests
   ```

### 运行综合测试

```bash
python -m tests.test_system
```

### 测试内容

1. **创建测试应用**：在数据库中创建测试应用
2. **测试日志创建**：创建不同级别的日志（INFO、WARN、ERROR）
3. **测试日志查询**：使用各种过滤条件查询日志
4. **测试告警创建**：推送 101 条错误日志触发告警
5. **测试告警处理**：将告警标记为已处理
6. **测试每日统计**：手动触发每日统计任务

## 手动测试

### 测试日志创建
```bash
curl -X POST http://localhost:8000/api/logs/ ^
  -H "Content-Type: application/json" ^
  -d "{\"app\": 1, \"level\": \"ERROR\", \"message\": \"测试错误日志\"}"
```

### 测试日志查询
```bash
# 查询所有错误日志
curl http://localhost:8000/api/logs/?level=ERROR

# 按应用和级别查询日志
curl http://localhost:8000/api/logs/?level=ERROR&app=1
```

### 测试告警查询
```bash
curl http://localhost:8000/api/alerts/
```

### 测试告警处理
```bash
# 将 {id} 替换为实际的告警 ID
curl -X PATCH http://localhost:8000/api/alerts/{id}/resolve/
```
