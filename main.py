# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 11:24 
# @Author : hxq
# @File : main.py
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic.schema import timedelta
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from dependencies import authenticate_user, create_access_token, get_current_active_user
from routers import user,up_down_load

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
# 可跨域访问的域名
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:33333",
]

# 可跨域访问的基本请求设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user.router,
    prefix="/users",
    tags=["用户"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)
app.include_router(
    up_down_load.router,
    prefix="/up_down",
    tags=["上传下载"],
    dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(minutes=15)
        )
        return {"access_token": access_token, "token_type": "bearer","username": user.username,}
    except Exception as e:
        return {"message": 'error'}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="10.10.14.5", port=8000, reload=True, debug=True)
    #testxsxsxsxsxsxsxsxsxsxsxsx