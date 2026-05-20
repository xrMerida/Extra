Cheatsheet Pseudocodigo

1. Tipos de Datos
    
    Tipo        Primitivo    Ejemplo         Tamaño 
                                              
    numerico    int          i = 10          4 Bytes 
    numerico    double       d = 10.5        8 Bytes
    numerico    float        f = 10.5        4 Bytes
    caracter    char         c = 'a'         2 Bytes
    logico      bool         b = true        1 Byte 
    cadena      string       s = "cadena"    2B / char

    String no simempre es un dato primitivo, pero usualmente se
    considera uno.
    https://en.wikipedia.org/wiki/String_(computer_science)
    Adiconalmente exite short, byte, long y decimal.

2. Expresiones
    
    2.1 Aritmeticas

    Evaluan solamente datos de tipo numerico

    Operador    Funcion           Ejemplo        
                                                 
    +           Sumar             x = y + z      
    -           Restar            x = y - z      
    *           Multiplicación    x = y * z      
    /           División          x = y / z      
    %           Modulo            x = y % z      
    ()          Prioridad         x = 2 * (y + z)

    2.1.2 Simplificación Aritmetica

    Todos los operadores aritmeticos (excepto el de prioridad) pueden
    simplificarse si la asignación de una variable se contiene a si misma

    Forma Original    Simplificación

    x = x + 1         x++               // Funcion: Incremento
    x = x - 1         x--               // Función: Decremento
    x = x + y         x += y
    x = x - y         x -= y
    x = x * y         x *= y
    x = x / y         x /= y
    x = x % y         x %= y

    2.3 Lógicas
    
    Evaluan solamente datos de tipo logico (true/false)

    Operador    Utilidad      Ejemplo
                           
    not         Negación      not p
    and         Conunción     p and q
    or          Disyunción    p or q
    ()          Prioridad     not (p and q)

    2.4 Relacionales

    Siempre obtiene como resultado un dato de tipo logico (true/false)
    Solamente puede operar dos datos del mismo tipo.

    Operador    Comparación          Ejemplo

    ==          Igual a              p == q
    !=          Diferente de         p != q
    <           Menor que            p < q
    >           Mayor que            p > q
    <=          Menor o igual que    p <= q
    >=          Mayor o igual que    p >= q

    Estos se pueden combinar con las expresiones lógicas utilizando el 
    operador de prioridad

    Ejemplos                   Significado

    (p == q) and (p < r)       P igual a Q y P menor que R
    not (q < p) or (p == r)    P no es menor que Q o P es igual a R

3. Estructuras Selectivas
    
    Es una expresión lógica compuesta.
    Ejecuta (o no) una porción de codigo, basandose en si una expresón logica
    tiene como resultado verdadero o falso.
    Solo evalua datos de tipo logico

    Tipo         Condiciones
    
    Simple       = 1
    Doble        = 1
    Compuesta    > 1
    Multiple     > 0

    3.1 Simple

    Evalua una condicion, ejecuta el codigo que le prosigue solamente
    si el resultado es verdadero
    
    if <condicion> then
        <codigo>         
    end_if               

    if x == y then
        Write("Los valores son iguales")
    end_if
                         
    3.2 Doble

    Evalua una expresión logica, si el resultado es verdadero, ejecuta el codigo
    que le prosigue, si el resultado es falso, ejecuta el codigo que prosigue
    a la palabra reservada 'else'
    
    if <condicion> then
        <codigo_1>         

    else
        <codigo_2>

    end_if               

    if x == y then
        Write("Los valores son iguales")
    else

        Write("Los valores no son iguales")
    end_if

    3.3 Compuestas

    Evalua multiples expresiónes logicas y ejecuta el codigo que le prosigue a
    cada expresiona, solamente si esta es verdadera.
    Opcionalmente, si ninguna es verdadera, ejecutara el codigo que prodigue a
    la palabra reservada 'else'
    
    if <condicion> then
        <codigo_1>         

    else
        if <condicion>
            <codigo_2>
        end_if

    else
        <codigo_3>
    end_if               

    if x > y then
        Write("X es mayor que Y")

    else 
        if x < y
            Write("X es menor que Y")
        end_if

    else // Opcional
        Write("X es igual que Y")
    end_if

    3.4 Multiples

    Simplificación de una estructura condicional compuesta (la anterior).
    Usualmente se le conoce como un "switch".
    Solamenete se puede utilizar al evaluar multiples condiciones a un solo
    valor. Las condiciones no pueden contener variables (son constantes).
    Si ningun valor es igual a la variable que se evalua, se ejecuta el
    codigo que prosigue a la palabra reservada 'else'

    case <variable>
        <condicion_1>:
            <codigo_1>
            break

        <condicion_2>:
            <codigo_2>
            break

        else
            break
    end_case

    case dia
        "Lunes":
            Write("Inicio de semana")
            break

        "Domingo" or "Sabado":
            Write("Fin de semana")
            break

        else
            Write("Transcurso de semana")
            break
    end_case

    La palabra reservada 'break', es utilizada para definir en que
    parte debe acabar la ejecución.
    En caso no se coloque 'break', se ejecutara el codigo de otros valores
    a los que la variable no es igual.
    Esto se conoce como "fallthrough" y puede ser realizado intencioalmente
    lo que se conoce como "intentionall fallthrough".
    Fallthrough puede ocurrir en todos los valores del switch, a excepción
    del ultimo.
    https://en.wikipedia.org/wiki/Switch_statement

