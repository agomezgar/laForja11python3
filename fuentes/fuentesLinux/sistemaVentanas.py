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
from __future__ import division
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
import webbrowser
from PIL import ImageTk, Image
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import tkinter.simpledialog
import tkinter.messagebox as messagebox
from creaBaseDatos import *
from VerticalScrolledFrame import *
from functools import partial
import shutil
import subprocess
LARGE_FONT= ("Verdana", 12)
class ventana:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1024x748")
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=7)
        
        self.master.title("LaForja v2.00")
        self.marcoMaestro=tk.Frame(self.master)
        self.marcoAnidado=tk.Frame(self.master)
        self.marcoMaestro.grid(row=0,column=0,sticky="nsew")
        self.marcoAnidado.grid(row=1,column=0,sticky="nsew")
        barraMenu=Menu(self.master)
        self.master.config(menu=barraMenu)
        menuArchivo=Menu(barraMenu)
        barraMenu.add_cascade(label="Archivo",menu=menuArchivo)
        menuArchivo.add_command(label="Hacer copia de seguridad",command=lambda: self.hacerCopiaSeguridad())
        menuArchivo.add_command(label="Restaurar copia de seguridad",command=lambda: self.restaurarCopiaSeguridad())

        menuProgramacion=Menu(barraMenu)
        barraMenu.add_cascade(label="Programación",menu=menuProgramacion)
        menuProgramacion.add_command(label="Generar nueva Programación", command=lambda: self.generaProgramacion())
        #menuProgramacion.add_command(label="debug",command=lambda: self.generaProgramacion2('2','tecnologia'))
        menuNotas=Menu(barraMenu)
        barraMenu.add_cascade(label="Notas",menu=menuNotas)
        menuNotas.add_command(label="Poner notas", command=lambda: self.ponerNotas())
        menuNotas.add_command(label="Ver notas de grupo", command=lambda: self.notasGrupo())
        menuNotas.add_command(label="Ver notas individuales", command=lambda: self.notasIndividual())
        menuCambios=Menu(barraMenu)
        barraMenu.add_cascade(label="Cambios en Programación",menu=menuCambios)
        menuCambios.add_command(label="Añadir instrumentos de evaluación",command=lambda: self.cambiarInstrumentos())
        menuCambios.add_command(label="Cambiar estándares de trimestre",command=lambda: self.cambiarEstandar())
        menuInformes=Menu(barraMenu)
        barraMenu.add_cascade(label="Informes", menu=menuInformes)
        menuInformes.add_command(label="Justificar calificaciones",command=lambda: self.justificarCalificaciones())
        
        #menuArchivo=menu.add_cascade(label="Archivo",menu=self.master.barraMenu)
        boton1=tk.Button(self.marcoMaestro,text="Generar Programación",height=1,width=20,command=lambda: self.generaProgramacion())
        boton2=tk.Button(self.marcoMaestro,text="Poner notas",height=1,width=20,command=lambda: self.ponerNotas())
        boton3=tk.Button(self.marcoMaestro,text="Ver notas",height=1,width=20,command=lambda: self.notasGrupo())
        boton4=tk.Button(self.marcoMaestro,text="Ver notas por alumno",height=1,width=20,command=lambda: self.notasIndividual())

        boton5=tk.Button(self.marcoMaestro,text="Añadir instrumentos de evaluación",height=1,width=30,command=lambda: self.cambiarInstrumentos())
        boton6=tk.Button(self.marcoMaestro,text="Cambiar estándar de trimestre",height=1,width=30,command=lambda: self.cambiarEstandar())
        boton7=tk.Button(self.marcoMaestro,text="Justificar calificaciones",height=1,width=30,command=lambda: self.justificarCalificaciones())
        #boton7=tk.Button(self.marcoMaestro,text="Justificar calificaciones",height=1,width=30,command=lambda: self.generaProgramacion0(3,"tecnologia"))

        etiqueta=tk.Label(self.marcoAnidado,text="La Forja v 2.00",font=LARGE_FONT,height=1)

        #boton1.grid(row=0,column=0,padx=20,pady=20,columnspan=2)
        #boton2.grid(row=0,column=3,padx=20,pady=20,columnspan=2)
        #boton3.grid(row=0,column=5,padx=20,pady=20,columnspan=2)
        #boton4.grid(row=0,column=7,padx=20,pady=20,columnspan=2)
        #boton5.grid(row=1,column=1,padx=20,pady=20,columnspan=2)
        #boton6.grid(row=1,column=3,padx=20,pady=20,columnspan=2)
        #boton7.grid(row=1,column=5,padx=20,pady=20,columnspan=2)
        etiqueta.pack(side="top",anchor="n")
        archivo=os.getcwd()+os.sep+'logoAprendizTecnologo.png'
        img = ImageTk.PhotoImage(file=archivo)
        panel =tk.Label(self.marcoAnidado, image = img)
        panel.image=img
        panel.pack(fill = "both", expand = "yes")

        #boton1.pack(fill=X,expand=1,side=LEFT,padx=20,pady=20)
        #boton2.pack(fill=X,expand=1,side=LEFT,padx=20,pady=20)
        #boton3.pack(fill=X,expand=1,side=LEFT,padx=20,pady=20)
        #boton4.pack(fill=X,expand=1,side=LEFT,padx=20,pady=20)
        #boton5.pack(fill=X,expand=1,side=LEFT,padx=20,pady=20)
        #etiqueta.pack()
        self.contenidosGrabados=0
    def updateMarcoAnidado(self):
        self.marcoAnidado.destroy()
        self.marcoAnidado=tk.Frame(self.master)
        self.marcoAnidado.grid(row=1,column=0,sticky="nsew")

    def hacerCopiaSeguridad(self):
        fuente=os.getcwd()+"/laForja.db"
        destino=filedialog.asksaveasfilename(defaultextension='.db')
        #destino=filedialog.asksaveasfile(mode='w',defaultextension='db')
        shutil.copy(fuente, destino)
     
    def restaurarCopiaSeguridad(self):

        archivo = filedialog.askopenfilename(filetypes = (("Archivos db ", "*.db"),("All files", "*.*") ))
        destino=os.getcwd()+os.sep+'laForja.db'
        farchivo=open(archivo,'rb')
        fdestino=open(destino,'wb')
        
        shutil.copy(archivo,destino)


    def justificarCalificaciones(self):
       
        def eligeMateria(event):

            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            grupo=combo.get()
            #Obtenemos el nivel de estudios del grupo seleccionado
            base=baseDatos('laForja.db')            
            sql="SELECT estudios FROM matriculas WHERE grupo==(?)"
            niveles=base.cursor.execute(sql,(grupo,))
            nivel=niveles.fetchone()
             #Obtenemos la letra siete del nivel (E para ESO, B para Bachillerato, F para FPB)
            inicial=nivel[0][6]
            if (inicial=="E"):
                self.nivelMateria=int(nivel[0][0]);
            if (inicial=="B"):
                self.nivelMateria=int(nivel[0][0])+4;
            #print ("nivel: "+str(self.nivelMateria))
            self.materia=base.buscaMateriasCurso(self.nivelMateria)
            self.combo2["values"]=sorted(list(self.materia.values()))
            base.close()
            
        def eligeTrimestre(event):
            cTrimestre['state']="readonly"


        def dameNotas(event):
            trimestre=cTrimestre.current()
            seleccion = self.materia
            self.materiaElegida = list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            #self.materiaElegida=self.materia.keys()[self.combo2.current()]
            cTrimestre['state']="disabled"
            combo['state']="disabled"

            self.combo2['state']="disabled"

            base=baseDatos('laForja.db')
            # buscaPrioridades=base.cursor.execute("SELECT * FROM prioridades")
            # prioridades=buscaPrioridades.fetchall()
            #print ("Basico: "+str(prioridades[0][1]))
            #print ("Intermedio: "+str(prioridades[1][1]))
            #print ("Basico: "+str(prioridades[2][1]))
            lAlumnos=base.dameAlumnosporGrupo(combo.get())
            
            
            tablaOrganizacion=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
            tablaPonderacion=self.materiaElegida+"ponderacionCriterios"+str(self.nivelMateria)
            tablaEstandares="estandares"+self.materiaElegida
            tablaNotas=self.materiaElegida+"notas"+str(self.nivelMateria)
            tablaInstrumentos=self.materiaElegida+"instrumentos"+str(self.nivelMateria)
            estandares=[]
            #COMPROBAMOS SI SELECCIONAMOS POR TRIMESTRE O BUSCAMOS CURSO COMPLETO
            if not(trimestre==4):
                consulta="SELECT * FROM "+tablaOrganizacion+" WHERE trimestre=="+str(trimestre)+" ORDER BY idestandar"
            else:
                print ("Generando informe para curso completo")
                consulta="SELECT * FROM "+tablaOrganizacion+" ORDER BY idestandar"
                
            #print ("Consulta: "+consulta)
            ejconsulta=base.cursor.execute(consulta)
            recogeDatosOrganizacion=ejconsulta.fetchall()
            for r in recogeDatosOrganizacion:
                if not(r[2] in estandares):
                    #print(r[2])
                    estandares.append(r[2])
            nPesos={}
            for e in recogeDatosOrganizacion:
                consultaTexto="SELECT * FROM "+tablaEstandares+" WHERE id=(?)"
                textosEstandares=base.cursor.execute(consultaTexto,(e[2],))
                textos=textosEstandares.fetchone()
                #print("textos: "+str(textos))
                textoAux=textos[4]
                #print("textoAux: "+textoAux)
                consultaPonderacion="SELECT * FROM "+tablaPonderacion+" WHERE criterio==(?)"
                ejPonderaciones=base.cursor.execute(consultaPonderacion,(str(textoAux),))
                ponderaciones=ejPonderaciones.fetchone()
                ponderacion=ponderaciones[2]
                nPesos[e[2]]=ponderacion

            pesoRelativo=0;
            pesosOrdenados=sorted(nPesos.keys())
            for p in pesosOrdenados:
                #print("A "+p+" le corresponde un "+str(nPesos[p])+"%")
                pesoRelativo+=int(nPesos[p])
           
            nAlumno=0
