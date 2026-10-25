`response_class=HTMLResponse` and  `include_in_schema=false`

`/docs` and `/redoc`

`uv add "fastapi[standard]"`

`from fastapi import FastAPI`

`app=FastAPI()`

`uvicorn <module>:<attribute>` translates to `uvicorn main:<function>`

### Dynamic Path

```python
@app.get("/product/{id}")
def getPoduct(id: int):
    …
```

### Database connectivity

```bash
uv add sqlalchemy psycopg2
```

```python
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dburl="postgres://<USERNAME>:<PASSWORD>@localhost:5432/<DBNAME>"
engine=create_engine(dburl)
Session=sessionmaker(bind=engine)
```