4. Estructuras Repetitivas
    
    Una expresión logica compuesta que ejecuta una cicla (repite) una
    porción de codigo, mientras una cierta expresión lógica sea verdadera.
    Sale del bucle de repetición cuando esta expresión es falsa o cuando se
    solicita explicitamente.
    
    Tipos       Uso
                
    while       Repetir mientras una condicion sea verdadera
    for         Repetir una cierta cantidad de veces
    do while    Como while, pero ejecuta al menos una vez

    4.1 While

    Evalua una condición, ejecutara el codigo mientras la condición 
    sea verdadera, saldra del bucle solamente cuando sea falsa.

    while <condición> do
        <codigo>
    end_while

    int i = 0
    while i <= 20 do
        if 20 % i == 0 then
            Write("20 es divisible entre " + i)
        end_if
        i++;
    end_while

    En el ejemplo anterior, el codigo muestra todos los numeros entre 0 y 20
    que son divisbles entre 20

    4.2 For
    
    Simplificación de ciclo while. Cuenta con 3 partes.
        Inicialización: define el inicio de un contador (se infiere int)
        Condición:      ejecuta el codigo mientras la variable sea menor a el
                        valor colocado
        Incremento:     define en cuanto incrementa el contador por iteración

    for <inicialización> to <condicion> step <incremento> do
        <codigo>
    end_for

    for i = 0 to 20 step 1 do
        if 20 % i == 0 then
            Write("20 es divisible entre " + i)
        end_if
    end_for

    El ejemplo anterior realiza lo mismo que el ejemplo de while

    4.3 Do While

    Al diferencia de while, do while permite al codigo ejectuarse al menos una
    vez, despues se evalua la expresión logica, si es verdadera cicla el 
    codigo.

    do
        <codigo>
    while <condicion>
    end_do-while

    do
        Write("Esta de acuerdo?")
        respuesta = Read()
    while respuesta != "si"
    end_do-while
    
    El ejemplo anterior pregunta al usuario si esta de acuerdo, y repite
    el codigo hasta que el usuario ingrese "si"

