# -*- coding:utf-8 -*-
#!/usr/bin/env python3
''' This file is part of laForja (www.aprendizdetecnologo.com)

    laForja is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import tkinter as tk
from sistemaVentanas import *
nucleo=tk.Tk()
try:
    camino=os.getcwd()+os.sep+'laForja.db'
    print(camino)
    archivo=open(camino)
    archivo.close()
    miVentana=ventana(nucleo)
    #barraMenu=Menu(nucleo)
    #nucleo.config(menu=barraMenu)

    nucleo.mainloop()

except:
    import traceback
    traceback.print_exc()
    print ("Buscando base de datos...")
    miVentana=configuracion(nucleo)
    nucleo.mainloop()

