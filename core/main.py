import pathlib
import time

from core.core import MolFigure
from fastapi import FastAPI
from fastapi.responses import FileResponse


pymol_inst = MolFigure()

app = FastAPI()
list_mol = ['1d7q', '1r9m', '6lu7', '6y2e', '6y2f', '2bx4', '6lzg', '2x19', '2xwu', '1aon', '3odu' ]

@app.get("/")
def root():
    return {"message": "Hello, All services working.", "list of molecules": list_mol}

@app.get("/picture/{mol}")
def picture(mol: str = '3odu'):
    if mol in list_mol:
        name = pymol_inst.get_picture(mol)
    else:
        name = pymol_inst.get_picture('3odu')
    while not pathlib.Path(name).is_file():
        time.sleep(1)
    return FileResponse(name)