5. Rutinas / Subrutinas
    
    Secuencia de instrucciones que se puede ejecutar en demanda.
    Pueden o no retornar un dato.

    Tipo             Descripción

    Función          Retornan un valor
    Procedimiento    Sin retorno
    Metodos          Funcion o procedimeinto asociado a una case u objeto

    Convencionalmente los nombres de las subrutinas se escribe en
    UpperCamelCase, es decir que se inicia en mayuscula y se coloca
    una mayuscual por cada palabra.

    Correcto         Incorrecto

    EvaluarAlgo()    evaluarlago()

    5.1 Parametros

    Una subrutina puede o no tener parametros y estos pueden ser:

    Forma         Descripción
    
    Valor         La subrutina copia el valor del parametro y no puede modificar
                  la variable
    Referencia    La subrutina utiliza la variable del parametro
                  y la puede modificar

    Para especificar una subrutina si la entrada es por referncia, se utiliza
    la palabra reservada 'ref'

    Forma         Ejemplo
                  
    Valor         (int numero, string cadena)
    Referencia    (ref int numero, ref string cadena)

    5.4 Procedimientos

    Devuelven void (vacio), en otras palabras, no devuelven un valor

    procedure <nombre> (<parametros>)
    begin
        <codigo>
    end_procedure

    procedure MostrarNumeros (int limite)
    begin
        for i = 0 to limite step 1 do
            Write(i)
        end_for
    end_procedure

    El ejemplo anterior muestra todos los numeros desde el 0 hasta el valor
    ingresado por el parametro 'limite'
    
    Usualmente los procedimientos escriben o muestran algo al usuario y no
    realizan calculos, a no ser que utizen un valor por referencia. Por ejemplo:

    procedure Curar (ref int vida) 
    begin
        if vida > 90 then
            vida = 100
        else
            vida += 10
        end_if
    end_procedure

    El ejemplo anterior utiliza un parametro por referencia 'vida' al cual
    le suma '10', note que el maximo de vida es 100.

    5.3 Funciones

    Deben devolver un dato, el tipo de dato que retornara la función se
    escribe como si se declarara una variable

    <tipo de dato de retorno> function <nombre> (<parametros>)
    begin
            <codigo>
            return <valor de retorno>
        end_function

    bool function EsPar (int numero)
    begin
        if numero % 2 == 0 then
            return true

        else
            return false
        end_if
    end_function

    El ejemplo retorna un valor booleano¸ el cual es verdader cuando el
    parametro 'numero' es divisibel entre 2. Se puede simplificar al devolver
    el valor de la condicion

    bool function EsPar (int numero)
    begin
        return numero % 2 == 0
    end_function

    5.3.1 Sobrecarga

    Ocurre cuando dos funciones que reciben diferentes paramteros son declaradas
    con el mismo nombre

    string function MomentoSemana (int dia)
    begin
        case dia in
            1:
                return "Inicio"
                break

            6 or 7:
                return "Final"
                break

            else
                return "Transcurso"
                break
            end_case
    end_function

    string function MomentoSemana (string dia)
    begin
        case dia in
            "Lunes":
                return "Inicio"
                break

            "Sabado" or "Domingo":
                return "Final"
                break

            else
                return "Transcurso"
                break
            end_case
    end_function

    En el ejemplo anterior MomentoSemana devuelve un string segun el momento
    de la semana. Se puede llamar la función y entregar el día de la semana
    en string o en int

    5.4 Invocación

    Para invocar (o llamar) una subrutina, se escribe su nombre y entre parentesis
    los parametors a enviar. Una subrutina puede llamar a otra subrutina internamente

    MomentoSemana(1)       // Devuelve Inicio
    MomentoSemana("Lunes") // Devuelve Inicio
    
    5.1 Internas

    Exsiten subrutinas internas, que son estandar en la mayoria de lenguajes de
    programación:
        
    Subrutina    Tipo             Retorno           Utilidad

    Write()      Procedimiento    Void              Escribe en una terminal
    Read()       Función          string            Retorna texto ingresado en 
                                                    una terminal.
    .ToString    Metodo           string            Retrona el valor asociado al
                                                    objeto como un string.
    .ToInt       Metodo           int               Retrona el valor asociado al
                                                    objeto como un int.

    // Se puede convertir a todos los tipos de datos de la forma .To<Tipo>

    .Length      Metodo           int               Retorna la lognitud de un objeto
                                                    (usualmente un arreglo)

    // etc

