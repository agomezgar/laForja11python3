import csv
def rellena_matriculas(archivo):
    print(archivo)
    print("intentando...")
    try:
        f = open(archivo, 'r')
        # next (f,None)
        print(f)
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row:
                print('probando')
                self.cursor.execute("INSERT INTO matriculas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
        f.close()
    except Exception as inst:
        print("Error abriendo archivo",inst)

rellena_matriculas('datMatriculas.csv')