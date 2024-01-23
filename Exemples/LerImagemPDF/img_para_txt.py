import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\geova\OneDrive\Desktop\Python\LER\Tesseract-OCR\tesseract.exe'
config = r'--oem 3 --psm 6'

# Carrega a imagem usando o OpenCV
imagem = cv2.imread('')

# Converte a imagem em texto usando o Tesseract OCR
texto = pytesseract.image_to_string(imagem, config=config)

# Imprime o texto extraído da imagem
print(texto)
