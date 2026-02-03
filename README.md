# LogMonitorSystem

日志采集与告警系统（LogMonitorSystem）是一个基于 Django 框架实现的日志管理系统，支持日志采集、告警生成和统计分析功能。

## 技术栈

- Python
- Django
- Celery
- Redis
- MySQL
- Django REST Framework

## 功能特性

- **日志采集**：接收并存储外部系统推送的日志
- **日志查询**：支持按级别和系统查询日志
- **告警管理**：自动生成错误日志告警并支持告警处理
- **定时任务**：每10分钟检查错误日志数量，每天生成日志统计报告

## 项目结构

```
log_monitor_system/
├── apps/
│   ├── core/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tasks.py
│   └── __init__.py
├── __init__.py
├── celery.py
├── manage.py
├── settings.py
└── urls.py
```

## 快速开始

### 1. 安装依赖

在项目根目录执行以下命令：

```bash
pip install -r requirements.txt
```

### 2. 数据库准备

1. 确保 MySQL 服务已启动
2. 创建名为 `log_monitor_system` 的数据库
3. 修改 `settings.py` 中的数据库配置（如果需要）：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'log_monitor_system',
        'USER': 'root',  # 替换为你的 MySQL 用户名
        'PASSWORD': '',  # 替换为你的 MySQL 密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 数据库迁移

执行以下命令创建数据库表结构：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 启动 Redis 服务

确保 Redis 服务已启动，默认端口为 6379。

## 数据库表结构

### 核心业务表

- **core_app**：存储业务系统信息
  - 字段：id、name（系统名称）、owner（负责人）、created_at（创建时间）

- **core_log**：存储日志记录
  - 字段：id、app_id（所属系统）、level（日志等级：INFO/WARN/ERROR）、message（日志内容）、created_at（创建时间）

- **core_alert**：存储告警记录
  - 字段：id、app_id（所属系统）、content（告警内容）、is_resolved（是否已处理）、created_at（创建时间）

- **core_logsummary**：存储每日日志统计摘要
  - 字段：id、app_id（所属系统）、info_count（INFO日志数量）、warn_count（WARN日志数量）、error_count（ERROR日志数量）、date（统计日期）

### Redis 存储

- **任务队列**：存储 Celery 任务
- **任务结果**：存储任务执行结果
- **消息绑定**：存储 Celery 相关的消息绑定信息

### 5. 启动服务

#### 5.1 启动 Celery Worker

在一个终端中执行：

```bash
celery -A log_monitor_system worker --loglevel=info
```

#### 5.2 启动 Celery Beat

在另一个终端中执行：

```bash
celery -A log_monitor_system beat --loglevel=info
```

#### 5.3 启动 Django 开发服务器

在第三个终端中执行：

```bash
python manage.py runserver
```

## API 文档

### 1. 推送日志

- **URL**: `POST /api/logs/`
- **请求体**:
  ```json
  {
    "app": 1,  # App ID
    "level": "ERROR",  # INFO/WARN/ERROR
    "message": "Error message here"
  }
  ```
- **响应**: 201 Created 带日志详情

### 2. 查询日志

- **URL**: `GET /api/logs/`
- **查询参数**:
  - `level`: 日志级别（可选）
  - `app`: App ID（可选）
- **示例**: `GET /api/logs/?level=ERROR&app=1`

### 3. 查询未处理告警

- **URL**: `GET /api/alerts/`
- **响应**: 未处理的告警列表

### 4. 处理告警

- **URL**: `PATCH /api/alerts/{id}/resolve/`
- **响应**: 更新后的告警详情

## 定时任务

1. **错误日志检查**: 每10分钟执行一次，检查过去10分钟内的错误日志数量，超过100则生成告警
2. **每日日志统计**: 每天00:00执行，生成前一天的日志统计报告

## 注意事项

- 确保 MySQL 和 Redis 服务正常运行
- 生产环境中建议使用 Supervisor 或类似工具管理 Celery 进程
- 生产环境中应修改 `settings.py` 中的 `SECRET_KEY` 和其他安全配置
