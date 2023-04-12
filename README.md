## 数据库同步脚本
将分库设置的表单数据定时同步到主库相应表中（全量同步）

初始先在主数据库中创建需要同步的分库数据库及表单，字段需一致

#### 运行：
```bash
python main.py
```

## 初始参数设置说明
main.py
db_params   # 分库连接参数
main_db_params  # 主库连接参数
SCHEDULE_MINUTES # 定时执行时间 单位分钟

table.py
tables  
需要同步的表及字段数据

