# laboratio_2
En este laboratorio el trabajo estara dividido en tres partes, comenzamos con lo basico donde vamos analizar como es la comunicacion entre el codigo de talker y el listener, para el intermedio vamos a trabajar con turtleSim donde aprendemos como crear un launch para iniciar y configuara los nodos y parametros de cada codigo a ejecutar, despues diseñamos un programa para que la toruga se mueva mediante comandos de teclado, es decir W,S,A,D para avanzar adelante, atras, izquierda y derecha, cuando esto funcione correcto modificamos el programa para que al ejecutar el launch del cubo la tortuga cree un cuadrado y asi lo mismo para un triaungulo, en el nivel avanzado tenemos que hacer que la tortuga avance mediante cordenadas en X,Y y THETA y despues hacer la trasnformacion espacial para que esta regrese a sus grados de posicion inicial y no se pierda al ponerle nuevamente cordenadas ya que si no se hace eso la tortuga se pierde y como no sabe que hacer solo forma una espiral sin detenerse.

# Para que es un launch y como funciona
Un archivo de launch es utilizado para iniciar y configurar nodos y otros componentes del sistema ROS, se utilizan para definir la configuración del entorno de trabajo, especificar qué nodos personalizados que deben ejecutarse y cómo se deben configurar. En pocas palabras es para ayudar una mejor comunicacion, personalisacion y manipualcion de archivos tanto en ROS como Python. 

# como funciona listener y talker en el nivel basico
El "talker" es un nodo que publica mensajes en el tópico “chatter”. Envía un mensaje cada segundo (1hz) que contiene la cadena “hello world” seguida de un contador que incrementa con cada mensaje, en el caso del "listener" es un nodo que se suscribe al tópico “chatter” este utiliza la función "chatter_callback" que sirve para hacer el registro de la información recibida cuando se ejecuta, este se queda esperando mensajes en el tópico “chatter”.

Cuando ambos códigos se ejecutan al mismo tiempo, la comunicación se realiza de la siguiente manera:

El talker inicia y comienza a publicar mensajes en el tópico “chatter”.

El listener está suscrito a ese mismo tópico y recibe los mensajes publicados por el talker.

Cada vez que el listener recibe un mensaje, llama a chatter_callback donde este registra el mensaje recibido y asi esto se repetira cada que el master este levantado y el nodo funcionando.

# creacion del programa para mover la tortuga con W,S,A y D y creacion del cuadrado y el triangulo en el nivel intermedio

En este apartado diseñamos un codigo para que la tortuga pueda moverse con las teclas W,S,A y D, cuando se resulve este problema pasamos a diseñar el cuadrado con la tortuga mediante cordenadas y recordar que tambien usaremos un launch nuevo para este nodo, donde tenemos que: 
* Se inicializa un nodo ROS con el nombre "turtle" utilizando rospy.init_node()
* Se crea un publicador que publica en el tema "/turtle1/cmd_vel" para enviar comandos de velocidad a la tortuga.

Configuramos las variables y el teclado:

* Se inicializan variables para almacenar los mensajes de velocidad (Twist), la tasa de publicación (Rate) y la tecla presionada (key).
* Se configura el teclado para leer una sola tecla sin necesidad de presionar Enter.

## Cuadrado
```python
#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty


class TeleopTurtleSim:
    def __init__(self):
        rospy.init_node('turle', anonymous=False)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=5)
        self.twist = Twist()
        self.rate = rospy.Rate(1)  # Reducido a 1Hz para facilitar la visualización
        self.key = None
        self.settings = termios.tcgetattr(sys.stdin)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            self.key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

    def teleopLoop(self):
        rospy.loginfo("Presiona Ctrl-C para salir y observa cómo la tortuga forma un cuadrado.")

        for _ in range(5):
            # Avanzar hacia adelante
            self.twist.linear.x = 1.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Girar 90 grados hacia la izquierda
            self.twist.linear.x = 0.0
            self.twist.angular.z = 2  # 1.57 radianes es aproximadamente 90 grados
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

        rospy.loginfo("Cuadrado completado. Saliendo del bucle.")


if __name__ == '__main__':
    teleop_turtlesim = TeleopTurtleSim()
    try:
        teleop_turtlesim.teleopLoop()
    except rospy.ROSInterruptException:
        pass
 ```
En este codigo tenemos lo siguiente para forma la figura del cubo:

Inicialización del nodo y publicador:
* Se inicializa un nodo con el nombre 'turle' utilizando rospy.init_node().
* Se crea un publicador que publica en el tema '/turtle1/cmd_vel' para enviar comandos de velocidad a la tortuga.

