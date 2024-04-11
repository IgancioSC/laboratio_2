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
