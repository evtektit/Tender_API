# Tender_API (ready v2)

### Установка
```
powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1
```

### Запуск API
```
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```