6. Manejo de Cadenas (string)
    
    Un ordenador solo puede entender instrucciones en binario. Para mostrar
    caracteres se creo un codigo que permite al ordenador entender y 
    mostrar cadenas de caracteres

    6.1 Codificación de Caracteres
        
    ASCII o American Standard for Infomation Interchange es un estandar que
    define cada caracter en 7 bits. En total tiene 128 caracteres posibles.
    El codigo 'ASCII Ampliado' utiliza 8 bits y tiene un total de 256 caracteres

    UNICODE un estandar que consiste en UTF-8, UTF-16 y UTF-32. El estandar más
    utilizado actualmente por la mayoria de computadoras es UTF-8, el cual es
    compatible con ASCII de 7 bits.

    6.1 Caracteres de Control

    Caracteres definidos por los codigos de 00 - 37 en ASCII. Estos caracteres
    no se pueden imprimir en pantalla, cada uno ejecuta una acción relacionada
    al movimiento del cursor o el texto escrito. Se les llama sequencia de escape
    ANSI.

    Para utilizar estos caracteres, se escribe una 'sequencia de escape', inicia
    con un backslash '\', seguido de una letra representativa:

    Caracter    Utilidad                 Sequencia    Codigo
                                         
    NUL         Terminador nulo          \0           0
    BS          Retroceso                \b           8
    HT          Tabulación Horizotnal    \t           9
    LF          Avance de Linea          \n           10
    VT          Tabulación Vertical      \f           11
    CR          Retorno de cursor        \r           13

    Mas informacion: https://www.asciitable.com/

    6.2 Strings

    Las variables string son un conjunto de caracteres. En lenguajes como C,
    estos se representaban como un arreglo de char 'char[]'. En otros lenguajes
    los string son más completos y tienen funciones internas.

    string <nombre> = "<valor>"

    string apellidos = "Valencia"

    6.2.1 Concatencaicón
    
    Concatenar se le llama a combinar 2 cadenas (strings) en una sola. Se puede
    utilizar el operador '+' o ',' para unir dos strings

    <cadena_1> + <cadena_2>
    <cadena_1>, <cadena_2>

    "Hola " + "Mundo" // Resutlado: "Hola Mundo"
    "Hola ", "Mundo"  // Resutlado: "Hola Mundo"

    6.2.2 Subrutinas Internas
    
    Subrutina    Tipo        Retorno    Descripción
              
    Position     Función     int        Obtiene la posicion de una cadena en otra
    Substring    Función     string     Obtiene una subcadena de la cadena original
    Insert       Función     string     Inserta una cadena dentro de otra cadena
    Delete       Función     string     Elimina una cadena dentro de otra cadena
    .Length      Metodo      int        Mide la cantidad de caracteres de la cadena
    .ToLower     Metodo      string     Convierte todos los caracteres a minusculas
    .ToUpper     Metodo      string     Convierte todos los caracteres a mayusculas
    .ToInt       Metodo      int        Convierte la cadena a un numero entero
    .ToFloat     Metodo      float      Convierte la cadena a un numero flotante
    // .To<dato> Funciona con todos los tipos de datos
    
    6.2.2.1 Ejemplos

    - Substring (<cadena>, <posición>, <caracteres>)

    string cadena = "Hola!"
    string subcadena
    subcadena = Substring(cadena, 0, 2) 
    // Resultado: subcadena = "Ho"
    subcadena = Substring(cadena, 2) 
    // Resultado: subcadena = "la!"

    - Position (<cadena>, <subcadena>)

    string cadena = "Mundo!"
    int posicion
    posicion = Position (cadena, "do!")
    // Resultado: posicion = 3
    posicion = Position (cadena, "nd")
    // Resultado: posicion = 2

    - Insert (<cadena>, <posicion>, <subcadena>)
    
    string cadena = "Bienvenido"
    string nuevaCadena
    nuevaCadena = Insert (cadena, 9, "!")
    // Resultado: nuevaCadena = "Bienvenido!"
    nuevaCadena = Insert (cadena, 3, ", ")
    // Resultado: nuevaCadena = "Bien, venido"

    - Delete (<cadena>, <posicion>, <caracteres>)

    string cadena = "Pseudocodigo"
    string nuevaCadena
    nuevaCadena = Delete (cadena, 0, 6)
    // Resultado: nuevaCadena = "codigo"
    nuevaCadena = Delete (cadena, 6, 6)
    // Resultado: nuevaCadena = "Pseudo"

    - .ToUpper()

    string cadena = "min-MAYUS"
    string nuevaCadena
    nuevaCadena = cadena.ToUpper()
    // Resultado: nuevaCadena = "MIN-MAYUS"
    nuevaCadena = cadena.ToLower()
    // Resultado: nuevaCadena = "min-mayus"

7. Arreglos
    
    Colección estatica de una cantidad finita de datos del mismo tipo

    Tipo                Descripción

    Unidimensionales    Aquellos arelglos que solamente tienen una 
                        fila y multiples columnas
    Bidimensionales     Aquellos arreglos que tienen mutliples columnas
                        y filas
    Multidimensionales  Aquellos arreglos que tienen mutliples columnas,
                        filas, profundidad, etc.

    7.1 Arreglos unidimensionales

    Declaración                              Ejemplo

    <tipo de dato>[] <nombre>[<cantidad>]    int[] numeros[5]

    // Arreglo de 5 valores

    7.1.2 Asignación

    <nombre>[] = { <valor_1>, <valor_2>, ... }

    numeros[] = { 1, 5, 3, 2, 9 }

    7.1.3 Asignación por Posicion

    <nombre>[<posicion>] = <valor>

    numeros[0] = 1
    numeros[1] = 5

    7.2 Matrices
