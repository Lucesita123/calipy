#ponemor esto para poder luego dejar 1 segundo hasta pasar el siguientetexto que imprimiremos

#este es un ejemplo para entender como funciona with open , 



#para que el texto de presentacion ya actualizado se muestre tendremos que crear un codigo:
#importamos las librerias necesarias

      




#aqui se crea la funcion que nos permitira poder guardar el registro
def guardar_registro(limite,calorias):
    #con el siguiente with open se podra crear un registro de todas las respuestas de diagnostico de los usuarios
    with open ("registro_calorias.txt",'a') as archivo:
        diagnostico_final=f"limite:{limite}kcal, Consumo:{calorias} kcal\n"
        archivo.write(diagnostico_final)
        print("¡Registro de calorías guardado en 'registro_calorias.txt'! 💾")

  



def obtener_limite():
   limite_calorias=float(input("porfavor ingrese su limite de calorias diarias: "))
   return limite_calorias


def sumar_calorias():
   cals_total = 0.0

   for i in range(5):
      entrada= float(input(f"porfavor introduzca las calorias consumidas en su comida {i+1} de 5:"))
      cals_total +=entrada
   return cals_total



def ejecutar_app():
   limite = obtener_limite()
   calorias = sumar_calorias()

   print(f"--- Diagnóstico ---")
   print(f"Límite diario: {limite} kcal")
   print(f"Total consumido: {calorias} kcal")
   print(f"-------------------")
   if calorias<limite:
    print("usted sigue dentro de su limite calorico")
   elif calorias>limite:
    print("haz sobrepasado tu limite")
   else:
    print("felicidades, estas justo en tu limite!") 
    
   guardar_registro(limite,calorias )

ejecutar_app()



   
  
   







    



    
    


    


