# FastFuzzing

Herramienta hecha en `python3` que permite realizar `fuzzing` de directorios y subdominios de manera rapida y visualmente comoda, ya que te muestra la información parseada en una tabla a colorines; ademas te permite controlar la velocidad del escaneo ya que puedes establecer el numero de hilos a emplear, si deseas tambien puedes `fuzzear` especificando uno o varios tipos de extensión y puedes filtrar los resultados ocultando los codigos de estado que no quieres visualizar.

# Instalación

```
git clone https://github.com/Firtsmiracle/FastFuzzing
cd FastFuzzing
pip3 install -r requirements.txt
```

# Requisitos

El requisito es muy simple:

1. Debes tener instalado `python3` y instalar los requerimientos necesarios en la instalación.

# Modo de Uso

```
python3 fast_fuzzing.py -h
```
![](https://github.com/Firtsmiracle/FastFuzzing/blob/main/Images/fuzz1.PNG)

> Seleccione las opciones para utilizar la herramienta segun su necesidad.

 * El programa te pedira como parametros necesarios la url y la ruta del diccionario:

    - `-u | --url`: Indicar la url objetivo `Puedes especificar la url o solamente indicar el dominio sin el protocolo`
    - `-w | --worlist`: Indicar la ruta del diccionario a emplear.

 * Como parametros opcionales:

    - `-t | --treads`: Establecer el numero de hilos a emplear.
    - `--hc`: Ocultar uno o varios codigos de estado `Ejem: --hc 404 301 403 ..`
    - `--subdomains`: Fuzzear por subdominios, al agregar el parametro automaticamente el programa cambia de fuzzear directorios a subdominios.
    - `--e | --extensions`: Fuzzear por uno o varios tipos de extensiones `Ejem: --e py, js, php, txt, ....`.
 
![](https://github.com/Firtsmiracle/FastFuzzing/blob/main/Images/fuzz2.PNG)

> Para salir del programa presione `Ctrl-c`.


