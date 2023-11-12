# Affinity_Mango_Wardrobe Documentation and Notes
Esta aplicación utiliza procesamiento en Python con librerías como pandas, matplotlib, seaborn y sklearn. Este proceso genera matrices de correspondencia que son utilizadas como filtros de afinidad para determinar la compatibilidad entre las prendas del DataSet original. Esta afinidad es traducida en diccionarios de tres métricas principales: Color, Tipo y Material. Aplicando estos diccionarios se determina la afinidad de una prenda con otras para determinar su compatibilidad dentro de un mismo outfit.  
  
  El resultado es registrado y mostrado gracias a una aplicación construida con Streamlit que genera con una seed aleatoria un outfit basado íntegramente en la afinidad de esa prenda con las otras. Adicionalmente, este algoritmo es resistente a datos nuevos que cuenten con los mismos campos que en los originales del DataSet y los clasificará con la afinidad base que desarrolló. Por lo tanto, la métrica utilizada precisa de un DataSet original, que será en el que se basará desde el primer momento y podrá ser alimentado con nuevas imagenes para generar outfits con ellas.
  
  A continuación se muestran capturas del funcionamiento de la aplicación web.

![outfit4](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/4704a82f-a941-4919-bba6-379501abedb0)
![image](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/f7a742cf-4651-4f16-9e8d-31ae193edaf3)
![image](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/8526d617-2538-49ba-99b8-3aab2bbe0cca)
![image](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/6ef9ebde-940a-49e5-8b8b-bf94fd5f6d37)
![outfit6](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/93cd8466-15c6-4ba8-8910-8167e11879de)
![image](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/cf132f17-a399-46d1-8572-57f087e2e001)

![image](https://github.com/Vex62/Affinity_Mango_Wardrobe/assets/101091948/559e3460-1a6c-4270-b7d9-beb56f10f278)

Por razones técnicas no ha sido posible hacer un "Deploy" de la aplicación, pero su funcionalidad está completamente incluida en el código del repositorio.
