# -*- coding:utf-8 -*-
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

import sqlite3
import csv
import time
import io
import os
import operator
#La clase está inspirada en https://gist.githubusercontent.com/goldsborough
class baseDatos:
    def __init__(self, name=None):

        self.conn = None
        self.cursor = None
        if name:
            self.open(name)

    def open(self,name):

        try:
            self.conn = sqlite3.connect(name);
            self.conn.text_factory = lambda x: str(x, 'utf-8', 'ignore')

            self.cursor = self.conn.cursor()


        except sqlite3.Error as e:
            print("Error connecting to database!")

    def close(self):

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()


    def __enter__(self):

        return self

    def __exit__(self,exc_type,exc_value,traceback):

        self.close()


    def crea_matriculas(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS 'matriculas' ('alumno' varchar(6)  ,'apellidos' text ,'nombre' text  ,'matricula' varchar(8)  ,'etapa' varchar(4)  ,'anno' varchar(4)  ,'tipo' varchar(2)  ,'estudios' text  ,'grupo' text  ,'repetidor' text  ,'fechamatricula' text  ,'centro' varchar(10)  ,'procedencia' varchar(10)  ,'estadomatricula' text  ,'fecharesolucionmatricula' text  ,'numexpcentro' varchar(5) )")
        except sqlite3.Error as e:
            print (e)
    #crea_matriculas()
    def borra_matriculas(self,archivo):
        self.cursor.execute("DELETE FROM matriculas")
        self.cursor.execute("VACUUM")

    def rellena_matriculas(self, archivo):

        print(archivo)
        print("intentando...")
        try:
            f=open(archivo,'r')
            #next (f,None)
            print(f)
            reader=csv.reader(f, delimiter=',')
            for row in reader:
                if row:
                    print('probando')
                    self.cursor.execute("INSERT INTO matriculas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
            f.close()
        except:
            print("Error abriendo archivo")
    def rellena_estandares_tecnologia(self,archivo):
        f=open(archivo,'r')
        next (f,None)
        reader=csv.reader(f,delimiter=',')

        for row in reader:
            if row:
                self.cursor.execute("INSERT INTO estandarestecnologia VALUES (?,?,?,?,?,?)",row)
        f.close()
    def dameAlumno(self,matricula):
        self.cursor.execute("SELECT * FROM MATRICULAS WHERE alumno=?",matricula)


    def crea_tablas(self):
        #Generamos tablas de estándares
        try:

            cadena=["lengua","tecnologia","matacademicas","mataplicadas","matematicas","robotica","tdic","tecnologia","cclasica","geografiahistoria"]
            for row in cadena:
                print("Materia: "+row)
                consulta="CREATE TABLE IF NOT EXISTS estandares"+row+" ('id' int(5) NOT NULL,'curso' varchar(5)  ,'bloque' text  ,'criterio' text  ,'estandar' text  ,'prioridad' varchar(5))"
                self.cursor.execute(consulta)
        except sqlite3.Error as e:
            print ("Error generando tablas de estandares: ")
            print (e)
        #Rellenamos tablas de estándares
        try:
            cur_path = os.getcwd()+"/estandares/"
            #print (cur_path)
            cadena=["lengua","tecnologia","cclasica","mataplicadas","matematicas","robotica","tdic","tecnologia","matacademicas","geografiahistoria"]
            for row in cadena:
                #print(row)
                try:
                    nombreTabla="estandares"+row
                    print ("Rellenando estandares de: "+nombreTabla)
                    archivo=cur_path+nombreTabla+".csv"
                    
                    print (archivo)

                    f=open(archivo,'r')
                    if (f):
                        print ("Archivo localizado")
                    else:
                        print ("Error localizando archivo")
                    print ("Archivo "+archivo+" abierto")
                    next(f,None)
                    reader=csv.reader(f,delimiter=',')
                   # print (reader)
                    for estandar in reader:
                        if estandar:
                            #print ("estandar encontrado")
                            #print (estandar)
                            consulta="INSERT INTO "+ nombreTabla+" VALUES (?,?,?,?,?,?)"
                            #print (consulta,(estandar))
                            try:
                                self.cursor.execute(consulta,(estandar))
                            except sqlite3.Error as e:
                                print ("Error rellenando estandares en tabla:"+nombreTabla)
                                print (e)

                    self.conn.commit()
                    f.close()
                except error as e:
                    print (e)
        except sqlite3.Error as e:
            print ("Error rellenando tablas de estandares: ")
            print ("Tabla: "+nombreTabla)
            print ("Consulta: "+consulta)
            print ("Fila: "+row)
            print (e)
        #Generamos y rellenamos tabla de competencias generales
        try:
            creaConsultas="CREATE TABLE IF NOT EXISTS `competencias` (`id` INTEGER PRIMARY KEY,`competencia` text ,`codigo` varchar(5))"
            self.cursor.execute(creaConsultas)
        except sqlite3.Error as e:
            print ("Error creando consultas:")
            print (e)
        try:
            rellenaConsultas="INSERT INTO `competencias` (`id`, `competencia`, `codigo`) VALUES(1, 'Competencia Matemática', 'CM'),(2, 'Competencia Lingüística', 'CL'),(3, 'Competencia Digital', 'CD'),(4, 'Sentido de la Iniciativa y Espíritu Emprendedor', 'SI'),(5, 'Conciencia y Expresiones Culturales', 'CEC'),(6, 'Competencias Sociales y Cívicas', 'CSC'),(7, 'Aprender a Aprender', 'AA')"
            self.cursor.execute(rellenaConsultas)
        except sqlite3.Error as e:
            print ("Error rellenando consultas: ")
            print (e)
#Generamos tablas de relación entre competencias y estándares
                    #Generamos tablas de estándares
        try:

            cadena=["lengua","tecnologia","matacademicas","mataplicadas","matematicas","robotica","tdic","tecnologia","cclasica","geografiahistoria"]
            for row in cadena:
                consulta="CREATE TABLE IF NOT EXISTS competencias"+row+"(`id` INTEGER PRIMARY KEY,`curso` int(2) NOT NULL,`contenido` int(3) NOT NULL,`competencia` int(3) NOT NULL)"
                self.cursor.execute(consulta)
        except sqlite3.Error as e:
            print ("Error generando tablas de relación competencias/estandares: ")
            print (e)
#Generamos tabla evaluaciongeneral:
        try:
            consulta="CREATE TABLE IF NOT EXISTS `evaluaciongeneral` (`id` INTEGER NOT NULL,`grupo` varchar(15)    ,`profesor` varchar(20)    ,`materia` varchar(30)    ,`fecha` text ,`conocenormas` varchar(15)    ,`respetanormas` varchar(15)    ,`homogeneo` varchar(15)    ,`nivelacademico` varchar(15)    ,`climaenaula` varchar(15)    ,`actitudalumnoprofesor` varchar(15)    ,`actitudentrealumnos` varchar(15)    ,`otros` varchar(30)  ) "
            self.cursor.execute(consulta)

        except sqlite3.Error as e:
            print ("Error generando tabla evaluaciongeneral: ")
            print (e)
#Generamos tabla materias:
        try:
            consulta="CREATE TABLE IF NOT EXISTS `materias` (`id` INTEGER PRIMARY KEY,`materia` text ,`codigo` text ,`curso` int(3) NOT NULL) "
            self.cursor.execute(consulta)

        except sqlite3.Error as e:
            print ("Error generando tabla de materias: ")
            print (e)
#Rellenamos tabla materias:
        try:
            consulta="INSERT INTO `materias` (`id`, `materia`, `codigo`, `curso`) VALUES(1, 'Lengua Castellana y Literatura', 'lengua', 1),(2, 'Matemáticas', 'matematicas', 1),(3, 'Geografía e Historia', 'geografiahistoria', 1),(4, 'Biología y Geología', 'biogeo', 1),(5, 'Inglés', 'ingles', 1),(6, 'Educación Física', 'edfisica', 1),(7, 'Educación Plástica, Visual y Artística', 'plastica', 1),(8, 'Música', 'musica', 1),(9, 'Valores éticos', 'valores', 1),(10, 'Religión Católica', 'religion', 1),(11, 'Francés', 'frances', 1),(12, 'Inic. Activ. Emprend. Y Empres.', 'emprendedores', 1),(13, 'Tecnología creativa', 'teccreativa', 1),(14, 'Ámbito Lingüístico y Social', 'ambling', 2),(15, 'Ámbito Científico y Matemáticdo', 'ambcient', 2),(16, 'Ámbito Inglés', 'ambingles', 2),(17, 'Lengua Castellana y Literatura', 'lengua', 2),(18, 'Matemáticas', 'matematicas', 2),(19, 'Geografía e Historia', 'geografiahistoria', 2),(20, 'Física y Química', 'fisquim', 2),(21, 'Inglés', 'ingles', 2),(22, 'Educación Física', 'edfisica', 2),(23, 'Educación Plástica, Visual y Artística', 'plastica', 2),(24, 'Música', 'musica', 2),(25, 'Valores éticos', 'valores', 2),(26, 'Religión Católica', 'religion', 2),(27, 'Francés', 'frances', 2),(28, 'Inic. Activ. Emprend. Y Empres.', 'emprendedores', 2),(29, 'Tecnología ', 'tecnologia', 2),(30, 'Cultura Clásica', 'cclasica', 2),(31, 'Taller de Arte y Expresión', 'tallerarte', 2),(32, 'Ámbito Lingüístico y Social', 'ambling', 3),(33, 'Ámbito Científico y Matemáticdo', 'ambcient', 3),(34, 'Ámbito Inglés', 'ambingles', 3),(35, 'Lengua Castellana y Literatura', 'lengua', 3),(36, 'Matemáticas Académicas', 'matacademicas', 3),(37, 'Matemáticas Aplicadas', 'mataplicadas', 3),(38, 'Geografía e Historia', 'geografiahistoria', 3),(39, 'Biología y Geología', 'biogeo', 3),(40, 'Física y Química', 'fisquim', 3),(41, 'Inglés', 'ingles', 3),(42, 'Educación Física', 'edfisica', 3),(43, 'Música Activa y movimiento', 'musica', 3),(44, 'Valores éticos', 'valores', 3),(45, 'Religión Católica', 'religion', 3),(46, 'Francés', 'frances', 3),(47, 'Tecnología ', 'tecnologia', 3),(48, 'Cultura Clásica', 'cclasica', 3),(49, 'Lengua Castellana y Literatura', 'lengua', 4),(50, 'Matemáticas Académicas', 'matacademicas', 4),(51, 'Matemáticas Aplicadas', 'mataplicadas', 4),(52, 'Inglés', 'ingles', 4),(53, 'Geografía e Historia', 'geografiahistoria', 4),(54, 'Biología y Geología', 'biogeo', 4),(55, 'Física y Química', 'fisquim', 4),(56, 'Economía', 'economia', 4),(57, 'Latín', 'latin', 4),(58, 'Tecnología ', 'tecnologia', 4),(59, 'Ciencias aplicadas a la actividad empresarial', 'empresariales', 4),(60, 'Inic. Activ. Emprend. Y Empres.', 'emprendedores', 4),(61, 'Educación Física', 'edfisica', 4),(62, 'Religión Católica', 'religion', 4),(63, 'Valores éticos', 'valores', 4),(64, 'Filosofía', 'filosofia', 4),(65, 'Tecnologías de la Información', 'tdic', 4),(66, 'Francés', 'frances', 4),(67, 'Cultura Científica', 'ccientifica', 4),(68, 'Cultura Clásica', 'cclasica', 4),(69, 'Educación Plástica, Visual y Artística', 'plastica', 4),(70, 'Música', 'musica', 4),(71, 'Artes escénicas y danza', 'danza', 4),(72, 'Tecnología Robótica', 'robotica', 4),(73, 'Filosofía', 'filosofia', 5),(74, 'Lengua Castellana y Literatura', 'lengua', 5),(75, 'Matemáticas', 'matematicas', 5),(76, 'Física y Química', 'fisquim', 5),(77, 'Educación Física', 'edfisica', 5),(78, 'Inglés', 'ingles', 5),(79, 'Dibujo Técnico I', 'dibtecnico', 5),(80, 'Biología y Geología', 'biogeo', 5),(81, 'Tecnología Industrial I', 'tecnologia', 5),(82, 'Dibujo Artístico I', 'plastica', 5),(83, 'Anatomía Aplicada', 'anatomia', 5),(84, 'Francés', 'frances', 5),(85, 'Cultura Científica', 'ccientifica', 5),(86, 'Tecnologías de la Información', 'tdic', 5),(87, 'Religión Católica', 'religion', 5),(88, 'Historia del Mundo Contemporáneo', 'geografiahistoria', 5),(89, 'Latín I', 'latin', 5),(90, 'Mat. Aplic. Ciencias Soc. I', 'matsociales', 5),(91, 'Economía', 'economia', 5),(92, 'Literatura Universal', 'literatura', 5),(93, 'Griego I', 'griego', 5),(94, 'Lenguaje y práctica musical', 'musica', 5),(95, 'Historia de España', 'geografiahistoria', 6),(96, 'Lengua Castellana y Literatura', 'lengua', 6),(97, 'Matemáticas II', 'matematicas', 6),(98, 'Inglés', 'ingles', 6),(99, 'Física  ', 'fisquim', 6),(100, 'Biología  ', 'biogeo', 6),(101, 'Dibujo Técnico II', 'dibtecnico', 6),(102, 'Química', 'quimica', 6),(103, 'Geología', 'biogeo', 6),(104, 'Tecnología Industrial II', 'tecnologia', 6),(105, 'Francés', 'frances', 6),(106, 'Ciencias de la Tierra y del M.A.', 'ctierra', 6),(107, 'Historia de la Filosofía', 'filosofia', 6),(108, 'Psicología', 'psicologia', 6),(109, 'Fundamentos de Administración', 'fadmin', 6),(110, 'Imagen y Sonido', 'imagen', 6),(111, 'Tecnologías de la Información', 'tdic', 6),(112, 'Historia de la Música y la Danza', 'musica', 6),(113, 'Latín II', 'latin', 6),(114, 'Mat. Aplic. Ciencias Soc. II', 'matsociales', 6),(115, 'Economía de la empresa', 'economia', 6),(116, 'Historia del Arte', 'historiarte', 6),(117, 'Griego II', 'griego', 6),(118, 'Geografía  ', 'geografiaoptativa', 6); "
            self.cursor.execute(consulta)

        except sqlite3.Error as e:
            print ("Error rellenando tabla de materias: ")
            print (e)
#Generamos tabla prioridades:
        try:
            consulta="CREATE TABLE `prioridades` (`prioridad` INTEGER PRIMARY KEY,`peso` int(3) NOT NULL)"
            self.cursor.execute(consulta)

        except sqlite3.Error as e:
            print ("Error generando tabla de prioridades: ")
            print (e)
#Rellenamos tabla prioridades:
        try:
            consulta="INSERT INTO `prioridades` (`prioridad`, `peso`) VALUES(1, 65),(2, 25),(3, 10)"
            self.cursor.execute(consulta)

        except sqlite3.Error as e:
            print ("Error generando tabla de prioridades: ")
            print (e)            
    def buscaMateriasCurso(self,curso):
        try:
            consulta="SELECT materia,codigo FROM materias WHERE curso=(?) ORDER BY materia"
            #print("Buscando materias para el curso: ")
            #print(curso)
            valor=self.cursor.execute(consulta,str(curso))
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            #print("A ordenar: ")
            result={}

            for row in valor.fetchall():

                result[row[1]]=row[0]
            #print(result)

            return result
        except sqlite3.Error as e:
            print (e)
    def buscaGrupos(self):
        try:
            consulta="SELECT DISTINCT grupo FROM matriculas ORDER BY grupo"
            valor=self.cursor.execute(consulta)
            result=[]
            for row in valor.fetchall():
                result.append(row[0])
            return result
            result=valor.fetchall()

            return result
        except sqlite3.Error as e:
            print (e)        
    def buscaContenidos(self,curso,materia):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT DISTINCT bloque FROM "+nombreTabla+" WHERE curso=(?)"
            valor=self.cursor.execute(consulta,str(curso))
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print (e)
    def creaTablaInstrumentos(self,curso,materia):
        try:
            #Borrar y recrear tabla de organizacion de estandares
            nombreTablaInstrumentos=materia+"organizacionEstandares"+str(curso)
            sql="DROP TABLE IF EXISTS "+nombreTablaInstrumentos
            print ("Borrando "+nombreTablaInstrumentos)
            self.cursor.execute(sql)
            query="CREATE TABLE IF NOT EXISTS "+nombreTablaInstrumentos+" (`id` INTEGER PRIMARY KEY,`prioridad` int(2) NOT NULL,`idestandar` varchar(10),`idinstrumento` varchar(10) ,`trimestre` int(2) NOT NULL)"
            print ("Creando de nuevo "+nombreTablaInstrumentos)
            valorInstrumento=self.cursor.execute(query)
            #Borrar y recrear tabla de notas para instrumentos de evaluacion
            nombreTabla=materia+"notas"+str(curso)
            sql="DROP TABLE IF EXISTS "+nombreTabla
            print ("Borrando "+nombreTabla)
            self.cursor.execute(sql)
            consulta="CREATE TABLE IF NOT EXISTS "+nombreTabla+" (`id` INTEGER PRIMARY KEY,`alumno` varchar(10) NOT NULL,`instrumento` varchar(10),`nota` float)"
            print ("Creando "+nombreTabla)
            valor=self.cursor.execute(consulta)            
            #Borrar y recrear tabla de instrumentos de evaluacion para materia y curso
            nombreTabla=materia+"Instrumentos"+str(curso)
            sql="DROP TABLE IF EXISTS "+nombreTabla
            print ("Borrando "+nombreTabla)
            self.cursor.execute(sql)
            consulta="CREATE TABLE IF NOT EXISTS "+nombreTabla+" (`id` INTEGER PRIMARY KEY, `contenido` int(3) NOT NULL,`instrumento` varchar(100),`trimestre` int(2) NOT NULL)"
            print ("Creando "+nombreTabla)
            valor=self.cursor.execute(consulta)
            

            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print (e)
    def grabaInstrumentos(self,materia,curso, contenido,instrumento,trimestre):
        try:

            Tabla="estandares"+materia
            #print ("Tabla: "+Tabla)
            consulta="SELECT *  FROM "+Tabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso)))
            estandarbase=valor.fetchone()
            nCurso=str(estandarbase[0])[0]
            nBloque=str(estandarbase[0])[1]
            #print ("Bloque de contenidos: "+curso)
            Tabla2=materia+"Instrumentos"+nCurso
            #print ("Tabla a insertar: "+Tabla2)
            consulta2="INSERT INTO "+Tabla2+"(contenido,instrumento,trimestre) VALUES (?,?,?)"
            valor2=self.cursor.execute(consulta2,(nBloque,instrumento,trimestre))
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print ("Error grabando instrumentos...")
            print (e)

    def buscaEstandaresporContenido0(self,curso,materia,contenido):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT * FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso),))
            resultado = []
            #for row in valor.fetchall():
            #    resultado.append(row)
            #print ("Comprobando estandares en origen de base de datos")
            #for r in resultado:
                #print (r[0])
            #print ("Fin de la comprobacion")
            result=valor.fetchall()
            print("resultado: "+str(result))
            return result
        except sqlite3.Error as e:
            print (e)
            
    def buscaCriteriosporContenido(self,curso,materia,contenido):
        try:
            nombreTabla="estandares"+materia
            print ("Buscando criterios: "+nombreTabla)
            
            consulta="SELECT DISTINCT criterio FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso)))
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print (e)

    def buscaEstandaresporContenido(self, curso, materia, contenido):
        try:
            nombreTabla = "estandares" + materia
            print("Buscando estandares: " + nombreTabla)

            consulta = "SELECT DISTINCT estandar FROM " + nombreTabla + " WHERE bloque=(?) AND curso=(?)"
            valor = self.cursor.execute(consulta, (contenido, str(curso)))
            # result = []
            # for row in valor.fetchall():
            #    result.append(row)
            result = valor.fetchall()
            return result
        except sqlite3.Error as e:
            print(e)
    def buscaTrimestresporContenido(self,curso,materia,contenido):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT * FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso)))
            #nombreTablaInstrumentos=materia+"Instrumentos"+str(curso)
            #for v in valor:
            #   contenido=str(v[0])[1]
            #   print contenido
            result=valor.fetchone()
            contenido=str(result[0])[1]
            #print ("Primer contenido hallado: "+contenido)
            nombreTabla2=materia+"Instrumentos"+str(curso)
            #print ("procedo a buscar los datos de "+nombreTabla2)
            consulta2="SELECT * FROM "+nombreTabla2+" where contenido=(?)"
            valor2=self.cursor.execute(consulta2,(contenido))
            trimestre=valor.fetchone()
            print ("El contenido "+contenido+" le corresponde el trimestre "+str(trimestre[3]))
            return trimestre[3]
        except sqlite3.Error as e:
            print (e)
    def buscaTrimestresporContenido(self,curso,materia,contenido):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT * FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso)))
            print ("Buscando contenidos para el trimestre: "+contenido)
            #nombreTablaInstrumentos=materia+"Instrumentos"+str(curso)
            #for v in valor:
            #   contenido=str(v[0])[1]
            #   print contenido
            result=valor.fetchone()
            contenido=str(result[0])[1]
            #print ("Primer contenido hallado: "+contenido)
            nombreTabla2=materia+"Instrumentos"+str(curso)
            #print ("procedo a buscar los datos de "+nombreTabla2)
            consulta2="SELECT * FROM "+nombreTabla2+" where contenido=(?)"
            valor2=self.cursor.execute(consulta2,(contenido))
            trimestre=valor.fetchone()
            #print ("El contenido "+contenido+" le corresponde el trimestre "+str(trimestre[3]))
            return trimestre[3]
        except sqlite3.Error as e:
            print (e)
    def buscaTrimestresporCriterio(self,curso,materia,criterio):
        try:
            nombreTabla=materia+"ponderacionCriterios"+str(curso)
            consulta="SELECT * FROM "+nombreTabla+" WHERE criterio==(?)"
            print (consulta)
            print(criterio)
            valor=self.cursor.execute(consulta,(criterio,))
            #nombreTablaInstrumentos=materia+"Instrumentos"+str(curso)
            #for v in valor:
            #   contenido=str(v[0])[1]
            #   print contenido
            trimestre=valor.fetchone()
            print(str(trimestre))
            return trimestre[3]
        except sqlite3.Error as e:
            print ("Error buscando trimestres por criterio: ")
            print (e)
                                                
    def buscaInstrumentosporContenido(self,curso,materia,contenido,trimestre):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT * FROM "+nombreTabla+" WHERE bloque=(?) AND curso=(?)"
            valor=self.cursor.execute(consulta,(contenido,str(curso)))
            #nombreTablaInstrumentos=materia+"Instrumentos"+str(curso)
            #for v in valor:
            #   contenido=str(v[0])[1]
            #   print contenido
            result=valor.fetchone()
            contenido=str(result[0])[1]
            #print ("Primer contenido hallado: "+contenido)
            nombreTabla2=materia+"Instrumentos"+str(curso)
            #print ("procedo a buscar los datos de "+nombreTabla2)
            consulta2="SELECT * FROM "+nombreTabla2+" where contenido=(?) AND trimestre=(?)"
            valor2=self.cursor.execute(consulta2,(contenido,trimestre))
            instrumentos=valor.fetchall()
            #print ("El contenido "+contenido+" le corresponde el trimestre "+str(trimestre[3]))
            return instrumentos
        except sqlite3.Error as e:
            print (e)
    def copiaInstrumentosaTrimestre(self,curso,materia,contenido,trimestreOriginal,trimestreNuevo):
        try:
            nombreTabla=materia+"Instrumentos"+str(curso)
            consulta="SELECT * FROM "+nombreTabla+" WHERE contenido=="+contenido+" AND trimestre=="+str(trimestreOriginal)
            valor=self.cursor.execute(consulta)
            result=valor.fetchall()
            print ("Resultado buscando contenidos: ")
            print (result)
            for r in result:
                print ("Instrumento: ")
                print (r[2])
                consulta2="SELECT * FROM "+nombreTabla+" WHERE instrumento='"+r[2]+"' AND trimestre=="+str(trimestreNuevo)
                valor2=self.cursor.execute(consulta2)
                result=valor.fetchone()
                #print (r)
                if not(result>0):
                    #print ("Copiando instrumentos...")
                    consulta="INSERT INTO "+nombreTabla+" (contenido, instrumento, trimestre) VALUES (?,?,?)"
                    valor=self.cursor.execute(consulta, (r[1], r[2],trimestreNuevo),)
                    
        except sqlite3.Error as e:
            print ("Error tratando de realizar copias de instrumentos de evaluación de un trimestre a otro...")
            print (e)

    def asignaCriterios(self,curso,materia,arrayCriterios):
        try:
            #No sé por qué para crear el nombre de la tabla me quedé originalmente con la letra inicial. Modifico:
            #nombreTablaCriterios=materia[0]+"ponderacionCriterios"+str(curso)
            nombreTablaCriterios=materia+"ponderacionCriterios"+str(curso)
            sql="DROP TABLE IF EXISTS "+nombreTablaCriterios
            #print ("Borrando "+nombreTablaCriterios)
            self.cursor.execute(sql)
            sql="CREATE TABLE IF NOT EXISTS "+nombreTablaCriterios+" (`id` INTEGER PRIMARY KEY, `criterio` varchar(100),`ponderacion` int(3),`trimestre` int (1))"
            #print ("Creando de nuevo la tabla "+nombreTablaCriterios)
            self.cursor.execute(sql)
            #print ("Rellenando la tabla "+nombreTablaCriterios)
            for n in range(len(arrayCriterios)):
                sql="INSERT INTO "+nombreTablaCriterios+" (criterio,ponderacion,trimestre) VALUES (?,?,?)"
                #print ("Criterio: "+arrayCriterios[n][0])
                #print ("Ponderacion: "+str(arrayCriterios[n][1].get()))
                self.cursor.execute(sql,(arrayCriterios[n][0],arrayCriterios[n][1].get(),arrayCriterios[n][2]))

        except sqlite3.Error as e:
            print (e)
            
    def buscaInstrumentos(self,curso,materia,trimestre):
        try:
            nombreTabla=materia+"Instrumentos"+str(curso)
            #print (nombreTabla)
            sql="SELECT DISTINCT instrumento FROM "+nombreTabla+" WHERE trimestre==(?)"
            valor=self.cursor.execute(sql,(str(trimestre),))
            print ("Buscando instrumentos")
            instrumentos=valor.fetchall()
            print(instrumentos)
            instrumental=[]
            for a in instrumentos:
                instrumental.append(a[0])
            return instrumental
        except sqlite3.Error as e:
            print (e)
            
    def buscaInstrumentosporEstandar(self,curso,materia,trimestre,estandar):
        try:
            nombreTabla=materia+"organizacionEstandares"+str(curso)
            #print (nombreTabla)
            #SI HACEMOS CÁLCULOS PARA TODO EL CURSO, TRIMESTRE VALE 4
            if not(trimestre==4):
                sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE trimestre==(?) AND idestandar==(?)"
                valor=self.cursor.execute(sql,(str(trimestre),estandar,))

            else:
                sql="SELECT idinstrumento FROM "+nombreTabla+" WHERE idestandar==(?)"
                valor=self.cursor.execute(sql,(estandar,))

            instrumentos=valor.fetchall()
            return instrumentos
        except sqlite3.Error as e:
            print (e)            
    def dameAlumnosporGrupo(self,grupo):
        try:

            sql="SELECT * FROM matriculas WHERE grupo=(?) ORDER BY apellidos,nombre"
            valor=self.cursor.execute(sql,(grupo,))
            alumnos=valor.fetchall()
            instrumental=[]     
            return alumnos
        except sqlite3.Error as e:
            print (e)

    def grabaNotas(self,tabla,alumnos):
        try:

            sql="INSERT INTO "+tabla+" (alumno,instrumento,nota) VALUES(?,?,?)"
            valor=self.cursor.executemany(sql,(alumnos))

        except sqlite3.Error as e:
            print (e)

    def buscaInstrumentos2(self,curso,materia,trimestre):
        try:
            nombreTabla=materia+"Instrumentos"+str(curso)
            sql="SELECT * FROM "+nombreTabla+" WHERE trimestre==(?)"
            valor=self.cursor.execute(sql,(str(trimestre),))
            instrumentos=valor.fetchall()


            return instrumentos
        except sqlite3.Error as e:
            print (e)
    def buscaNotas(self,curso,materia,alumno,instrumento):
        try:
            nombreTabla=materia+"notas"+str(curso)
            sql="SELECT * FROM "+nombreTabla+" WHERE alumno=(?) AND instrumento==(?)"
            valor=self.cursor.execute(sql,(str(alumno),str(instrumento),))
            instrumentos=valor.fetchall()


            return instrumentos
        except sqlite3.Error as e:
            print (e)
    def actualizaNotas(self,curso,materia,idNota,nota,accion):
        try:
            nombreTabla=materia+"notas"+str(curso)
            print (nombreTabla)
            print (idNota)
            print (nota)
            print (accion)
            if (accion=="actualizar"):
                sql="UPDATE "+nombreTabla+" SET nota=(?) WHERE id=(?)"
                self.cursor.execute(sql,(nota,idNota))

            if (accion=="borrar"):       
                sql="DELETE FROM "+nombreTabla+" WHERE id=(?)"
                self.cursor.execute(sql,(idNota,))

        except sqlite3.Error as e:
            print ("Error en tabla...")
            print (e)
    def borraInstrumentos(self,curso,materia,instrumento):
        try:
            nombreTabla=materia+"Instrumentos"+str(curso)
            print (nombreTabla)

            sql="DELETE FROM "+nombreTabla+" WHERE id=(?)"
            self.cursor.execute(sql,(instrumento,))
            nombreTabla=materia+"organizacionEstandares"+str(curso)
            sql="DELETE FROM "+nombreTabla+" WHERE idinstrumento=(?)"
            self.cursor.execute(sql,(instrumento,))
           

        except sqlite3.Error as e:
            print ("Error en tabla...")
            print (e)
   #CREO QUE EMPECÉ A ESCRIBIR ESTA FUNCIÓN, PERO NO PARECE TENER APLICACIÓN. SU EQUIVALENTE ES asignaInstrumentoEstandar (TAMBIÉN FALTA EL PARÁMETRO PRIORIDAD)         
    def nuevoInstrumentoEstandar(self,curso,materia,idEstandar,idInstrumento,trimestre,accion):
        try:
            nombreTabla=materia+"organizacionestandares"+str(curso)
            print ("idEstandar: "+str(idEstandar))
            print ("trimestre: "+str(trimestre))
            print ("Materia: "+materia)
            print ("Curso: "+str(curso))
            if (accion=="grabar"):
                consulta="SELECT prioridad FROM "+nombreTabla+" WHERE idestandar=(?) AND trimestre=(?)"
                valor=self.cursor.execute(consulta,(str(idEstandar),str(trimestre),))
                resultado=valor.fetchone()
                prioridad=resultado[0]
                print ("grabando en "+nombreTabla+" con prioridad: "+str(prioridad)+" el instrumento "+str(idInstrumento)+" para el estandar "+str(idEstandar)+" en el trimestre "+str(trimestre))
                consulta="INSERT INTO "+nombreTabla+"(prioridad, idestandar, idinstrumento, trimestre) VALUES (?,?,?,?)"
                self.cursor.execute(consulta,(prioridad,idEstandar,idInstrumento,trimestre))

            else:
                print ("borrando")
                consulta="DELETE FROM "+nombreTabla+" WHERE idestandar==(?) AND idinstrumento==(?) AND trimestre==(?)"
                self.cursor.execute(consulta,(idEstandar,idInstrumento,trimestre))
           
        except sqlite3.Error as e:
            print (e)

    def asignaInstrumentoEstandar(self,curso,materia,prioridad,idEstandar,idInstrumento,trimestre,accion):
        try:
            nombreTabla=materia+"organizacionestandares"+str(curso)
            print ("idEstandar: "+str(idEstandar))
            print ("trimestre: "+str(trimestre))
            print ("Materia: "+materia)
            print ("Curso: "+str(curso))
            if (accion=="grabar"):
                #consulta="SELECT prioridad FROM "+nombreTabla+" WHERE idestandar=(?) AND trimestre=(?)"
                #valor=self.cursor.execute(consulta,(str(idEstandar),str(trimestre),))
                #resultado=valor.fetchone()
                #prioridad=resultado[0]
                print ("grabando en "+nombreTabla+" con prioridad: "+str(prioridad)+" el instrumento "+str(idInstrumento)+" para el estandar "+str(idEstandar)+" en el trimestre "+str(trimestre))
                consulta="INSERT INTO "+nombreTabla+"(prioridad, idestandar, idinstrumento, trimestre) VALUES (?,?,?,?)"
                self.cursor.execute(consulta,(prioridad,idEstandar,idInstrumento,trimestre))

            else:
                print ("borrando")
                consulta="DELETE FROM "+nombreTabla+" WHERE idestandar==(?) AND idinstrumento==(?) AND trimestre==(?)"
                self.cursor.execute(consulta,(idEstandar,idInstrumento,trimestre))
           
        except sqlite3.Error as e:
            print (e)
    def buscaEstandaresporTrimestre(self,curso,materia,trimestre):
        try:
            nombreTabla=materia+"organizacionEstandares"+curso
            consulta="SELECT DISTINCT idestandar FROM "+nombreTabla+" WHERE trimestre=(?) ORDER BY idestandar"
            valor=self.cursor.execute(consulta,(str(trimestre)),)
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print (e)
            
    def identificaEstandar(self,materia,idEstandar):
        try:
            nombreTabla="estandares"+materia
            consulta="SELECT estandar FROM "+nombreTabla+" WHERE id=(?)"
            valor=self.cursor.execute(consulta,(idEstandar,))
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
            return result
        except sqlite3.Error as e:
            print (e)
    def actualizaEstandaryTrimestre(self,materia,curso,estandar,trimestreAntiguo,trimestreNuevo):
        try:
            nombreTabla=materia+"organizacionEstandares"+curso
            nombreTabla2=materia+"Instrumentos"+curso
            nombreTabla3="estandares"+materia
            #print ("Estandar en base: "+str(estandar))
            # BUSCAMOS LOS INSTRUMENTOS QUE EVALUABAN DICHO ESTANDAR
            consulta="SELECT * FROM "+nombreTabla+" WHERE idestandar=(?) AND trimestre=(?)"
            valor=self.cursor.execute(consulta,(estandar,trimestreAntiguo),)
            #result = []
            #for row in valor.fetchall():
            #    result.append(row)
            result=valor.fetchall()
          
            #COMPROBAMOS SI EXISTE EL INSTRUMENTO EN EL NUEVO TRIMESTRE; DE LO CONTRARIO, LO INSERTAMOS EN LA TABLA DE INSTRUMENTOS
            for i in result:
                print (i)
                consulta="SELECT DISTINCT id FROM "+nombreTabla2+" WHERE id=(?) AND trimestre=(?)"
                print(consulta)
                print(str(i[3]))
                print (trimestreNuevo)
                valor=self.cursor.execute(consulta,(str(i[3]),trimestreNuevo))
                resultb=valor.fetchone()
                print ("Resultb: ")
                print(resultb)
                #Para localizar el número de contenido, recuperamos de la tabla de estandares su nombre mediante i[2[
                #Hay que localizar si el contenido tiene más de una cifra o no
                consultaContenidos="SELECT * FROM "+nombreTabla3+" WHERE id=(?)"
                valor6=self.cursor.execute(consultaContenidos,((i[2],)))
                resultd=valor6.fetchone()
                if resultd[2][8].isdigit():
                    #print ("El bloque de contenidos es mayor que  9. Es: "+str(contenidos[fila][0])+str(contenidos[fila][1]))
                #Para concatenar ambas cifras, las convierto a string, las sumo y luego las vuelvo a pasar como int
                    a=str(resultd[2][7])
                    b=str(resultd[2][8])
                    bloqueContenido=a+b
                #     base.cursor.execute(consulta, (int(a+b), instrumento, trimestre))
                #
                else:
                    #print ("El bloque de contenidos es menor que  9. Es: "+str(contenidos[fila][0]))
                    bloqueContenido=resultd[2][7]
                #     base.cursor.execute(consulta, (contenidos[fila][7], instrumento, trimestre))
                if (resultb!=None):
                    print ("El instrumento "+str(i[3])+" ya existe")
                    consulta2="UPDATE "+nombreTabla+" SET trimestre=(?) WHERE id=(?)"
                    valor2=self.cursor.execute(consulta2,(trimestreNuevo,i[0]),)
                    
                else:
                    print ("El instrumento "+str(i[3])+" no existe en el trimestre "+str(trimestreNuevo))
                    consulta3="SELECT * FROM "+nombreTabla2+" WHERE id=(?)"
                    valor3=self.cursor.execute(consulta3,(str(i[3]),))
                    resultc=valor.fetchall()
                    #print ("Resultado: ")
                    print ("Instrumento "+resultc[0][2])
                    try:
                        print ("Haciendo copia del instrumento "+str(i[3])+ " con el contenido "+str(i[1])+" al trimestre "+str(trimestreNuevo))
                        consulta4="INSERT INTO "+nombreTabla2+" (contenido, instrumento, trimestre) VALUES (?,?,?)"
                        valor4=self.cursor.execute(consulta4,(bloqueContenido,resultc[0][2],trimestreNuevo),)
                        self.cursor.execute("SELECT * FROM "+nombreTabla2+" ORDER BY id DESC LIMIT 1")
                        result = self.cursor.fetchone()
                        print (result[0])
                        consulta5="UPDATE "+nombreTabla+" SET trimestre=(?), idinstrumento=(?) WHERE id=(?)"
                        valor5=self.cursor.execute(consulta5,(trimestreNuevo,result[0],i[0]),)
                    except sqlite3.Error as e:
                        print("Aqui no es")
                        print (e)
                    except:
                        import traceback
                        traceback.print_exc()     

                    
            
        except sqlite3.Error as e:
            print (e)
