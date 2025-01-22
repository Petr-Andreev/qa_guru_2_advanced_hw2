# qa_guru_hw1
Python autotesting advanced

### Объяснение структуры `README.md`

1. **Предварительные условия:** 
   - Убедитесь, что у вас установлено следующее:
   - Python 3.12 или выше;
   - `pip` for package management;
   - `uvicorn` for running the FastAPI server;
   - `pytest` for running tests;
   - `fastapi-pagination` for pagination;

Вы можете установить необходимые пакеты, запустив:

```bash
pip install fastapi uvicorn pytest fastapi-pagination requests
```

2. **Как запустить сервер FastAPI:**
   - Инструкция по запуску FastAPI сервера с использованием `uvicorn`.
```bash
uvicorn app.main:app --reload 
```
   - Также есть возможность использовать SWAGGER:
   - В поисковую строку браузера нужно прописать: http://127.0.0.2:8000/docs

3. **Как запускать тесты:**
   - Запуск API тестов:
```bash
pytest
```