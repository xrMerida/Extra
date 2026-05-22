using System;

namespace Try_Catch;

static class Program
{
    static void Main()
    {
        WriteContinue(1);
        ////////// EJERCICIO 01 //////////
        double entrada;
        while (true)
        {
            try
            {
                Console.Write("Ingrse un numero real: ");
                // Se agrega ?? "" para manejar 'ArgumentNullExeption'
                entrada = double.Parse(Console.ReadLine() ?? "");
                CleanLine();

                // Mostrar el cuadrado
                Console.WriteLine($"=> {entrada:00.00}² = {Math.Pow(entrada, 2):00.00}");

                // Mostrar la raiz
                Console.WriteLine($"=> √{entrada:00.00} = {Math.Sqrt(entrada):00.00}");

                break;
            }
            catch (FormatException)
                { WriteError("Ingrese un numero real"); }
            catch (OverflowException)
                { WriteError("El numero ingresado es extreamadamente grande"); }
        }

        WriteContinue(2);
        ////////// EJERCICIO 02 //////////
        Console.Write("Ingrese una palabra: ");
        // Manejo de NullReferenceException usando ?? ""
        if (TieneHiato(Console.ReadLine() ?? ""))
            Console.WriteLine("=> Hiato encontrado en la palabra");
        else
            Console.WriteLine("=> No coincide con ninguna forma de Hiato");


        WriteContinue(3);
        ////////// EJERCICIO 03 //////////
        int seleccion;
        string[] colores =
        [
            "Rojo",
            "Azul",
            "Amarillo",
            "Verde",
            "Blanco",
            "Violeta",
            "Naranja"
        ];

        for (int i = 0; i < colores.Length; i++)
            Console.WriteLine($" [{i}] {colores[i]}");

        while (true)
        {
            try
            {
                Console.Write("Ingrese la posicion del arreglo [0-9]: ");
                // Se agrega ?? "" para manejar 'ArgumentNullExeption'
                seleccion = int.Parse(Console.ReadLine() ?? "");
                CleanLine();

                // Mostrar el cuadrado
                Console.WriteLine($"=> {colores[seleccion]}");
                break;
            }
            catch (FormatException)
                { WriteError("Ingrese un numero entero"); }
            catch (IndexOutOfRangeException)
                { WriteError("El numero ingresado esta fuera del rango"); }
        }
    }

    static bool TieneHiato (string palabra)
    {
        char[] abiertas        = ['a', 'e', 'o', 'á', 'é', 'ó'];
        char[] cerradas        = ['i', 'u'];
        char[] cerradasTonicas = ['í', 'ú'];
        string vocales = $"{abiertas}{cerradas}{cerradasTonicas}";
        palabra = palabra.ToLower();

        // Se le resta 1 palabras.Length para evitar IndexOutOfRangeException
        for (int i = 0; i < palabra.Length - 1; i++)
        {
            // Dos Vocales Iguales
            if (vocales.Contains(palabra[i])
                && palabra[i] == palabra[i + 1])
            { return true; }

            // Filtrar vocales abiertas
            else if (abiertas.Contains(palabra[i]))
            {
                // Vocal abierta + Vocal abierta
                if (abiertas.Contains(palabra[i + 1]))
                    return true;

                // Vocal abierta + Tonica Cerrada
                else if (cerradasTonicas.Contains(palabra[i + 1]))
                    return true;
            }

            // Tonica Cerrada + Vocal Abierta
            else if (cerradasTonicas.Contains(palabra[i])
                     && abiertas.Contains(palabra[i + 1]))
            { return true; }
        }

        return false;
    }
    static void WriteContinue (int ejercicio)
    {
        // Muestra un mensaje para continuar con el ejercicio
        Console.ForegroundColor = ConsoleColor.Cyan;
        if (ejercicio > 1)
        {
            Console.Write("\n :: Presione una tecla para continuar");
            Console.ReadKey(true);
        }
        Console.WriteLine($"\r\e[K////////// EJRCICIO {ejercicio:00} //////////");
        Console.ResetColor();
    }

    static void WriteError (string mensajeError)
    {
        // Permite mostrar un error en consola sin cambiar el cursor de linea
        Console.ForegroundColor = ConsoleColor.Red;
        Console.Write($"\r\e[K  ERROR: {mensajeError}\eM\r\e[K");
        Console.ResetColor();
    }
    static void CleanLine ()
    {
        // Limpia el error escrito por WriteError()
        Console.Write("\r\e[K");
    }
}
