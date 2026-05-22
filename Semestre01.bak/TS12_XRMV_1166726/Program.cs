 namespace Matrizes
 {
     static class Program
     {
         static void Main()
         {
             ///////// EJERCICIO 0 /////////
             int[,] matriz = new int[4, 3]
             {
                { 5, 7, 1 },
                { 2, 8 ,6 },
                { 3, 4, 5 },
                { 4, 7, 9 }
             };

             for (int i = 0; i < matriz.GetLength(0); i++)
             {
                 int totalFila = 0;
                 for (int j = 0; j < matriz.GetLength(1); j++)
                 {
                     Console.Write($"{matriz[i,j]}  ");
                     totalFila += matriz[i,j];
                 }
             Console.WriteLine($" = {totalFila}");
             }
             Console.WriteLine();


             ///////// EJERCICIO 1 /////////
             for (int i = 0; i < matriz.GetLength(0); i++)
             {
                 for (int j = 0; j < matriz.GetLength(1); j++)
                 {
                     if (matriz[i,j] % 2 == 0)
                         Console.ForegroundColor = ConsoleColor.Magenta;
                     else
                         Console.ForegroundColor = ConsoleColor.Cyan;
                     Console.Write($"{matriz[i,j]}  ");
                 }
                 Console.WriteLine();
             }
             Console.ResetColor();
             Console.WriteLine();

             ///////// EJERCICIO 2 /////////
             for (int i = 0; i < matriz.GetLength(0); i++)
             {
                 int mayorFila = matriz[i,0];
                 for (int j = 1; j < matriz.GetLength(1); j++)
                 {
                    if (mayorFila < matriz[i,j])
                        { mayorFila = matriz[i, j]; }
                 }
                 Console.WriteLine($"Mayor Fila {i+1}: {mayorFila}");
             }
             Console.WriteLine();


             ///////// EJERCICIO 3 /////////
             int fila;
             int columna;
             int valor;

             Console.Write("Ingrese la fila: ");
             fila = int.Parse(Console.ReadLine() ?? "");
             Console.Write("Ingrese la columna: ");
             columna = int.Parse(Console.ReadLine() ?? "");

             valor = matriz[fila, columna];
             Console.WriteLine($"Se multiplicara la matriz por {valor}\n");

             for (int i = 0; i < matriz.GetLength(0); i++)
             {
                 for (int j = 0; j < matriz.GetLength(1); j++)
                 {
                    Console.Write($"{matriz[i,j] * valor:D2}  ");
                 }
                 Console.WriteLine();
             }
             Console.WriteLine();


             ///////// EJERCICIO 4 /////////
             for (int i = 0; i < matriz.GetLength(1); i++)
             {
                 int producto = 1;
                 for (int j = 0; j < matriz.GetLength(0); j++)
                 {
                        Console.Write($"{matriz[j,i]}  ");
                        producto *= matriz[j,i];
                 }
                 Console.WriteLine($" = {producto}");
             }
             Console.WriteLine();

         }
     }
 }
