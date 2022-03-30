import threading
import os
import xmlrpc.client as xc
import pathlib
import uuid
import time

from xmlrpc.client import ServerProxy as Server

HOST = "localhost"
PORT = 9123
PIC_WIDTH = 1024
PIC_HEIGHT = 1024
PIC_DPI = 300


class MolViewer(object):
    __metaclass__ = xc
    def __init__(self, host=HOST, port=PORT):
        self.port = port
        self.host = host
        _thread = threading.Thread(target=os.system, args=(('pymol -cKRQ',)))
        _thread.setDaemon(True)
        _thread.start()
        time.sleep(3)

    def _add_methods(self):
        for method in self._server.system.listMethods():
            if method[0].islower():
                setattr(self, method, getattr(self._server, method))

    def start(self):
        self._server = Server(
            uri="http://%s:%d/RPC2" % (self.host, self.port)
        )
        if hasattr(self, '_server'):
            self._add_methods()


class MolFigure():

    def __init__(self):
        self.pymol = MolViewer(HOST)
        self.init()

    def init(self):
        self.pymol.start()
        self.pymol.deleteAll()
        return self

    def get_picture(self, molecule: str = '3odu') -> str:
        self.pymol.fetch(molecule)
        self.pymol.show_as('cartoon')
        self.pymol.bg_color('white')
        pic_dir = pathlib.Path().cwd()/'pictures'
        print(pic_dir)
        file_name = uuid.uuid4()
        pic_path = pic_dir / f'{file_name}.png'
        self.pymol.png(str(pic_path), PIC_WIDTH, PIC_HEIGHT, PIC_DPI)
        return pic_path


if __name__=='__main__':
    py_mol_pic_gen = MolFigure()
    list_mol = ['1d7q', '1r9m', '6lu7', '6y2e', '6y2f', '2bx4', '6lzg', '2x19', '2xwu', '1aon', '3odu' ]
    for mol in list_mol:
        py_mol_pic_gen.get_picture(mol)
