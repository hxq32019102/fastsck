import os
from math import ceil
import uuid
from fastapi import APIRouter, Form, HTTPException, File, UploadFile
from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from sql_ import crud, schemas, models
from sql_.database import SessionLocal, engine
from utils.Pager import Pager, Pager2

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/dir/tree/dir")
def get_list_dir(parentid: int = None, current_page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    '''目录树可用于弹窗目录，不包含该目录下文件，只有文件夹
    parentid:默认根目录 None'''
    dirs = crud.get_dir_list(db, parent_id=parentid)
    res = Pager(dirs, per_page=limit, page=current_page)
    return {'total': res.counts,'total_page':res.pages, 'current_page': current_page, 'limit': limit, 'data': res.items}


@router.get("/dir/tree/dir_file/")
def get_list_dir_file(parentid: int = None, current_page: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    '''目录树可用于弹窗目录，不包含该目录下文件，只有文件夹
    parentid:默认根目录 None'''
    files = crud.get_file_list(db, dir_id=parentid).all()
    dirs = crud.get_dir_list(db, parent_id=parentid).all()

    res = Pager2(files=files,dirs=dirs, per_page=limit, page=current_page)
    return {'total': res.counts, 'total_page':res.pages,'current_page': current_page, 'limit': limit, 'data': res.items}

@router.post("/dir/create/")
def create_dir(dir: schemas.DirCreate, db: Session = Depends(get_db)):
    '''创建目录'''
    db_dir = crud.get_dir_by_id(db, id=dir.parent_id)
    if db_dir:
        if db_dir.status == 0:
            raise HTTPException(status_code=400, detail="dir create not allow")
        else:
            db_dir = crud.get_dir_by_name_parent_id(db, parent_id=dir.parent_id, dirname=dir.dir_name)
            if db_dir:
                raise HTTPException(status_code=400, detail="dir already exit")
            return crud.create_dir(db=db, dir=dir)
    raise HTTPException(status_code=400, detail="parentdid  not exit")


@router.post('/file/upload/')
async def file_upload(dir_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    '''单文件上传
    dir_id:文件上传路径id
    file:文件'''
    db_file = crud.get_dir_by_id(db, id=dir_id)
    if db_file:
        db_file = crud.get_file_by_dirid_filename(db, dirid=dir_id, filename=file.filename)
        if db_file:
            raise HTTPException(status_code=400, detail="file already exit")
        else:
            try:
                while 1:
                    uid = str(uuid.uuid1())
                    db_file = crud.get_file_by_uid(db, uid=uid)
                    if not db_file:
                        break
                path = 'static/data/' + uid
                res = await file.read()
                with open(path, "wb") as f:
                    f.write(res)
                # 保存在数据库
                filesize = os.path.getsize(path)
                return crud.create_file(db=db, dir_id=dir_id, file_size=filesize, uid=uid, file_name=file.filename)
            except Exception as e:
                return {"message": str(e), 'filename': file.filename}
    raise HTTPException(status_code=400, detail="dir not exit")


@router.get('/file/download/')
async def file_down(uid: str, db: Session = Depends(get_db)):
    '''根据uid下载文件'''
    file_ = crud.get_file_name_by_url(db, uid=uid)
    if file_:
        return FileResponse('static/data/' + uid, filename=file_.file_name)


@router.get("/MD5/123123/")
async def mergeChunks(chunkNumber: int,
                      chunkSize: str,
                      currentChunkSize: int,
                      filename: str,
                      identifier: str,
                      relativePath: int,
                      totalChunks: int,
                      totalSize: int, db: Session = Depends(get_db)):
    '''
     * 当前文件块，从1开始  Integer chunkNumber;
     * 分块大小 private Long chunkSize;
     * 当前分块大小private Long currentChunkSize;
     * 总大小private Long totalSize;
     * 文件标识private String identifier;
     * 文件名private String filename;
     * 相对路径private String relativePath;
     * 总块数private Integer totalChunks;
     * 二进制文件private MultipartFile file;
    '''
    # 判断文件名字是否重复
    db_filename = crud.get_file_by_dirid_(db, dirid=relativePath, filename=filename)
    if db_filename:
        raise HTTPException(status_code=400, detail="该目录下已存在" + filename)
    # 判断文件是否秒传 a. 如果是秒传，在请求结果中会有相应的标识，比如我这里是skipUpload为true，且返回了url，代表服务器告诉我们这个文件已经有了，我直接把url给你，你不用再传了，这就是秒传。
    db_md5 = crud.get_file_by_MD5_(db, MD5=identifier)
    if db_md5:
        # md5存在妙传，将文件添加到数据库，同时生成缩略图
        return {"skipUpload": "true", "file": '文件信息'}
    # 判断文件是否断点续传 如果后台返回了分片信息，这是断点续传。如图，返回的数据中有个uploaded的字段，代表这些分片是已经上传过的了，插件会自动跳过这些分片的上传。
    import os
    paths = os.listdir('static/tmp')
    uploaded = []
    if identifier + '_' + str(chunkNumber) in paths:
        for i in paths:
            if identifier in i:
                uploaded.append(i.split('_')[-1])
        return {"skipUpload": "false", "uploaded": uploaded}
    # 可能什么都不会返回，那这就是个全新的文件了，走完整的分片上传逻辑
    return


@router.post("/MD5/123123/")
async def mergeChunks(fileupload: schemas.FileUpload, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return True
