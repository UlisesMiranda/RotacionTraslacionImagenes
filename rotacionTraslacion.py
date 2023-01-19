import cv2
import numpy as np

# Definir función para procesar clicks en la imagen
def click(event, x, y, flags, param):
  global points
  # Si se hace click izquierdo, guardar coordenadas en la lista
  if event == cv2.EVENT_LBUTTONDOWN:
    points.append((x, y))

# Función para aplicar transformación  a la imagen
def transform(image, M, mask):
  # Crear imagen de salida con el mismo tamaño que la imagen original
  transformed_image = np.zeros_like(image)

  # Recorrer cada pixel de la imagen
  for i in range(image.shape[0]):
    for j in range(image.shape[1]):
      # Verificar si el pixel está dentro de la región seleccionada
      if mask[i][j]:
        # Calcular nuevas coordenadas del pixel utilizando la matriz de transformación afín
        x_prime = M[0][0] * j + M[0][1] * i + M[0][2]
        y_prime = M[1][0] * j + M[1][1] * i + M[1][2]

        # Verificar que las coordenadas estén dentro del rango de la imagen original
        if 0 <= x_prime < image.shape[1] and 0 <= y_prime < image.shape[0]:
          # Asignar valor del pixel a la posición correspondiente en la imagen de salida
          transformed_image[int(y_prime)][int(x_prime)] = image[i][j]

  return transformed_image


# Cargar imagen
image = cv2.imread('crayones.jpg')

# Crear ventana 'image'
cv2.namedWindow('image')

# Crear una lista que contendra las coordenadas de los clicks
global points 
points = []

# Asignar método click como manejador de eventos de ratón para la imagen
cv2.setMouseCallback('image', click)

# Bucle principal
while True:

  img_copy = image.copy()
  for point in points:
    cv2.circle(img_copy, point, 5, (0, 0, 255), -1)
    
  cv2.imshow('image', img_copy)
  
  # Si se han seleccionado cuatro esquinas, calcular posición y tamaño de la región
  if len(points) == 4:

    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]

    # Calcular ancho y alto de la región
    width = max(x1, x2, x3, x4) - min(x1, x2, x3, x4)
    height = max(y1, y2, y3, y4) - min(y1, y2, y3, y4)

    # Crear máscara de la región seleccionada
    mask = np.zeros_like(image[:, :, 0], dtype=bool)
    mask[min(y1, y2, y3, y4):min(y1, y2, y3, y4) + height, min(x1, x2, x3, x4):min(x1, x2, x3, x4) + width] = True

    # Especificar ángulo de rotación, punto de rotación y desplazamiento en x y y
    angle = 90
    dx = 0
    dy = -100
    # Calcular centro de rotación
    center_x = (x1 + x2 + x3 + x4) // 4
    center_y = (y1 + y2 + y3 + y4) // 4
    
    cv2.circle(img_copy, (center_x, center_y), 5, (0, 255, 0), -1)
    cv2.imshow('image', img_copy)

    # Crear matriz de transformación afín
    M = [[np.cos(np.radians(angle)), -np.sin(np.radians(angle)), center_x + dx],
        [np.sin(np.radians(angle)), np.cos(np.radians(angle)), 0]]

    # Aplicar transformación afín a la imagen
    transformed_image = transform(image, M, mask)
    # Mostrar imagen original y imagen transformada
    cv2.imshow('Original', image)
    cv2.imshow('Transformed', transformed_image)

  # Si se pulsa la tecla "q", sale del bucle
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# Cierra las ventanas y finaliza el programa
cv2.destroyAllWindows()