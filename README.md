![SGC](images/sgc_logo.png)<!-- .element width="700"-->

# ConsultaSQL

Rutina realizada para contar eventos según su magnitud y su tipo. (Se puede hacer simple id o radial). Revisar las isntrucciones.  

## 1. Instalación en linux

### - Requerimientos previos
Se corre en sistemas linux.

*Es necesario que en el archivo conteo.py se cambie esta línea*
```bash
php_query_path = "/home/ecastillo/repositories/php_queries"
```
y se reemplace por la ubicación del repositorio https://github.com/SGC-analistas/php_queries

### - Python
#### Instalación con pip 
Python Versión 3.7 en adelante. (Usaremos como ejemplo python 3.8)
```bash
sudo apt-get install python3.7 (o 3.8)
```
Tener virtualenv en python.
```bash
python3.7 -m pip install virtualenv
```


```bash
python3.7 -m virtualenv .conteo
source .conteo/bin/activate
pip install -r requirements.txt
```
#### Instalación con anaconda 
```bash
conda env create -f enviroment.yml
conda activate php_query
```


## Instrucciones de uso

Si necesita correrlo en consola puede ver los siguientes ejemplos


### Comandos

```bash
+h, ++help            show this help message and exit
  
  REQUERIDOS:
  +s , ++start          Fecha inicial en formato 'yyyymmddThhmmss'
  +e , ++end            Fecha final en formato 'yyyymmddThhmmss'
  +m  [ ...], ++mag     Rango e intervalo de magnitud, ej: 0 10 1
  +d  [ ...], ++depth   Profundidad mínima
  +r  [ ...], ++radial  Se debe especificar: lat lon r. Ejemplo: 6.81 -73.17 120
                        

  OPCIONALES:
  +u  [ ...], ++users           Usuario. ej: ecastillo
  +mysqldb  [ ...], ++mysqldb   Se debe especificar: host user passwd db. Ejemplo: 10.100.100.232 consulta consulta seiscomp3
```

### Ejemplos


- simple

```bash
python conteo.py +s 20210101T000000 +e 20210801T000000 +m 0 10 1 +d 0 200 
```
- simple: servidor 13 con usuario ecastillo

```bash
python conteo.py +s 20210101T000000 +e 20210801T000000 +m 0 10 1 +d 0 200 +u ecastillo +mysqldb 10.100.100.13 consulta consulta seiscomp3 +o prove.csv
```

-radial con usuario ecastillo
```bash
 python conteo.py +s 20210101T000000 +e 20210801T000000 +m 0 10 1 +d 0 200 +r 6.81 -73.17 120 +u ecastillo
```


## Autor

- Emmanuel  Castillo ecastillo@sgc.gov.co