#GENERAMOS UN PDF
            
            Story = []
            estilos = getSampleStyleSheet()
            cabecera=estilos['Heading1']
            cabecera2=estilos['Heading3']
            cabecera3=estilos['Normal']

            estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            #informe=canvas.Canvas('informe.pdf',pagesize=A4)
            doc = SimpleDocTemplate("informe.pdf", pagesize=A4,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
            width,height=A4
            label["text"]="GENERANDO INFORME..."
            for l in lAlumnos:
                notaFinalAlumno=0
                posicion=750
                texto="Alumno: "+l[1]+", "+l[2]
                #informe.drawString(100,posicion,)
                Story.append(Paragraph(texto, cabecera))
                posicion-=50
                #marco=VerticalScrolledFrame(marcoGeneral.interior)
                #marco.columnconfigure(0,weight=1)
                #marcoAlumnos.append(marco)
                #marcoAlumnos[nAlumno].grid(row=nAlumno,column=0,sticky="nsew")
                #marcoAlumnos[nAlumno].columnconfigure(0,weight=1)
                idAlumno=l[0]
                #etNombre=tk.Label(marcoAlumnos[nAlumno].interior,text="Alumno: "+l[1]+", "+l[2],relief="raised",font=LARGE_FONT,height=1,wraplength=600)
                #etNombre.grid(row=0,column=0,sticky="nsew")
                nCriterio=0
                mCriterios=[]
                #Llevo la cuenta de la fila en la que estoy
                nCuenta=1
                pesoTotal = 0
                #Vamos recorriendo los estándares del trimestre o curso
                for e in estandares:
                    notaEstandar=0
                    notaEstandarTemporal=0
                    pesoTotal=0
                    cuentaInstrumentos=0
                    consultaTexto = "SELECT * FROM " + tablaEstandares + " WHERE id=(?)"
                    textosEstandares = base.cursor.execute(consultaTexto, (e,))
                    textos = textosEstandares.fetchone()
                    #print ("Textos: "+str(textos))
                    texto="Criterio "+e+": "+textos[4]
                    Story.append(Paragraph(texto,cabecera2))
                    texto="Peso en la Programación Didáctica para todo el curso: "+str(nPesos[e])+ "%"
                    Story.append(Paragraph(texto,cabecera2))
                    #Si estamos calculando las notas por trimestre, habrá que rebaremar criterios
                    if not(trimestre==4):
                        texto="Peso relativo para el trimestre: {0: .2f}".format((nPesos[e]/pesoRelativo)*100)+"%"
                        pesoTotal=(nPesos[e]/pesoRelativo)*100
                        Story.append(Paragraph(texto,cabecera2))
                    else:
                        pesoTotal=nPesos[e]
                    #Buscamos los instrumentos que corresponden a ese estandar y trimestre
                    if not(trimestre==4):
                        consultaInstrumentos = "SELECT * FROM " + tablaOrganizacion + " WHERE idestandar=(?) AND trimestre=(?)"
                        ejInstrumentos = base.cursor.execute(consultaInstrumentos, (e,trimestre))
                    else:
                        consultaInstrumentos = "SELECT * FROM " + tablaOrganizacion + " WHERE idestandar=(?)"
                        ejInstrumentos = base.cursor.execute(consultaInstrumentos, (e,))
                    inst = ejInstrumentos.fetchall()
                    for i in inst:
                        cuentaInstrumentos+=1
                        # texto="Instrumento: "+str(i[3])
                        # Story.append(Paragraph(texto,cabecera3))
                        consultaNombreInstrumentos="SELECT * FROM "+tablaInstrumentos+" WHERE id=(?)"
                        ejNombreInstrumentos=base.cursor.execute(consultaNombreInstrumentos, (i[3],))
                        nombInst=ejNombreInstrumentos.fetchone()
                        texto="Instrumento de evaluación: "+nombInst[2]
                        Story.append(Paragraph(texto,cabecera3))
                        consultaNotasInstrumento="SELECT * FROM "+tablaNotas+" WHERE alumno=(?) AND instrumento=(?)"
                        ejConsultaNotasInst=base.cursor.execute(consultaNotasInstrumento, (l[0], i[3],))
                        notasInst=ejConsultaNotasInst.fetchall()
                        if (len(notasInst)>1):
                            texto="Hay varias notas de este instrumento: "

                            notaTemp=0
                            cuenta=0
                            for i in notasInst:
                                notaTemp+=i[3]
                                cuenta+=1
                                texto +=str(i[3])+" / "
                            Story.append(Paragraph(texto, cabecera3))

                            nota=notaTemp/cuenta
                            notaEstandarTemporal+=nota
                            texto = "Nota media: {0: .2f}".format(nota)
                            Story.append(Paragraph(texto, cabecera3))


                        else:
                            for i in notasInst:
                                texto="Nota: "+str(i[3])
                                Story.append(Paragraph(texto,cabecera3))
                                nota=i[3]
                                notaEstandarTemporal += nota
                    notaEstandar=notaEstandarTemporal/cuentaInstrumentos
                    notaEstandar=notaEstandar*pesoTotal/100

                    texto = "Aportación al conjunto de la nota final: {0: .2f}".format(notaEstandar)
                    Story.append(Paragraph(texto, cabecera3))
                    notaFinalAlumno+=notaEstandar

              

                texto=" Nota final para el alumno "+l[1]+", "+l[2]+":  {0: .2f}".format(notaFinalAlumno)
                Story.append(Paragraph(texto,cabecera))
                #informe.showPage()
                nAlumno+=1
                Story.append(PageBreak())
            base.close()
            doc.build(Story)
    
##            try:
##                webbrowser.open_new(r'informe.pdf')
##            except Exception as e:
##                print (e)
##                messagebox.showinfo("Problemas abriendo en navegador web","A continuación se abrirá el informe con el lector xpdf. Si hubiera algún error, asegúrese de tenerlo instalado")
##                #os.system('xpdf.real informe.pdf')
##                subprocess.Popen(os.path.abspath('informe.pdf'), shell=True)
        #PARA CREAR UN INFORME EN PDF EN LINUX, DADO QUE PYINSTALLER NO SE LLEVA BIEN CON EVINCE:
            os.system('xpdf.real informe.pdf')

        alumnos=[]
        filaInstrumentos=[]
        marcoAlumnos=[]
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoNotas=tk.Frame(self.marcoAnidado)
        marcoNotas.columnconfigure(0,weight=1)
        marcoNotas.rowconfigure(0,weight=1)
        marcoGeneral=VerticalScrolledFrame(marcoNotas)
        marcoGeneral.grid(row=0,column=0,sticky="nsew")
        marcoGeneral.columnconfigure(0,weight=1)


        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoNotas.grid(row=1,column=0,sticky="nsew")
        marcoNotas.columnconfigure(0,weight=1)

        try:
            curso=""
            
            estandares=[]
            etiquetas=[]
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia y trimestre", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            grupos=base.buscaGrupos()
            combo["values"] = grupos
            base.close()
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre","Curso completo"]
            cTrimestre.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameNotas)
        except:
            import traceback
            traceback.print_exc()
            
    def cambiarEstandar(self):
        def eligeMateria(event):
            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            combo['state']="disabled"
            self.nivelMateria=combo.current()
            #Obtenemos el nivel de estudios del grupo seleccionado
           
            self.materia=base.buscaMateriasCurso(self.nivelMateria)
            self.combo2["values"]=sorted(list(self.materia.values()))

        def eligeTrimestre(event):
            combo['state']="disabled"
            self.combo2['state']="disabled"
            cTrimestre['state']="readonly"
            seleccion = self.materia
            self.materiaElegida = list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            #self.materiaElegida=list(self.materia.keys())[self.combo2.current()]
        def buscaInstrumentos(materia,curso,estandar,trimestreOriginal,trimestreNuevo):
            #messagebox.showinfo("holis", "materia: "+materia+", curso: "+str(curso)+"estandar, "+str(estandar)+", trimestre: "+str(trimestre))
            base=baseDatos('laForja.db')
            print ("actualizando a "+str(trimestreOriginal))
            base.actualizaEstandaryTrimestre(materia,str(curso),estandar,str(trimestreOriginal),str(trimestreNuevo))
            base.close()


        def cambiaEstandares(event,estandar,trimestre):
            if  (event.widget.get()==""):
                print ("No hay cambios")
            else:
                #print ("Trimestre: "+event.widget.get())
                #print (event.widget.current())
                #print (estandar)
                trimestreOriginal=self.trimestre
                trimestreNuevo=event.widget.current()
                if (trimestreOriginal==trimestreNuevo):
                    print ("No hay cambios")
                else:
                    print ("Estandar en función: "+str(estandar))
                    #print ("Cambiamos de trimestre: "+str(trimestreOriginal)+" a: "+str(trimestreNuevo)+", "+event.widget.get())

                    buscaInstrumentos(self.materiaElegida, self.nivelMateria,str(estandar),trimestreOriginal,trimestreNuevo)
                    self.trimestre=trimestreNuevo
               
        def dameEstandares(event):
            cTrimestre['state']="disabled"
            self.trimestre=cTrimestre.current()
            #messagebox.showinfo("Información completa", str(self.nivelMateria)+", "+self.materiaElegida+", "+str(self.trimestre))
            base=baseDatos('laForja.db')
            estandares=base.buscaEstandaresporTrimestre(str(self.nivelMateria),self.materiaElegida,str(self.trimestre))
            fila=0
            for e in estandares:
                marco=VerticalScrolledFrame(marcoGeneral.interior)
                marco.grid_columnconfigure(0, weight=1)
                marcos.append(marco)
                marcos[fila].grid(row=fila,column=0,sticky="ew")
                

                texto=base.identificaEstandar(self.materiaElegida,e[0])
                etEstandar=tk.Label(marcos[fila].interior,text=texto[0][0],relief="raised",wraplength=600)
                etEstandares.append(etEstandar)
                etEstandar.grid(row=0,column=0,sticky="nsew")
                cTrimestre2=ttk.Combobox(marcos[fila])
                cTrimestre2["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
                cTrimestre2.current(self.trimestre)
                cTrimestre2.bind("<<ComboboxSelected>>", lambda event, estandar=e[0],trimestre=cTrimestre2.get() :cambiaEstandares(event,estandar,trimestre))
                cTrimestre2.pack()

                fila=fila+1
            base.close()
            
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoInstrumentos=tk.Frame(self.marcoAnidado)
        marcoInstrumentos.columnconfigure(0,weight=1)
        marcoInstrumentos.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoInstrumentos.grid(row=1,column=0,sticky="nsew")       
        marcoGeneral=VerticalScrolledFrame(marcoInstrumentos)
        marcoGeneral.grid(row=0,column=0,sticky="nsew")
        etEstandares=[]
        cbEstandares=[]
        marcos=[]
        try:
            curso=""
            
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia, y trimestre", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            combo["values"] = ["","1º ESO","2º ESO","3º ESO", "4º ESO", "1º BACHILLERATO", "2º BACHILLERATO"]
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
            cTrimestre.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameEstandares)

        except:
            import traceback
            traceback.print_exc()         
        
    def cambiarInstrumentos(self):

        def eligeMateria(event):
            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            self.nivelMateria=combo.current()
            #Obtenemos el nivel de estudios del grupo seleccionado
           
            self.materia=base.buscaMateriasCurso(self.nivelMateria)
            self.combo2["values"]=sorted(list(self.materia.values()))

        def eligeTrimestre(event):
            cTrimestre['state']="readonly"
            seleccion=self.materia
            self.materiaElegida=list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            #self.materiaElegida=list(self.materia.keys())[self.combo2.current()]
            
            
        def dameInstrumentos(event):

            def borraInstrumentos(self,nInstrumento,instrumento):
                mensaje1 = messagebox.askquestion ('Borrar instrumento ','¿Desea Vd. borrar este instrumento?',icon = 'warning')
                if mensaje1 == 'yes':
                    base=baseDatos('laForja.db')
                    base.borraInstrumentos(str(nivelMateria),materiaElegida,instrumento)
                    messagebox.showinfo("Instrumento borrado","El instrumento de evaluación ha sido borrado")
                    etInstrumentos[nInstrumento]["text"]="¡Borrado!"
                    base.close()
            def pideCadena(fila,contenido,estandares):
                mensaje1 = messagebox.askquestion ('Nuevo instrumento','¿Desea Vd. crear un nuevo instrumento de evaluacion?',icon = 'warning')
       
                if mensaje1 == 'yes':
                    for e in etInstrumentos:
                        e.destroy()
                    botones[fila].destroy()
                    valor=StringVar()
                    entrada=tk.Entry(marcos[fila].interior,textvariable=valor,width=50)
                    entrada.grid(row=fila+1,column=0,sticky="nsew")
                    botonGrabar=tk.Button(marcos[fila].interior,text="Grabar ",command=lambda fila=fila, entrada=entrada,estandares=estandares :nuevoInstrumento(fila,entrada,estandares))
                    botonGrabar.grid(row=fila+2,column=0)
                    #botones[fila]["text"]="Grabar"
                    #botones[fila]["command"]=(partial (nuevoInstrumento,fila,entrada))
        
                    
            def sumaInstrumento(fila,entrada):
                print ("fila: "+str(fila))
                print ("Instrumento: "+entrada.get())
                self.updateMarcoAnidado()
                self.marcoAnidado.rowconfigure(0,weight=1)
                self.marcoAnidado.rowconfigure(1,weight=5)
                self.marcoAnidado.columnconfigure(0,weight=1)
                marcoInstrumentos=tk.Frame(self.marcoAnidado)
                marcoInstrumentos.columnconfigure(0,weight=1)
                marcoInstrumentos.rowconfigure(0,weight=1)
                marcoTitulo=tk.Frame(self.marcoAnidado)
                marcoTitulo.grid(row=0,column=0,sticky="nsew")
                marcoInstrumentos.grid(row=1,column=0,sticky="nsew")       
                marcoGeneral=VerticalScrolledFrame(marcoInstrumentos)
                marcoGeneral.grid(row=0,column=0,sticky="nsew")
                instrumentosaGrabar=[]
                base=baseDatos('laForja.db')
                estandares=base.buscaEstandaresporContenido(str(nivelMateria),materiaElegida,contenidos[fila])
                filaEstandar=0
                print ("Nivel materia: "+str(nivelMateria))
                print ("Materia Elegida: "+materiaElegida)
                print ("Bloque de contenidos: "+contenidos[fila])
                instrumentos=base.buscaInstrumentosporContenido(str(nivelMateria),materiaElegida,contenidos[fila][0])
                for e in estandares:
                    print (e)
                    etEstandar=tk.Label(marcoGeneral.interior, text=e[4],justify="left",relief="raised")
                    etEstandar.grid(row=filaEstandar,column=0)
                    frameInstrumentos=VerticalScrolledFrame(marcoGeneral.interior)
                    frameInstrumentos.grid(row=filaEstandar,column=1)
                    filaInst=0
                    for i in instrumentos:
                        valor=IntVar()
                        cInst=tk.Checkbutton(frameInstrumentos.interior,text=i[0],variable=valor)
                        instrumentosaGrabar.append(cInst)
                        nombreTabla=self.materiaElegida+"Instrumentos"+str(self.nivelMateria)
                        sql="SELECT * FROM "+nombreTabla+" WHERE instrumento==(?)"                        
                        buscaInst=base.cursor.execute(sql,(i[0],)).fetchone()
                        nombreTabla=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
                        
                        sql2="SELECT * FROM "+nombreTabla+" WHERE idestandar=(?), idinstrumento=(?) and trimestre=(?)"
                        buscaCoincidencia=base.cursor.execute(sql,(str(e[0]),str(cInst[0]),str(trimestre),)).fetchone()

                        #print(str(buscaInst[0])+", "+str(e[0]))
                        cInst.grid(row=filaInst,column=0)
                        filaInst=filaInst+1
                    filaEstandar=filaEstandar+1
                    
                base.close()
            def asignaInstrumento(estandar,fila,idInstrumento):
                #messagebox.showinfo("Estandar grabado",estandar)
                base=baseDatos('laForja.db')
                if (vEstandares[fila].get()==1):
                    print ("Grabando el instrumento "+str(idInstrumento))
                    accion="grabar"
                    

                    #base.asignaInstrumentoEstandar(curso,materia,CPrioridades[indice2].current(),estandar,idInstrumento,CTrimestres[indice2].current()+1,"grabar")
                else:
                    print ("Borrando el instrumento "+str(idInstrumento))
                    accion="borrar"
                    #base.asignaInstrumentoEstandar(curso,materia,CPrioridades[indice2].current()+1,estandar,idInstrumento,CTrimestres[indice2].current()+1,"borrar")
                base.nuevoInstrumentoEstandar(nivelMateria,materiaElegida,estandar,idInstrumento,trimestre,accion)
                base.close()
           
            def nuevoInstrumento(fila,entrada,estandares):
                instrumento=entrada.get()
                #botones[fila]['state'] = 'disabled'
                entrada['state']='disabled'
                #print ("fila: "+str(fila))
                #print ("Instrumento: "+entrada.get())
                #print ("Contenido: "+contenidos[fila])
                #print ("Se superan los diez bloques de contenido: "+str(muchosContenidos))
                
                self.updateMarcoAnidado()
                self.marcoAnidado.rowconfigure(0,weight=1)
                self.marcoAnidado.rowconfigure(1,weight=5)
                self.marcoAnidado.columnconfigure(0,weight=1)
                marcoInstrumentos=tk.Frame(self.marcoAnidado)
                marcoInstrumentos.columnconfigure(0,weight=1)
                marcoInstrumentos.rowconfigure(0,weight=1)
                marcoTitulo=tk.Frame(self.marcoAnidado)
                marcoTitulo.grid(row=0,column=0,sticky="nsew")
                marcoInstrumentos.grid(row=1,column=0,sticky="nsew")       
                marcoGeneral=VerticalScrolledFrame(marcoInstrumentos)
                marcoGeneral.grid(row=0,column=0,sticky="nsew")
                
                instrumentosaGrabar=[]
                base=baseDatos('laForja.db')
                nombreTabla=self.materiaElegida+"Instrumentos"+str(self.nivelMateria)
                #print (nombreTabla)
                consulta="INSERT INTO "+nombreTabla+"(contenido,instrumento, trimestre) VALUES (?,?,?)"
                if contenidos[fila][8].isdigit():
                    print ("El bloque de contenidos es mayor que  9. Es: "+str(contenidos[fila][0])+str(contenidos[fila][1]))
                    #Para concatenar ambas cifras, las convierto a string, las sumo y luego las vuelvo a pasar como int
                    a=str(contenidos[fila][7])
                    b=str(contenidos[fila][8])
                    c=a+b
                    base.cursor.execute(consulta, (int(a+b), instrumento, trimestre))

                else:
                    print ("El bloque de contenidos es menor que  9. Es: "+str(contenidos[fila][0]))
                    base.cursor.execute(consulta, (contenidos[fila][7], instrumento, trimestre))
                #base.cursor.execute(consulta,(contenidos[fila][7],instrumento,trimestre))
                #Obtenemos el numero de instrumento nuevo en la tabla
                idInstrumentoNuevo=0
                consulta="SELECT id FROM "+nombreTabla+" ORDER BY id DESC LIMIT 1"
                result=base.cursor.execute(consulta)
                idInstrumentoNuevo = result.fetchone()
                #messagebox.showinfo("Nuevo instrumento",idInstrumentoNuevo)
                #Hay que comprobar si cada bloque de contenidos tiene uno o dos digitos (cuando haya mas de diez bloques)
                if contenidos[fila][8].isdigit():
                    print ("El bloque de contenidos es mayor que  9. Es: "+str(contenidos[fila][0])+str(contenidos[fila][1]))
                else:
                     print ("El bloque de contenidos es menor que  9. Es: "+str(contenidos[fila][0]))
                nombreTabla="estandares"+materiaElegida
                consulta="SELECT DISTINCT * FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
                result=base.cursor.execute(consulta,(contenidos[fila],nivelMateria),)
                estandaresAfectados=result.fetchall()
                base.close()
                labelInforma = tk.Label(marcoGeneral.interior, text="Indique qué estándares ayudará a evaluar este nuevo instrumento.",wraplength=450, font=LARGE_FONT)
                labelInforma.grid(row=2,column=0,columnspan=2)
                filaE=3

                estandarN=0
                for e in estandaresAfectados:
                    print ("Estandar: "+str(e[0]))
                    #etEstandar=tk.Label(marcos[fila].interior,text=e[4],width=45,wraplength=150,anchor='center', justify='left', relief="raised",padx=5,pady=5)
                    #etEstandar.grid(row=filaE,column=0,sticky="nsew")
                    valor=BooleanVar()
                    vEstandares.append(valor)
                    cbEstandar=tk.Checkbutton(marcoGeneral.interior, variable=vEstandares[estandarN],text=e[4],wraplength=350,anchor='w', padx=30, pady=30,justify='left',relief='raised',command=lambda estandar=e[0],fila=estandarN,idInstrumento=idInstrumentoNuevo:asignaInstrumento(estandar,fila,idInstrumento[0]))
                    cbEstandares.append(cbEstandar)
                    cbEstandares[estandarN].grid(row=filaE,column=0,sticky="nsew")
                    filaE=filaE+1
                    estandarN=estandarN+1
                
                botonFinal=tk.Button(marcoGeneral.interior,text="He terminado ",command= lambda: self.updateMarcoAnidado())
                botonFinal.grid(row=filaE,column=0,columnspan=2)

                
            fila1=0
            columna1=1
            numeroEtInst=0
            marcos=[]
            etInstrumentos=[]
            etEstandares=[]
            contenidos=[]
            instrumentos=[]
            botones= []
            del etInstrumentos[:]
            del instrumentos[:]
            del contenidos[:]
            #Esta variable esta a prueba. Se supone que si superamos los diez bloques de contenido, se disparara a True
            muchosContenidos=False
            trimestre=cTrimestre.current()
            nivelMateria=self.nivelMateria
            materiaElegida=self.materiaElegida
            nombreTabla=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
            cTrimestre['state']="disabled"
            combo['state']="disabled"
            self.combo2['state']="disabled"
            label['text']="Pinche en un instrumento si desea eliminarlo. Para añadir instrumentos, pulse el botón de abajo"
            base=baseDatos('laForja.db')
            #DE LA TABLA DE ORGANIZACION DE ESTANDARES SACAMOS LOS ESTANDARES INVOLUCRADOS
            sql="SELECT DISTINCT idestandar FROM "+nombreTabla+" WHERE trimestre=(?) ORDER BY idestandar"
           
            estandares=base.cursor.execute(sql,(trimestre,)).fetchall()
            print ("Buscando estandares en "+nombreTabla+" para el trimestre "+str(trimestre))
            #for e in estandares:
            #    print (str(e))
          
 
            nombreTabla="estandares"+self.materiaElegida
            #SACO LOS BLOQUES DE CONTENIDO CORRESPONDIENTES A CADA ESTANDAR (SE REPITEN MUCHISIMO, HAY UN ERROR DE DISEÑO EN LA BASE DE DATOS)
            contenidos=[]
            #Saco el primer contenido
            sql="SELECT  * FROM "+nombreTabla+" WHERE id==(?)"
            valor = base.cursor.execute(sql, (estandares[0][0],))
            contenido = valor.fetchone()
            contenidos.append(contenido[2])
            cuentaC=0;
            for e in estandares:
                valor=base.cursor.execute(sql,(e[0],))
                contenido=valor.fetchone()
                #print("contenido parcial: "+str(contenido))
                if not(contenidos[cuentaC]==contenido[2]):
                    contenidos.append(contenido[2])
                    cuentaC+=1
            filaBoton=3
            print ("Contenidos: "+str(contenidos))
            #NUEVO ENFOQUE EN SEGUNDA VERSIÓN: EN CADA CONTENIDO, REVISAMOS CADA ESTÁNDAR
            #(TENEMOS LAS DOS LISTAS), Y SI EN LA TABLA DE ESTÁNDARES VEMOS QUE EL ESTÁNDAR
            #Y EL CONTENIDO COINCIDEN PASAMOS A RECOGER LOS INSTRUMENTOS DE CADA ESTÁNDAR PARA ESE TRIMESTRE.

            for c in contenidos:
                marco = VerticalScrolledFrame(marcoGeneral.interior)
                marcos.append(marco)
                marcos[fila1].grid(row=fila1, column=0, sticky="nsew")
                etContenido = tk.Label(marcos[fila1].interior, text=c)
                etContenido.grid(row=0, column=0, sticky="nsew")

                fila2=1
                nTablaEst="estandares"+self.materiaElegida
                nTablaOrg=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
                inst = []
                estandaresporContenido=[]
                for e in estandares:
                    sql = "SELECT  * FROM " + nTablaEst + " WHERE id==(?) AND bloque=(?)"
                    #print(sql+", "+c+", "+e[0])
                    valor = base.cursor.execute(sql, (e[0],c,))
                    contenido = valor.fetchone()
                    print ("contenido: "+str(contenido))



                    if (contenido):
                        #UNA VEZ LOCALIZADA LA CORRESPONDENCIA ENTRE ESTÁNDAR Y CONTENIDO,
                        #PROCEDEMOS A BUSCAR INSTRUMENTOS (SIN REPETIRLOS) EN LA TABLA DE ORGANIZACIÓN
                        #DE ESTÁNDARES. CREAMOS UNA MATRIZ DE ENTEROS CON LAS ID DE CADA INSTRUMENTO
                        estandaresporContenido.append(contenido)
                        sql="SELECT  * FROM " + nTablaOrg + " WHERE idestandar==(?) AND trimestre=(?)"
                        valor=base.cursor.execute(sql,(e[0],trimestre))
                        contenido2=valor.fetchall()
                        for c2 in contenido2:
                            #print("Al estandar "+e[0]+" en el trimestre "+str(trimestre)+" se le mide con el instrumento"+c2[3])
                            if not (c2[3] in inst):
                                inst.append(c2[3])
                    #Creamos los marcos para cada bloque de contenidos
                nTablaInst=self.materiaElegida+"Instrumentos"+str(nivelMateria)
                for i in inst:
                    sql = "SELECT  * FROM " + nTablaInst + " WHERE id==(?)"
                    valor = base.cursor.execute(sql, (i,))
                    nombreInst = valor.fetchone()
                    #print(str(nombreInst))
                    etInstrumento=tk.Label(marcos[fila1].interior,text=str(nombreInst[2]),relief="raised",wraplength=300)
                    etInstrumentos.append(etInstrumento)
                    etInstrumentos[numeroEtInst].grid(row=fila2,column=0,sticky="nsew")
                    etInstrumentos[numeroEtInst].bind("<Button-3>", lambda event, nInstrumento=numeroEtInst , instrumento=nombreInst[0] : borraInstrumentos(event,nInstrumento,instrumento))

                    #columna1=columna1+1
                    numeroEtInst=numeroEtInst+1
                    #etInst = tk.Label(marcos[fila1].interior, text=str(nombreInst[2]))
                    #etInst.grid(row=fila2, column=0, sticky="nsew")
                    fila2+=1
                boton=tk.Button(marcos[fila1].interior,text="Nuevo instrumento ",command= partial(pideCadena,fila1,c,estandaresporContenido))
                botones.append(boton)
                botones[fila1].grid(row=fila2,column=0)
                fila1 += 1
            # for c in contenidos:
            #
            #     del instrumentos[:]
            #     marco=VerticalScrolledFrame(marcoGeneral.interior)
            #     marcos.append(marco)
            #     marcos[fila1].grid(row=fila1,column=0,sticky="nsew")
            #     etContenido=tk.Label(marcos[fila1].interior,text=c)
            #     etContenido.grid(row=0,column=0,sticky="nsew")
            #
            #     boton=tk.Button(marcos[fila1].interior,text="Nuevo instrumento ",command= partial(pideCadena,fila1))
            #     botones.append(boton)
            #     botones[fila1].grid(row=filaBoton+1,column=0)
            #     fila1=fila1+1
            #     nombreTabla=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
            #
            #     columna1=1
            #     filaBoton=3
            #     for e in estandares:
            #         print ("Iniciando búsqueda en: "+str(e[0]))
            #         #SI e[0][1] (el segundo digito del estandar) coincide con c[0] (el numero de bloque de contenido), se suma al array
            #         #OJO OJO OJO OJO SOLO SIRVE PARA UN MAXIMO DE 9 BLOQUES DE CONTENIDOS (PENDIENTE DE REDISEÑO)
            #         #print (e[0])
            #         if (len(e[0])==4):
            #             print("empezando..."+e[0][1]+", " +c[6])
            #             if (e[0][1]==c[6]):
            #                 print ("aumentando array...")
            #                 sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE idestandar==(?) AND trimestre==(?) ORDER BY idinstrumento"
            #                 valor=base.cursor.execute(sql,(e[0],trimestre,))
            #                 idInstrumento=valor.fetchall()
            #                 for i in idInstrumento:
            #                     instrumentos.append(i[0])
            #                 #if (idInstrumento[0] != instrumentos[-1]):
            #                 #    print (str(idInstrumento[0])+" no es igual a "+str(instrumentos[-1])+"; grabando...")
            #                 #    instrumentos.append(idInstrumento[0])
            #             instrumentos=list(set(instrumentos))
            #             instrumentos=sorted(instrumentos)
            #         if (len(e[0])==5):
            #             muchosContenidos=True
            #             if (e[0][1]+e[0][2]==c[0]+c[1]):
            #                 #print ("aumentando array...")
            #                 sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE idestandar==(?) AND trimestre==(?) ORDER BY idinstrumento"
            #                 valor=base.cursor.execute(sql,(e[0],trimestre,))
            #                 idInstrumento=valor.fetchall()
            #                 for i in idInstrumento:
            #                     instrumentos.append(i[0])
            #                 #if (idInstrumento[0] != instrumentos[-1]):
            #                 #    print (str(idInstrumento[0])+" no es igual a "+str(instrumentos[-1])+"; grabando...")
            #                 #    instrumentos.append(idInstrumento[0])
            #             instrumentos=list(set(instrumentos))
            #             instrumentos=sorted(instrumentos)
            #     for i in instrumentos:
            #         #print (i)
            #         nombreTabla=self.materiaElegida+"Instrumentos"+str(self.nivelMateria)
            #         #print (nombreTabla)
            #         sql="SELECT * FROM "+nombreTabla+" WHERE id=(?)"
            #         valor=base.cursor.execute(sql,(i,)).fetchone()
            #         #print (valor)
            #         etInstrumento=tk.Label(marcos[fila1].interior,text=valor[2],relief="raised",wraplength=300)
            #         etInstrumentos.append(etInstrumento)
            #         etInstrumentos[numeroEtInst].grid(row=filaBoton,column=0,sticky="nsew")
            #         etInstrumentos[numeroEtInst].bind("<Button-3>", lambda event, nInstrumento=numeroEtInst , instrumento=valor[0] : borraInstrumentos(event,nInstrumento,instrumento))
            #         filaBoton=filaBoton+1
            #         #columna1=columna1+1
            #         numeroEtInst=numeroEtInst+1
            #     cuenta=1
            #     # nombreTabla = "estandares" + self.materiaElegida
            #     # nombreTabla2 = self.materiaElegida + "organizacionEstandares" + str(self.nivelMateria)
            #     # for e in estandares:
            #     #     sql2 = "SELECT  * FROM " + nombreTabla + " WHERE id==(?)and bloque==(?)"
            #     #     valor=base.cursor.execute(sql2,(e[0],c,))
            #     #     print("Estandar: "+e[0]+", bloque: "+c)
            #     #     t=valor.fetchone()
            #     #     if (t):
            #     #         etEstandar=tk.Label(marcos[fila1].interior,text=t[4])
            #     #         etEstandar.grid(row=cuenta,column=0,sticky="nsew")
            #     #         cuenta+=1

            # print ("resultado: "+str(resultado))
            # #METO EL PRIMER BLOQUE DE CONTENIDOS
            # contenidos.append(resultado[2])
            # #print (contenidos[0])
            # #AHORA ESCARBAMOS EN EL RESTO DE BLOQUES, ELIMINANDO LOS QUE SE REPITEN
            # for estandar in estandares:
            #     #print ("Valor estandar: "+str(estandar[0]))
            #     sql="SELECT estandar FROM "+nombreTabla+" WHERE id==(?)"
            #     valor=base.cursor.execute(sql,(estandar[0],))
            #     resultado=valor.fetchall()
            #     #print ("Resultado: "+str(resultado[0]))
            #     for r in resultado:
            #         #print ("comprobando: "+r[0])
            #         if (r[0] != contenidos[-1]):
            #             contenidos.append(r[0])
            #
            # print("Contenidos:"+str(contenidos))
            # for c in contenidos:
            #
            #     del instrumentos[:]
            #     marco=VerticalScrolledFrame(marcoGeneral.interior)
            #     marcos.append(marco)
            #     marcos[fila1].grid(row=fila1,column=0,sticky="nsew")
            #     etContenido=tk.Label(marcos[fila1].interior,text=c)
            #     etContenido.grid(row=0,column=0,sticky="nsew")
            #     nombreTabla=self.materiaElegida+"organizacionEstandares"+str(self.nivelMateria)
            #
            #     columna1=1
            #     filaBoton=3
            #     for e in estandares:
            #         #SI e[0][1] (el segundo digito del estandar) coincide con c[0] (el numero de bloque de contenido), se suma al array
            #         #OJO OJO OJO OJO SOLO SIRVE PARA UN MAXIMO DE 9 BLOQUES DE CONTENIDOS (PENDIENTE DE REDISEÑO)
            #         #print (e[0])
            #         if (len(e[0])==4):
            #             if (e[0][1]==c[0]):
            #                 #print ("aumentando array...")
            #                 sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE idestandar==(?) AND trimestre==(?) ORDER BY idinstrumento"
            #                 valor=base.cursor.execute(sql,(e[0],trimestre,))
            #                 idInstrumento=valor.fetchall()
            #                 for i in idInstrumento:
            #                     instrumentos.append(i[0])
            #                 #if (idInstrumento[0] != instrumentos[-1]):
            #                 #    print (str(idInstrumento[0])+" no es igual a "+str(instrumentos[-1])+"; grabando...")
            #                 #    instrumentos.append(idInstrumento[0])
            #             instrumentos=list(set(instrumentos))
            #             instrumentos=sorted(instrumentos)
            #         if (len(e[0])==5):
            #             muchosContenidos=True
            #             if (e[0][1]+e[0][2]==c[0]+c[1]):
            #                 #print ("aumentando array...")
            #                 sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE idestandar==(?) AND trimestre==(?) ORDER BY idinstrumento"
            #                 valor=base.cursor.execute(sql,(e[0],trimestre,))
            #                 idInstrumento=valor.fetchall()
            #                 for i in idInstrumento:
            #                     instrumentos.append(i[0])
            #                 #if (idInstrumento[0] != instrumentos[-1]):
            #                 #    print (str(idInstrumento[0])+" no es igual a "+str(instrumentos[-1])+"; grabando...")
            #                 #    instrumentos.append(idInstrumento[0])
            #             instrumentos=list(set(instrumentos))
            #             instrumentos=sorted(instrumentos)
            #     for i in instrumentos:
            #         #print (i)
            #         nombreTabla=self.materiaElegida+"Instrumentos"+str(self.nivelMateria)
            #         #print (nombreTabla)
            #         sql="SELECT * FROM "+nombreTabla+" WHERE id=(?)"
            #         valor=base.cursor.execute(sql,(i,)).fetchone()
            #         #print (valor)
            #         etInstrumento=tk.Label(marcos[fila1].interior,text=valor[2],relief="raised",wraplength=300)
            #         etInstrumentos.append(etInstrumento)
            #         etInstrumentos[numeroEtInst].grid(row=filaBoton,column=0,sticky="nsew")
            #         etInstrumentos[numeroEtInst].bind("<Button-3>", lambda event, nInstrumento=numeroEtInst , instrumento=valor[0] : borraInstrumentos(event,nInstrumento,instrumento))
            #         filaBoton=filaBoton+1
            #         #columna1=columna1+1
            #         numeroEtInst=numeroEtInst+1
            #     boton=tk.Button(marcos[fila1].interior,text="Nuevo instrumento ",command= partial(pideCadena,fila1))
            #     botones.append(boton)
            #     botones[fila1].grid(row=filaBoton+1,column=0)
            #     fila1=fila1+1


         
        
            base.close()
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoInstrumentos=tk.Frame(self.marcoAnidado)
        marcoInstrumentos.columnconfigure(0,weight=1)
        marcoInstrumentos.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoInstrumentos.grid(row=1,column=0,sticky="nsew")       
        marcoGeneral=VerticalScrolledFrame(marcoInstrumentos)
        marcoGeneral.grid(row=0,column=0,sticky="nsew")
        vEstandares=[]
        cbEstandares=[]
        try:
            curso=""
            
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia, y trimestre", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            combo["values"] = ["","1º ESO","2º ESO","3º ESO", "4º ESO", "1º BACHILLERATO", "2º BACHILLERATO"]
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
            cTrimestre.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameInstrumentos)

        except:
            import traceback
            traceback.print_exc()         
        
    def notasIndividual(self):
        def eligeMateria(event):

            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            grupo=combo.get()
            #Obtenemos el nivel de estudios del grupo seleccionado
            base=baseDatos('laForja.db')            
            sql="SELECT estudios FROM matriculas WHERE grupo==(?)"
            niveles=base.cursor.execute(sql,(grupo,))
            nivel=niveles.fetchone()
             #Obtenemos la letra siete del nivel (E para ESO, B para Bachillerato, F para FPB)
            inicial=nivel[0][6]
            if (inicial=="E"):
                self.nivelMateria=int(nivel[0][0]);
            if (inicial=="B"):
                self.nivelMateria=int(nivel[0][0])+4;
            print ("nivel: "+str(self.nivelMateria))
            self.materia=base.buscaMateriasCurso(self.nivelMateria)

            self.combo2["values"]=sorted(list(self.materia.values()))
            base.close()
        def eligeTrimestre(event):
            cTrimestre['state']="readonly"
        def dameAlumnos(event):
            
            cAlumno['state']="readonly"
            base=baseDatos('laForja.db')            
            self.alumnos=base.dameAlumnosporGrupo(combo.get())
            nombreAlumnos=[]
            for a in self.alumnos:
                nombre=a[1]+", "+a[2]
                nombreAlumnos.append(nombre)
            cAlumno["values"]=nombreAlumnos
            base.close()
            
        def dameNotas(event):
            notasTemporal=[]
            def cambiaNota(self,indice,nota):
                base=baseDatos('laForja.db')            
                print ("Numero de fila: "+str(indice)+", indice en Tabla: "+str(notasTemporal[indice][1])+", nota: "+str(notasTemporal[indice][3]))
                print (notasTemporal[indice][1])
                mensaje1 = messagebox.askquestion ('Modificar nota','¿Desea Vd. modificar esta nota?',icon = 'warning')
                if mensaje1 == 'yes':
                    notaNueva = tk.simpledialog.askfloat ("Entrada", "Introduzca nuevo valor")
                    notasTemporal[indice][0]["text"]=notaNueva
                    base.actualizaNotas(notasTemporal[indice][4],notasTemporal[indice][5],notasTemporal[indice][1],notaNueva,"actualizar")
                    base.close()
                    
            def borraNota(self,indice,nota):
                base=baseDatos('laForja.db')                            
                print ("Numero de fila: "+str(indice)+", indice en Tabla: "+str(notasTemporal[indice][1])+", nota: "+str(notasTemporal[indice][3]))
                print (notasTemporal[indice][1])
                mensaje1 = messagebox.askquestion ('Borrar nota','¿Desea Vd. borrar esta nota?',icon = 'warning')
                if mensaje1 == 'yes':
                    notasTemporal[indice][0]["text"]=""
                    notaNueva=0
                    base.actualizaNotas(notasTemporal[indice][4],notasTemporal[indice][5],notasTemporal[indice][1],notaNueva,"borrar")
                    base.close()                    
                    messagebox.showinfo("Nota borrada","Se ha borrado la nota especificada")
                            
          
            alumno=self.alumnos[cAlumno.current()]
            #print ("Alumno seleccionado: "+alumno[1])
            trimestre=cTrimestre.current()
            seleccion = self.materia
            self.materiaElegida = list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]

            #self.materiaElegida=list(self.materia.keys())[self.combo2.current()]
            marcoFila=[]
            base=baseDatos('laForja.db')            
            #print ("Trimestre: "+str(trimestre))
            #print ("Materia: "+self.materiaElegida)
            #print ("Nivel materia: "+str(self.nivelMateria))
            inst=base.buscaInstrumentos2(self.nivelMateria,self.materiaElegida,trimestre)
            etNombre=tk.Label(marcoGeneral.interior,text="Alumno: "+alumno[1]+", "+alumno[2],relief="raised")
            etNombre.grid(row=0,column=0,sticky="nsew")
            fila1=1
            indiceInstrumento=0
            for i in inst:
                marco=tk.Frame(marcoGeneral.interior)
                marco.grid(row=fila1,column=0,sticky="nsew")
                marcoFila.append(marco)
                etInst=tk.Label(marco,text="Instrumento evaluador: "+i[2],width=15,wraplength=85,relief="raised")
                etInst.grid(row=0,column=0,sticky="nsew")
                nota=base.buscaNotas(self.nivelMateria,self.materiaElegida,alumno[0],i[0])
                n=1
                marcoNotasInstrumento=tk.Frame(marco,relief="raised",borderwidth=1)
                marcoNotasInstrumento.grid(row=0,column=1,sticky="nsew")
                for i in nota:
                    etN=tk.Label(marcoNotasInstrumento,text="Nota"+str(n))
                    etN.grid(row=fila1,column=0)
                    enNota=tk.Label(marcoNotasInstrumento,text=i[3])
                    notasTemporal.append([enNota,i[0],alumno[0],i[3],self.nivelMateria,self.materiaElegida])
                    enNota.grid(row=fila1,column=1)
                    enNota.bind("<Button-1>", lambda event, indice=indiceInstrumento, nota=i[3] : cambiaNota(event,indice,nota))
                    enNota.bind("<Button-3>", lambda event, indice=indiceInstrumento, nota=i[3] : borraNota(event,indice,nota))

                    indiceInstrumento=indiceInstrumento+1
                    n=n+1
                    fila1=fila1+1

             
                fila1=fila1+1
            base.close()


        alumnos=[]
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoNotas=tk.Frame(self.marcoAnidado)
        marcoNotas.columnconfigure(0,weight=1)
        marcoNotas.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoNotas.grid(row=1,column=0,sticky="nsew")       
        marcoGeneral=VerticalScrolledFrame(marcoNotas)
        marcoGeneral.grid(row=0,column=0,sticky="nsew")

        try:
            curso=""
            
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia, trimestre y alumno", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            grupos=base.buscaGrupos()
            combo["values"] = grupos
            base.close()
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
            cTrimestre.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameAlumnos)
            cAlumno=ttk.Combobox(marcoTitulo,state="disabled",width=40)
            cAlumno.pack(side="left",padx=20)
            cAlumno.bind("<<ComboboxSelected>>", dameNotas)
        except:
            import traceback
            traceback.print_exc()         

 
    def notasGrupo(self):
        def eligeMateria(event):

            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            grupo=combo.get()
            #Obtenemos el nivel de estudios del grupo seleccionado
            base=baseDatos('laForja.db')            
            sql="SELECT estudios FROM matriculas WHERE grupo==(?)"
            niveles=base.cursor.execute(sql,(grupo,))
            nivel=niveles.fetchone()
             #Obtenemos la letra siete del nivel (E para ESO, B para Bachillerato, F para FPB)
            inicial=nivel[0][6]
            if (inicial=="E"):
                self.nivelMateria=int(nivel[0][0]);
            if (inicial=="B"):
                self.nivelMateria=int(nivel[0][0])+4;
            #print ("nivel: "+str(self.nivelMateria))
            self.materia=base.buscaMateriasCurso(self.nivelMateria)
            self.combo2["values"]=sorted(list(self.materia.values()))
            base.close()
        def eligeTrimestre(event):
            cTrimestre['state']="readonly"


        def dameNotas(event):
            trimestre=cTrimestre.current()
            seleccion = self.materia
            self.materiaElegida = list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            self.materiaElegida=list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            print ("Calculando notas para: "+str(self.materiaElegida))
            cTrimestre['state']="disabled"
            combo['state']="disabled"

            self.combo2['state']="disabled"

            base=baseDatos('laForja.db')
            inst=base.buscaInstrumentos2(self.nivelMateria,self.materiaElegida,trimestre)
            for a in inst:
                idInstrumento=a[0]
                nombreInstrumento=a[2]
                filaInstrumentos.append(nombreInstrumento)
            alumn=base.dameAlumnosporGrupo(combo.get())
            for a in alumn:
                nombre=a[1]+", "+a[2]
                id=a[0]
                alumno=[id,nombre]
                alumnos.append(alumno)


            marcoGeneral=VerticalScrolledFrame(marcoNotas)
            marcoGeneral.grid(row=0,column=0,sticky="nsew")
            etNombre=tk.Label(marcoGeneral.interior,text="Alumno",relief="raised")
            etNombre.grid(row=0,column=0,sticky="nsew")
            columna=1
            for i in inst:
                etInst=tk.Label(marcoGeneral.interior,text=i[2],width=15,wraplength=85,relief="raised")
                etInst.grid(row=0,column=columna,sticky="nsew")
                columna=columna+1
            fila1=1
            for a in alumnos:

                nombreAlumno=tk.Label(marcoGeneral.interior,text=a[1],width=20,wraplength=140,relief="raised")
                nombreAlumno.grid(row=fila1,column=0,sticky="nsew")
                columna=1
                for i in inst:
                    nota=base.buscaNotas(self.nivelMateria,self.materiaElegida,a[0],i[0])
                    print("Nota para: "+str(a)+": "+str(nota))
                    if (len(nota)>1):
                        print("Multiples notas")
                        notaUnica=0
                        for n in nota:
                            notaUnica=notaUnica+n[3]
                        notaUnica=notaUnica/len(nota)
                        print("Nota media: %.2f" % (notaUnica))
                        texto="Media: %.2f \n (varias notas)"%(notaUnica)
                    if not nota:
                        print ("El alumno"+str(a[0])+" no tiene nota en "+str(i[2])+" para la materia "+str(self.materiaElegida))
                        texto="No hay nota"
                    if(len(nota)==1):
                        texto=str(nota[0][3])+" (nota única)"
                        print("nota unica")
                    
                    etNota=tk.Label(marcoGeneral.interior,text=texto,width=15,relief="raised")
                    etNota.grid(row=fila1,column=columna,sticky="nsew")
                    columna=columna+1
                fila1=fila1+1
            base.close()
        alumnos=[]
        filaInstrumentos=[]
        marcoAlumno=[]
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoNotas=tk.Frame(self.marcoAnidado)
        marcoNotas.columnconfigure(0,weight=1)
        marcoNotas.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoNotas.grid(row=1,column=0,sticky="nsew")       

        try:
            curso=""
            
            estandares=[]
            etiquetas=[]
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia y trimestre", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            grupos=base.buscaGrupos()
            combo["values"] = grupos
            base.close()
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
            cTrimestre.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameNotas)
        except:
            import traceback
            traceback.print_exc() 

    def ponerNotas(self):
        grupo=""
        nivelMateria=0
        materiaElegida=""
        trimestre=0
        materia=""
        instrumento=""
        idInstrumento=""
        def eligeCurso(event):
            print("ordenando diccionarios")
            if (self.combo.current()!=0):
                self.combo2["state"]="readonly"
                base= baseDatos('laForja.db')
                self.curso=self.combo.current()
                listaMaterias=base.buscaMateriasCurso(self.curso)
                self.materia = sorted(listaMaterias.items(), key=operator.itemgetter(1))

                print (self.materia)
                self.combo2["values"]=list(self.materia.values())
                base.close()

        def eligeMateria(event):
            self.combo2['state']="readonly"
            cTrimestre['state']="disabled"
            cInstrumento['state']="disabled"
            grupo=combo.get()
            #Obtenemos el nivel de estudios del grupo seleccionado
            base=baseDatos('laForja.db')            
            sql="SELECT estudios FROM matriculas WHERE grupo==(?)"
            niveles=base.cursor.execute(sql,(grupo,))
            nivel=niveles.fetchone()
             #Obtenemos la letra siete del nivel (E para ESO, B para Bachillerato, F para FPB)
            inicial=nivel[0][6]
            if (inicial=="E"):
                self.nivelMateria=int(nivel[0][0]);
            if (inicial=="B"):
                self.nivelMateria=int(nivel[0][0])+4;
            #print ("nivel: "+str(self.nivelMateria))
            self.materia=base.buscaMateriasCurso(self.nivelMateria)
            listaClaves=list(self.materia.keys())
            print("Lista claves: "+str(listaClaves))
            self.combo2["values"]=sorted(list(self.materia.values()))
            base.close()
        def eligeTrimestre(event):
            cTrimestre['state']="readonly"
            cInstrumento['state']="disabled"

                
        def dameInstrumentos(event):
            valor=cTrimestre.get()
            #print (valor)
            
        def dameAlumnos(event):
            trimestre=cTrimestre.current()
            base=baseDatos('laForja.db')
            seleccion=self.materia
            self.materiaElegida=list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            #print("Materia elegida: "+str(self.materiaElegida))
            #self.materiaElegida=list(self.materia.keys())[self.combo2.current()]
            #list(d.keys())[list(d.values()).index(v)]
            #print ("Materia elegida: "+self.materiaElegida)
            #print (self.combo2.current())

            instrumentos=base.buscaInstrumentos(self.nivelMateria,self.materiaElegida,trimestre)
            cInstrumento['state']="readonly"
            cInstrumento["values"]=instrumentos
            base.close()
        def dameTablaNotas(event):
            def grabarNotas():
                notasCorrectas=True
                print ("Grabaremos en un momento...")
                try:
                    for a in range(0,fila):

                        valor=float(Notas[a].get())
                        if ((valor<0) or (valor>10)):
                              messagebox.showinfo("Error en notas","Al alumno "+nombreAlumnos[a]+" no se le puede poner una nota inferior a 0 o superior a 10")
                              notasCorrectas=False
                              break

                except:
                    messagebox.showinfo("Error en notas","Al alumno "+nombreAlumnos[a]+" se le ha puesto por error una nota no numerica")
                    notasCorrectas=False

                try:
                    if (notasCorrectas==True):
                        print ("¡Todo esta bien!")
                        resultado=[]
                        for a in range(0,fila):
                            valor=[int(idAlumnos[a]),idInstrumento,Notas[a].get()]
                            resultado.append(valor)
                    base=baseDatos('laForja.db')
                    materia=self.materiaElegida
                    nombreTabla=materia+"notas"+str(self.nivelMateria)
                    print("Grabando en: "+nombreTabla)
                    base.grabaNotas(nombreTabla,resultado)
                    base.close()
                    messagebox.showinfo("¡Perfecto!","¡Notas grabadas!")
                    self.updateMarcoAnidado()

                        

                except:
                    print ("¡Algo esta mal!")
            #Defino tres arrays(idalumnos,nombreAlumnos, nota(este ultimo de widgets entry))

            idAlumnos=[]
            nombreAlumnos=[]
            Notas=[]
            base=baseDatos('laForja.db')
            #materia=list(self.materia.keys())[self.combo2.current()]

            nombreTabla=str(self.materiaElegida)+"Instrumentos"+str(self.nivelMateria)
            #Obtengo de nuevo el id del instrumento:
            consulta="SELECT id FROM "+nombreTabla+" WHERE instrumento==(?)"
            valor=base.cursor.execute(consulta,(cInstrumento.get(),))
            idInstrumento=valor.fetchone()[0]
            print ("Id instrumento: "+str(idInstrumento))
            grupo=combo.get()
            print(grupo)
            trimestre=cTrimestre.current()
            print (trimestre)
            #print(self.materia.keys()[self.combo2.current()])
            marcoDesplazable=VerticalScrolledFrame(marcoNotas)
            marcoDesplazable.grid(row=0,column=0,sticky="nsew")
            alumnos=base.dameAlumnosporGrupo(grupo)
            fila=0
            for alumno in alumnos:
                idAlumnos.append(alumno[0])
                print ("Id: "+str(alumno[0])+", nombre: "+alumno[1]+", "+alumno[2])
                etAlumno=tk.Label(marcoDesplazable.interior,text=alumno[1]+", "+alumno[2])
                nombreAlumnos.append(alumno[1]+", "+alumno[2])
                etAlumno.grid(row=fila,column=0)
                nota=DoubleVar()
                etNota=tk.Entry(marcoDesplazable.interior,textvariable=nota)
                Notas.append(nota)
                etNota.grid(row=fila,column=1)
                fila=fila+1
            botonGrabar=tk.Button(marcoDesplazable.interior,text="Grabar",command=lambda:grabarNotas())
            botonGrabar.grid(row=fila,column=0)
            base.close()


                    
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoNotas=tk.Frame(self.marcoAnidado)
        marcoNotas.columnconfigure(0,weight=1)
        marcoNotas.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoNotas.grid(row=1,column=0,sticky="nsew")       

        try:
            curso=""
            
            estandares=[]
            etiquetas=[]
            label = tk.Label(marcoTitulo, text="Seleccione curso, materia y trimestre", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            combo = ttk.Combobox(marcoTitulo, state="readonly")
            base=baseDatos('laForja.db')
            grupos=base.buscaGrupos()
            combo["values"] = grupos
            base.close()
            combo.pack(side="left",padx=20)
            combo.bind("<<ComboboxSelected>>", eligeMateria)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left",padx=20)
            self.combo2.bind("<<ComboboxSelected>>", eligeTrimestre)
            cTrimestre=ttk.Combobox(marcoTitulo,state="disabled")
            cTrimestre["values"] = ["","1º Trimestre", "2º Trimestre", "3º Trimestre"]
            cTrimestre.pack(side="left",padx=20)
            cInstrumento=ttk.Combobox(marcoTitulo,state="disabled")
            cInstrumento.pack(side="left",padx=20)
            cTrimestre.bind("<<ComboboxSelected>>", dameAlumnos)
            cInstrumento.bind("<<ComboboxSelected>>", dameTablaNotas)
 
                    
        
            

        except:
            import traceback
            traceback.print_exc()
    #LA FUNCIÓN generaProgramacion0 ES LA ENCARGADA DE REPASAR LA PONDERACIÓN DE LOS CRITERIOS Y REALIZAR  UNA ASIGNACION DE TRIMESTRES
    def generaProgramacion0(self,curso,materia):
        def cambiaTrimestre(event,contenido,trimestreOriginal,nCriterio):
            #HE RECOGIDO DOS CARACTERES DE LA TABLA DE CONTENIDOS. EL PRIMERO ES UN DÍGITO SEGURO. EL SEGUNDO LO SERÁ SI
            #HAY MÁS DE DIEZ BLOQUES DE CONTENIDO
            if not(contenido[1].isdigit()):
                contenido=contenido[0]
                
            #messagebox.showinfo("informacion","Contenido afectado: "+str(contenido)+" , Trimestre original: "+str(trimestreOriginal)+", nuevo Trimestre: "+str(event.widget.current()+1))
            arrayCriterios[nCriterio][2]=event.widget.current()+1
            base=baseDatos('laForja.db')
            #print ("Comprobando: "+str(curso)+materia+str(contenido)+str(trimestreOriginal)+str(event.widget.current()+1))
            base.copiaInstrumentosaTrimestre(curso, materia, contenido,trimestreOriginal,str(event.widget.current()+1))
            base.close()
            
            #AVISO: HE MODIFICADO LA FUNCION GENERAPROGRAMACION2 PARA QUE AHORA EN CADA ESTANDAR BUSQUE LOS INSTRUMENTOS POR CONTENIDO
            #Y (ESTO ES IMPORTANTE) POR TRIMESTRE. FALTA AQUÍ BUSCAR LOS INSTRUMENTOS DEL CRITERIO CORRESPONDIENTE Y HACER UNA COPIA
            #EN LA TABLA DE INSTRUMENTOS PARA EL TRIMESTRE NUEVO
            #for a in arrayCriterios:
            #    print (a)
        def setTrimestre(contenido):
            base= baseDatos('laForja.db')
            #print ("Buscando criterios que coincidan con trimestre: "+criterio)
            n=base.buscaTrimestresporContenido(curso,materia,contenido)
            print (n)
            base.close()
            return n
        def equilibraCriterios(valor):
            #UTILIZO UNA DOUBLE VAR PARA CLONAR LA VARIABLE QUE RECOGÍA LOS VALORES DE PONDERACIÓN EN EL FORMULARIO
            valorArray=DoubleVar()
            valorArray.set(valor)
            for a in arrayCriterios:
                a[1]=valorArray
                
                
            base=baseDatos('laForja.db')
            base.asignaCriterios(curso,materia,arrayCriterios)
            base.close()
            self.generaProgramacion2(curso,materia)

        def sumaCriterios():
           
            print ("PONDERANDO:-----------------------------")
            suma=0
            sumaBien=True
            #Comprobamos que los valores son numeros decimales (y no letras)
            n=0
            for criterio in arrayValorCriterios:
                
                try:
                    valor=float(criterio.get())
                    n=n+1
                except:
                    messagebox.showinfo("Error en valores","El criterio: "+arrayEtCriterios[n].cget("text")+ "no tiene un valor asignado correcto: "+criterio.get())
                    sumaBien=False
                    break
            for criterio in arrayValorCriterios:
                n=0      
                valor=float(criterio.get())
                arrayListaPonderaciones.append(valor)
                suma=suma+valor
                n=n+1
            if (sumaBien==True):
                decido=messagebox.askyesno("Suma total","La suma total de los criterios de evaluacion alcanza un "+str(suma)+" %, ¿Quiere continuar?")
                if (decido==True):
                    base= baseDatos('laForja.db')
                    base.asignaCriterios(curso,materia,arrayCriterios)
                    base.close()
                    self.generaProgramacion2(curso,materia)


                
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0, weight=1)
        self.marcoAnidado.rowconfigure(1, weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoEstandares=tk.Frame(self.marcoAnidado,bg="blue")
        marcoTitulo=tk.Frame(self.marcoAnidado,bg="orange")
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoTitulo.columnconfigure(0,weight=1)
        marcoTitulo.columnconfigure(1,weight=1)
        marcoTitulo.columnconfigure(2,weight=1)
        marcoTitulo.columnconfigure(3,weight=1)
        etiqueta=tk.Label(marcoTitulo,text="Introduzca valor de cada estandar de evaluación en %")
        etiqueta.config(font=("Courier", 22))
        etiqueta.grid(row=0,column=0,columnspan=6,sticky="nsew")
        marcoEstandares.columnconfigure(0, weight=1)
        marcoEstandares.rowconfigure(0, weight=1)
        marcoEstandares.grid(row=1,column=0,sticky="nsew")
        marcoDesplazable=VerticalScrolledFrame(marcoEstandares)
        marcoDesplazable.pack(fill=BOTH,expand=1)
        base= baseDatos('laForja.db')
        contenidos=base.buscaContenidos(curso,materia)
        arrayCriterios=[]
        arrayListaPonderaciones=[]
        fila=1
        fila2=0
        nCriterio=0
        marcos=[]
        arrayValorCriterios=[]
        arrayEtCriterios=[]
        arrayEtTrimestres=[]
        self.Trimestre=[]
        
        for contenido in contenidos:
            fila2=0
            #print ("Comprobando contenido: "+contenido[0])
            marco=VerticalScrolledFrame(marcoDesplazable.interior)
            marcos.append(marco)
            marcos[fila-1].pack(fill=X,expand=1)
            etContenido=tk.Label(marcos[fila-1].interior,text=contenido[0],relief="raised",wraplength=200)
            etContenido.grid(row=fila-1,column=0,sticky="nsew")
            #criterios=base.buscaCriteriosporContenido(curso,materia,contenido[0])
            estandares=base.buscaEstandaresporContenido(curso,materia,contenido[0])
            fInstrumentos=tk.Frame(marcos[fila-1].interior)
            fInstrumentos.grid(row=fila-1,column=1,sticky="nsew")
            #Aquí empiezo el cambio de la nueva versión: VAMOS A PONDERAR DIRECTAMENTE ESTÁNDARES
            #EN LUGAR DE CRITERIOS (de momento, no cambio el nombre criterio por valor, pero hay
            #que entender eso).
            for estandar in estandares:
                ponderaCriterio=DoubleVar()
                etCriterio=tk.Label(fInstrumentos,text=estandar[0],relief="raised",wraplength=400,justify="left")
                arrayEtCriterios.append(etCriterio)
                arrayEtCriterios[nCriterio].grid(row=fila2, column=1,sticky="nsew")
                entValor=tk.Entry(fInstrumentos,textvariable=ponderaCriterio,relief="raised")
                arrayValorCriterios.append(entValor)
                arrayValorCriterios[nCriterio].grid(row=fila2, column=2,sticky="nsew")
                
                arrayEtTrimestres.append(ttk.Combobox(fInstrumentos,state="readonly"))
                arrayEtTrimestres[nCriterio]["values"] = ["1º Trimestre", "2º Trimestre", "3º Trimestre"]
                trimestreActual=setTrimestre(contenido[0])
                #print ("criterio: "+criterio[0]+", trimestre: "+str(trimestreActual))
                self.Trimestre.append(trimestreActual)
                arrayEtTrimestres[nCriterio].current(trimestreActual-1)
                #el valor contenido[0][7] busca el número que hay detrás de la palabra "Bloque "
                arrayEtTrimestres[nCriterio].bind("<<ComboboxSelected>>", lambda event ,contenido=contenido[0][7]+contenido[0][8],trimestreOriginal=trimestreActual,nCriterio=nCriterio: cambiaTrimestre(event,contenido,trimestreOriginal,nCriterio))
                arrayEtTrimestres[nCriterio].grid(row=fila2,column=3,sticky="nsew")
                par=[estandar[0],ponderaCriterio,self.Trimestre[nCriterio]]
                arrayCriterios.append(par)

                #print ("Trimestre: "+str(Trimestre))
                nCriterio=nCriterio+1
                fila2=fila2+1
            valor=100/len(arrayEtCriterios)
            fila=fila+1
        marcoBotones=VerticalScrolledFrame(marcoDesplazable.interior)
        marcoBotones.pack(fill=X,expand=1)
        botonSumaCriterios=tk.Button(marcoBotones.interior,text="Sumar criterios",command= lambda: sumaCriterios())
        botonSumaCriterios.grid(row=0,column=0)
        botonnoSumo=tk.Button(marcoBotones.interior,text="Autoasignar valor de ponderación a todos los criterios por igual",command= lambda a=valor: equilibraCriterios(a))
        botonnoSumo.grid(row=0,column=1)
        base.close()

    #LA FUNCIÓN generaProgramacion2 SE ENCARGA DE REPASAR TODOS LOS ESTANDARES E INSTRUMENTOS PARA REALIZAR LA ORGANIZACIÓN
    #FINAL EN LA TABLA organizacionEstandares
    def generaProgramacion2(self,curso,materia):
        
        def cambioTrimestre(event,fila1,fila2,total,nInstrumento,estandar):

            base= baseDatos('laForja.db')
            
            #Contamos el numero de filas e instrumentos hasta el momento
            print ("Fila actual: "+str(total))
            print ("Numero de instrumentos en fila: "+str(totalInstrumentosporFila[total]))
            print ("Estandar referido: "+estandar)
            consulta="SELECT id FROM estandares"+materia+" WHERE curso==(?) AND estandar==(?)"
            valor=base.cursor.execute(consulta,(curso,estandar))
            idEstandar=valor.fetchone()
            print (idEstandar)
            trimestre=event.widget.current()
            prioridad=CTrimestres[total].current()
            print ("Prioridad: "+str(prioridad))
            print (str(event.widget.current()))
            for a in range(nInstrumento,nInstrumento+totalInstrumentosporFila[total]):
                try:
                    if (vInstrumentos[a].get()==1):
                        vInstrumentos[a].set(0)
                        consulta="DELETE FROM "+materia+"organizacionEstandares"+str(curso)+" WHERE idestandar==(?)"
                        base.cursor.execute(consulta,(idEstandar))

                except sqlite3.Error as e:
                    print (e)
    
         
            base.close()
        def setTrimestre(criterio):
            base= baseDatos('laForja.db')
            n=base.buscaTrimestresporCriterio(curso,materia,criterio)
            base.close()
            return n
        def leeCB(indice,indice2,idInstrumento,estandar):
            base= baseDatos('laForja.db')

            #print ("El indice 2 es :"+str(indice2))
            #print ("El valor del combo de trimestres es: "+CPrioridades[indice2].get())
            #COMO EN ESTA VERSIÓN PRESCINDIMOS DE LOS ÍNDICES, LOS MARCO TODOS COMO 'basico'
            # if (CPrioridades[indice2].get()==""):
            #             messagebox.showinfo("¡Atención!","No es posible grabar este instrumento sin establecer la prioridad del estándar.")
            #             vInstrumentos[indice].set(0)
            # else:
            #     if (vInstrumentos[indice].get()==1):
            #         print ("Grabando el instrumento "+str(idInstrumento)+" con el trimestre "+str(CTrimestres[indice2].current()+1)+" para el estandar "+str(estandar))
            #         base.asignaInstrumentoEstandar(curso,materia,CPrioridades[indice2].current(),estandar,idInstrumento,CTrimestres[indice2].current()+1,"grabar")
            #     else:
            #         print ("Borrando el instrumento "+str(idInstrumento)+" con el trimestre "+str(CTrimestres[indice2].current()+1)+" para el estandar "+str(estandar))
            #         base.asignaInstrumentoEstandar(curso,materia,CPrioridades[indice2].current()+1,estandar,idInstrumento,CTrimestres[indice2].current()+1,"borrar")
            # base.close()
            if (vInstrumentos[indice].get() == 1):

                print ("Grabando el instrumento "+str(idInstrumento)+" con el trimestre "+str(CTrimestres[indice2].current()+1)+" para el estandar "+str(estandar))
                base.asignaInstrumentoEstandar(curso,materia,'basico',estandar,idInstrumento,CTrimestres[indice2].current()+1,"grabar")
            else:
                print ("Borrando el instrumento "+str(idInstrumento)+" con el trimestre "+str(CTrimestres[indice2].current()+1)+" para el estandar "+str(estandar))
                base.asignaInstrumentoEstandar(curso,materia,'basico',estandar,idInstrumento,CTrimestres[indice2].current()+1,"borrar")
            base.close()
        def acabaProgramacion():
            self.updateMarcoAnidado()
            messagebox.showinfo("¡Terminado!","Acabas de grabar la Programación Didáctica")
          

        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0, weight=1)
        self.marcoAnidado.rowconfigure(1, weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoEstandares=tk.Frame(self.marcoAnidado,bg="blue")
        marcoTitulo=tk.Frame(self.marcoAnidado,bg="orange")
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoTitulo.columnconfigure(0,weight=1)
        marcoTitulo.columnconfigure(1,weight=1)
        marcoTitulo.columnconfigure(2,weight=4)
        marcoTitulo.columnconfigure(3,weight=1)        
        marcoEstandares.columnconfigure(0, weight=1)
        marcoEstandares.rowconfigure(0, weight=1)
        marcoEstandares.grid(row=1,column=0,sticky="nsew")
        messagebox.showinfo("¡Aviso!","Consigne la relación final de estándares e instrumentos, trimestre a trimestre (NOTA: DEBE MARCAR POR LO MENOS UN INSTRUMENTO EN CADA ESTÁNDAR. PUEDE REALIZAR MODIFICACIONES POSTERIORMENTE)")
        #et1=tk.Label(marcoEstandares,text="Consigne la relación final de estándares e instrumentos, trimestre a trimestre (NOTA: DEBE MARCAR POR LO MENOS UN INSTRUMENTO EN CADA ESTÁNDAR. PUEDE REALIZAR MODIFICACIONES POSTERIORMENTE)",wraplength=400,relief="raised",font=LARGE_FONT)
        #et1.grid(row=0,column=0,sticky="nsew")
        #et2=tk.Label(marcoEstandares,text="marco estandares")
        #et2.grid(row=0,column=0)
        etBloque=tk.Label(marcoTitulo,text="Bloque")
        etBloque.grid(row=0,column=0,sticky="nsew")
        etEstandar = tk.Label(marcoTitulo, text="Estándar")
        etEstandar.grid(row=0, column=1, sticky="nsew")
        etTrimestre=tk.Label(marcoTitulo,text="Trimestre" )
        etTrimestre.grid(row=0,column=2,sticky="nsew")

        #etPrioridad=tk.Label(marcoTitulo,text="Prioridad" )
        #etPrioridad.grid(row=0,column=3,sticky="nsew")
        marcoDesplazable=VerticalScrolledFrame(marcoEstandares)
        marcoDesplazable.pack(fill=BOTH,expand=1)
        base= baseDatos('laForja.db')
        contenidos=base.buscaContenidos(curso,materia)
        marcos=[]
        fila1=0
        vInstrumentos=[]
        cbInstrumentos=[]
        nInstrumentos=0
        CPrioridades=[]
        CTrimestres=[]
        fPrioridades=0
        totalInstrumentosporFila=[]
        for c in contenidos:
            print ("Comprobando contenido: "+c[0])
        for contenido in contenidos:
            print (contenido[0])
            fila2=0
            marco=VerticalScrolledFrame(marcoDesplazable.interior)
            marcos.append(marco)
            marcos[fila1].pack(fill=BOTH,expand=1)
            #print ("Buscando estandares, curso:"+curso+", materia: "+materia)
            estandares=base.buscaEstandaresporContenido0(curso,materia,contenido[0])
            #print (estandares)
            marco.instrumentos=[]
            lEstandares=[]
            lEstandares.append(estandares[0])
            #NO SÉ POR QUÉ, PERO LOS ESTÁNDARES SE ME GRABAN DOS VECES. LO ARREGLO ASÍ:
            for e in estandares:
                if not (e in lEstandares):
                    lEstandares.append(e)
            #print("Hasta aqui vamos bien: "+str(lEstandares))
            for estandar in lEstandares:
                #print ("Estandar: "+str(estandar))
                etContenido=tk.Label(marcos[fila1].interior,text=contenido[0],relief="raised",wraplength=100,justify="center")
                etContenido.grid(row=fila2,column=0,sticky="nsew")
                etEstandar=tk.Label(marcos[fila1].interior,text=estandar[4],anchor="e", relief="raised",wraplength=350,justify="left")
                etEstandar.grid(row=fila2,column=1,sticky="nsew")
                #INCLUIR TRIMESTRE
                print("Buscando trimestre para estandar: "+str(estandar[3]))
                trimestreActual=setTrimestre(estandar[4])
                instrumentos=base.buscaInstrumentosporContenido(curso,materia,contenido[0],trimestreActual)

                cTrimestre=ttk.Combobox(marcos[fila1].interior,state="readonly")
                cTrimestre["values"] = ["1º Trimestre", "2º Trimestre", "3º Trimestre"]
                cTrimestre.current(trimestreActual-1)
                cTrimestre.bind("<<ComboboxSelected>>", lambda event,fila1=fila1, fila2=fila2,total=fPrioridades,nInstrumento=nInstrumentos,estandar=estandares[fila2][4]: cambioTrimestre(event,fila1,fila2,total,nInstrumento,estandar))                
                CTrimestres.append(cTrimestre)
                CTrimestres[fPrioridades].grid(row=fila2,column=2)

                fInstrumentos=tk.Frame(marcos[fila1].interior,bd=1,relief="raised")
                fInstrumentos.grid(row=fila2,column=3,sticky="nsew")
                #etPrueba=tk.Label(fInstrumentos,text="Etiqueta de prueba")
                #etPrueba.grid(row=0,column=0)
                fila3=0
                #cPrioridad=ttk.Combobox(marcos[fila1].interior,state="readonly")
                #cPrioridad["values"] = ["", "Básico", "Intermedio", "Avanzado"]
                #CPrioridades.append(cPrioridad)
                #CPrioridades[fPrioridades].grid(row=fila2,column=4)
                instrumentosenFilaActual=0
                for instrumento in instrumentos:
                    valor=BooleanVar()
                    vInstrumentos.append(valor)
                    cbInstrumento=tk.Checkbutton(fInstrumentos, variable=vInstrumentos[nInstrumentos],text=instrumento[2], command=lambda indice=nInstrumentos,indice2=fPrioridades, idInstrumento=instrumento[0],estandar=estandar[0]:leeCB(indice,indice2,idInstrumento,estandar))
                    cbInstrumentos.append(cbInstrumento)
                    cbInstrumentos[nInstrumentos].grid(row=fila3,column=0,sticky="nsew")
                    marco.instrumentos.append(cbInstrumento)
                    #etInstrumento=tk.Label(fInstrumentos,text=instrumento[2],wraplength=100)
                    #etInstrumento.grid(row=fila3,column=0,sticky="nsew")
                    nInstrumentos=nInstrumentos+1
                    fila3=fila3+1
                    instrumentosenFilaActual=instrumentosenFilaActual+1
                #print ("Instrumentos en fila: "+str(fila1)+", "+str(fila2)+": "+str(instrumentosenFilaActual))
                totalInstrumentosporFila.append(instrumentosenFilaActual)
                #fEst=fEst+1
                fPrioridades=fPrioridades+1
                fila2=fila2+1
            fila1=fila1+1
        botonFinal=tk.Button(marcoEstandares,text="Finalizar",command=lambda:acabaProgramacion())
        botonFinal.pack()
        base.close()
        
    def generaProgramacion(self):
        messagebox.showinfo("¡Atención!","Si realizas la programación de una materia y curso anteriores, perderías los resultados ya grabados...")
        self.updateMarcoAnidado()
        self.marcoAnidado.rowconfigure(0,weight=1)
        self.marcoAnidado.rowconfigure(1,weight=5)
        self.marcoAnidado.columnconfigure(0,weight=1)
        marcoEstandares=tk.Frame(self.marcoAnidado)
        marcoEstandares.columnconfigure(0,weight=1)
        marcoEstandares.rowconfigure(0,weight=1)
        marcoTitulo=tk.Frame(self.marcoAnidado)
        marcoTitulo.grid(row=0,column=0,sticky="nsew")
        marcoEstandares.grid(row=1,column=0,sticky="nsew")
        def eligeCurso(event):
            #print("Nuevo elemento seleccionado:", self.combo.get())
            #print("Numero de orden: ",self.combo.current())
            if (self.combo.current()!=0):
                self.combo2["state"]="readonly"
                base= baseDatos('laForja.db')
                self.curso=self.combo.current()
                self.materia=base.buscaMateriasCursonuevaProgramacion(self.curso)
                self.combo2["values"]=sorted(list(self.materia.values()))
                base.close()
                
        def eligeMateria(event):
            marcoDesplazable=VerticalScrolledFrame(marcoEstandares)
            #marcoDesplazable.pack(fill=BOTH,expand=1)
            marcoDesplazable.grid(row=0,column=0,sticky="nsew")
            fila=4
            eleccion= self.combo2.current()
            print("Eleccion: "+str(eleccion))
            base= baseDatos('laForja.db')
            seleccion = self.materia
            materia= list(seleccion.keys())[list(seleccion.values()).index(self.combo2.get())]
            print("Materia: "+str(materia))
            #materia=list(self.materia.keys())[eleccion]
            curso=str(self.combo2.current())
            nombreTabla=materia+"Instrumentos"+curso
            base.creaTablaInstrumentos(self.combo.current(),str(materia))
            estandares=base.buscaContenidos(self.combo.current(),str(materia))
            nEstandar=0  
            etiquetas=[]
            lbTrimestre=[]
            lbNInstrumentos=[]
            self.contenidosGrabados=0
            marcos=[]
            

            def borraProgramacion1(curso,materia):
                print ("¡grabado!")
                print ("Procedo a borrar marco...")
                
            def rellenaInstrumentos(event,numero):
                entradas=[]

                #messagebox.showinfo("Contenido: ",estandares[numero][0])
                def grabaInstrumentos(contenidosGrabados):
                    self.contenidosGrabados=self.contenidosGrabados+1
                    base= baseDatos('laForja.db')
                    #print (materia)
                    #print ("Curso: "+str(self.curso))
                    #c=base.grabaInstrumentos(materia,self.curso,estandares[numero][0])
                    trimestre=lbTrimestre[numero].get()

                    for instrumento in range(numeroI):
                        c=base.grabaInstrumentos(materia,str(self.curso),estandares[numero][0],entradas[instrumento].get(),trimestre[0])
                    #base.close()
                    #print ("Presentando elementos encontrados en la consulta: ")
                    #print (len(c))
                    #for a in c:
                    #    print (a[0])
                    #messagebox.showinfo("Contenido: ","a")
                    base.close()
                    #for instrumento in range(numeroI):
                        #messagebox.showinfo("Instrumento: ",entradas[instrumento].get())
                    for  child in (marcos[numero].interior.winfo_children()):
                        child['state'] = DISABLED
                    if (self.contenidosGrabados==nEstandar):
                        
                        boton=tk.Button(marcos[numero].interior, text="Finalizar", command= lambda  a=self.curso, b=materia: self.generaProgramacion0(a,b))
                        boton.grid(row=50,column=0,sticky="nsew")
                        #boton.config(text=str(self.contenidosGrabados))

                if (lbTrimestre[numero].get()==""):
                    lbNInstrumentos[numero].current(0)
                    messagebox.showinfo("Advertencia","Primero debes introducir el trimestre en que empezarás a impartir este bloque de contenidos")
                    return
                Etiqueta=tk.Label(marcos[numero].interior,text="Nombre del instrumento: ")
                Etiqueta.grid(row=3,column=1)                
                numeroI=int(lbNInstrumentos[numero].get())
                fila=4
                trimestre=lbTrimestre[numero].get()
                for n in range(0,numeroI):
                    text="Bloque"+str(numero+1)+"Examen"+str(n+1)
                    entrada=tk.Entry(marcos[numero].interior)
                    entrada.insert(0,text)
                    entradas.append(entrada)
                    entradas[n].grid(row=fila,column=1,sticky="nsew")
                    fila=fila+1
                    
                botonGrabar=tk.Button(marcos[numero].interior,text="Grabar",command=lambda c=self.contenidosGrabados : grabaInstrumentos(c))
                botonGrabar.grid(row=fila,column=1)
            for n in estandares:
                nExamenes=1
                marco=VerticalScrolledFrame(marcoDesplazable.interior)
                marcos.append(marco)
                #marcos[nEstandar].grid(row=fila,column=0,sticky="ew")
                marcos[nEstandar].pack(fill=BOTH,expand=1)
                etContenido=tk.Label(marcos[nEstandar].interior,text=n[0], relief="raised",height="1")
                etContenido.grid(row=0,column=0,columnspan="2")
                etContenido2=tk.Label(marcos[nEstandar].interior,text="Trimestre: " ,height="1")
                etContenido2.grid(row=1,column=0)                
                #etCriterio=tkst.ScrolledText(marcos[nEstandar], wrap=tk.WORD)
                #etCriterio.insert("insert", n[3])
                #etCriterio.config(state="disabled")
                #etCriterio.grid(row=0,column=1)
                lbTrimestre.append(ttk.Combobox(marcos[nEstandar].interior,state="readonly"))
                lbTrimestre[nEstandar]["values"] = [" ","1º Trimestre", "2º Trimestre", "3º Trimestre"]
                lbTrimestre[nEstandar].grid(row=1,column=1)
                etInstrumentos=tk.Label(marcos[nEstandar].interior,text="Nº de instrumentos: " ,height="1")
                etInstrumentos.grid(row=2,column=0)   
                lbNInstrumentos.append(ttk.Combobox(marcos[nEstandar].interior,state="readonly"))
                lbNInstrumentos[nEstandar]["values"] = [" ","1","2","3","4","5","6","7","8","9"]
                lbNInstrumentos[nEstandar].grid(row=2,column=1)
                lbNInstrumentos[nEstandar].bind("<<ComboboxSelected>>", lambda event, x=nEstandar : rellenaInstrumentos(event,x))
                nEstandar=nEstandar+1
                fila=fila+1

            base.close()

        try:
            curso=""
            materia={}
            estandares=[]
            etiquetas=[]


            label = tk.Label(marcoTitulo, text="Generar nueva Programación Didáctica", font=LARGE_FONT)
            label.pack(side="top",anchor="n")
            self.combo = ttk.Combobox(marcoTitulo, state="readonly")
            self.combo["values"] = [" ","1º ESO", "2º ESO", "3º ESO", "4º ESO", "1º Bachillerato", "2º Bachillerato"]
            self.combo.pack(side="left",padx=300)
            self.combo.bind("<<ComboboxSelected>>", eligeCurso)
            self.combo2=ttk.Combobox(marcoTitulo,state="disabled")
            self.combo2.pack(side="left")
            self.combo2.bind("<<ComboboxSelected>>", eligeMateria)
            #boton=tk.Button(marcoTitulo, text="Fase 2", command= lambda: self.generaProgramacion2(2,"matematicas"))
            #boton.pack(side="bottom")
            #boton2=tk.Button(marcoTitulo, text="Fase 3", command= lambda: self.generaProgramacion0(2,"matematicas"))
            #boton2.pack(side="bottom")
                        
            
                

        except:
            import traceback
            traceback.print_exc()

class configuracion:

    
    def __init__(self, master):
        self.master = master
        self.master.title("LaForja v2.00")
        self.master.columnconfigure(0,weight=1)
        self.master.rowconfigure(0,weight=1)
        self.master.rowconfigure(1,weight=7)
        self.marcoPrincipal=tk.Frame(self.master)
        self.marcoPrincipal.grid(row=0,column=0)
        self.label = tk.Label(self.marcoPrincipal, text="No hay base de datos predefinida. Por favor, introduzca el archivo datMatriculas.csv", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        self.botonNavegar=tk.Button(self.marcoPrincipal, text="Buscar archivo",command=self.buscarArchivo)
        self.botonNavegar.pack()
        self.botonVolver=tk.Button(self.marcoPrincipal, text="Pagina principal",command=lambda: self.devuelveControl())


        
    def buscarArchivo(self):
        archivo = filedialog.askopenfilename(filetypes = (("Archivos csv", "*.csv"),("All files", "*.*") ))
        if archivo: 
            try: 
                messagebox.showinfo("¡Estupendo!","El archivo se cargó correctamente. Pasamos a generar base de datos.")
                print ("Creando base de datos...")
                base= baseDatos('laForja.db')
                print ("¡Hecho!")
                print ("Creando tablas de matricula...")
                base.crea_matriculas()
                print ("¡Hecho!")
                print ("Rellenando tabla de matrículas...")
                base.rellena_matriculas(archivo)
                print ("¡Hecho!")
                print ("Generando el resto de tablas...")
                base.crea_tablas()
                print ("¡Hecho!")
                print ("Pasamos a la página principal")                
                base.close()
                try:
                    print ("hola")
                    
                    self.botonNavegar.destroy()
                    self.label['text']="¡Todo funcionó!"
                    self.botonVolver.pack()
                    print ("¿funciono?")
                except:
                    import traceback
                    traceback.print_exc()
                    self.widget.quit()
            except: 
                messagebox.Message("OOOPSSS... Parece que algo fallo, wey...")
    def devuelveControl(self):
        self.master.destroy()
        nucleo=tk.Tk()        
        miVentana=ventana(nucleo)
        nucleo.mainloop()    
          