Inicialización de variables y configuración de teclado:

* Se inicializan variables para almacenar los mensajes de velocidad (Twist), la tasa de publicación (Rate) y la tecla presionada (key).
* Se configura el teclado para leer una sola tecla sin necesidad de presionar Enter.
*Función getKey():Esta función se encarga de leer la entrada del teclado para determinar qué tecla se ha presionado.

Bucle de control teleopLoop():
* Este bucle se ejecuta hasta que se interrumpe el programa.
* Se imprime un mensaje de instrucción para indicar cómo salir del programa y qué hará la tortuga.
* El bucle se repite 5 veces para formar un cuadrado.
* En cada iteración:
  1. La tortuga avanza hacia adelante durante un segundo (linear.x = 1.0) durante un período de tiempo. Esto se logra estableciendo self.twist.linear.x = 1.0, espués de avanzar durante un tiempo (determinado por self.rate.sleep()), se detiene configurando self.twist.linear.x = 0.0. Esto detiene el movimiento lineal de la tortuga.
  2. Luego se detiene.
  3. La tortuga gira 90° hacia la izquierda (angular.z = 2).
  4. Luego se detiene nuevamente.
     
Por ultimo se maneja la excepción "ROSErrorInterruptException" para salir del bucle y finalizar el programa limpiamente cuando se presiona Ctrl-C.
## triangulo
Para el codigo del triangulo vamos a modifar algunos puntos pára que ahora no forme un cuadrado pero ya es mas facil por el avance que tenemos al sacar el movimeinto de la tortuga con teclas y al formar el cubo.

Acontinuacion se muestra una imagen al ejecutar el nodo:
![image](https://github.com/IgancioSC/laboratio_2/assets/157633777/472eaa4d-04ab-41b2-9be8-d70777ce2a49)

```python
#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty
import math


class TeleopTurtleSim:
    def __init__(self):
        rospy.init_node('tri', anonymous=False)
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=5)
        self.twist = Twist()
        self.rate = rospy.Rate(1)  # Reducido a 1Hz para facilitar la visualización
        self.key = None
        self.settings = termios.tcgetattr(sys.stdin)

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            self.key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)

    def teleopLoop(self):
        rospy.loginfo("Presiona Ctrl-C para salir y observa cómo la tortuga forma un triángulo equilátero.")

        for _ in range(4):
            # Avanzar hacia adelante
            self.twist.linear.x = 1.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Girar 120 grados hacia la izquierda
            self.twist.linear.x = 0.0
            self.twist.angular.z = math.radians(120)  # Convertir 120 grados a radianes
            self.pub.publish(self.twist)
            self.rate.sleep()

            # Detenerse
            self.twist.linear.x = 0.0
            self.twist.angular.z = 0.0
            self.pub.publish(self.twist)
            self.rate.sleep()

        rospy.loginfo("Triángulo equilátero completado. Saliendo del bucle.")


if __name__ == '__main__':
    teleop_turtlesim = TeleopTurtleSim()
    try:
        teleop_turtlesim.teleopLoop()
    except rospy.ROSInterruptException:
        pass
```
A grandes rasgos lo que se hace este esta parte con el codigo presentado comenzamos por:

Inicialización del nodo y publicador:
* Se inicializa un nodo ROS con el nombre 'tri' utilizando rospy.init_node().
* Se crea un publicador que publica en el tema '/turtle1/cmd_vel' para enviar comandos de velocidad a la tortuga.

Inicialización de variables y configuración de teclado:
* Se inicializan variables para almacenar los mensajes de velocidad (Twist), la tasa de publicación (Rate) y la tecla presionada (key).
* Se configura el teclado para leer una sola tecla sin necesidad de presionar Enter.
* Método getKey(): Esta función se encarga de leer la entrada del teclado para determinar qué tecla se ha presionado.

Bucle de control teleopLoop():
* Este bucle se ejecuta hasta que se interrumpe el programa.
* Se imprime un mensaje de instrucción para indicar cómo salir del programa y qué hará la tortuga.
* El bucle se repite 4 veces para formar un triángulo equilátero.
* En cada iteración:
  1. La tortuga avanza hacia adelante durante un período de tiempo (linear.x = 1.0).
  2. Luego se detiene.
  3. La tortuga gira 120° hacia la izquierda (angular.z = math.radians(120)) para formar un ángulo interno del triángulo equilátero.
  4. Luego se detiene nuevamente.

# Avanzado: diseñar un controlador PID
