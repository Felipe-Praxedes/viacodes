import fitz  # PyMuPDF
from PIL import Image

def pdf_to_images(pdf_path, image_folder):
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()

        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Salvar a imagem em um arquivo
        image.save(f"{image_folder}/page{page_number + 1}.png")

    pdf_document.close()

if __name__ == '__main__':
    pdf_receber = r'C:\Users\geova\OneDrive\Desktop\Python\LER\scaneado.pdf'
    img_receber = r'C:\Users\geova\OneDrive\Desktop\Python\LER\img'
    pdf_to_images(pdf_receber,img_receber)