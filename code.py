import os
from PIL import Image, ImageDraw
import fitz  # PyMuPDF

def add_watermark(input_image_path, output_image_path, watermark_image_path, position, transparency):
    original = Image.open(input_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")

    # Adjust watermark transparency
    watermark = watermark.copy()
    alpha = watermark.split()[3]
    alpha = Image.eval(alpha, lambda a: int(a * transparency))
    watermark.putalpha(alpha)

    # Calculate position for the watermark
    width, height = original.size
    watermark_width, watermark_height = watermark.size

    if position == 'top-left':
        x = 10
        y = 10
    elif position == 'top-right':
        x = width - watermark_width - 10
        y = 10
    elif position == 'bottom-left':
        x = 10
        y = height - watermark_height - 10
    elif position == 'bottom-right':
        x = width - watermark_width - 10
        y = height - watermark_height - 10
    else:
        raise ValueError("Invalid position argument. Use 'top-left', 'top-right', 'bottom-left', or 'bottom-right'.")

    # Add watermark to the original image
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(original, (0, 0))
    transparent.paste(watermark, (x, y), mask=watermark)
    watermarked = Image.alpha_composite(transparent, Image.new('RGBA', (width, height), (0, 0, 0, 0)))

    # Save watermarked image
    watermarked.convert("RGB").save(output_image_path, "JPEG")

def convert_pdf_to_images(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        output_image_path = os.path.join(output_folder, f"page_{page_num}.png")
        pix.save(output_image_path)
        images.append(output_image_path)
    return images

def process_folder(input_folder, output_folder, watermark_image_path, position, transparency):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        if os.path.isfile(input_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                output_path = os.path.join(output_folder, filename)
                if os.path.exists(output_path):
                    print(f"File {filename} already exists in the output folder.")
                else:
                    add_watermark(input_path, output_path, watermark_image_path, position, transparency)
                    print(f"Watermarked {filename} and saved to {output_path}")

            elif filename.lower().endswith('.pdf'):
                pdf_images = convert_pdf_to_images(input_path, output_folder)
                for image_path in pdf_images:
                    output_path = os.path.join(output_folder, os.path.basename(image_path))
                    add_watermark(image_path, output_path, watermark_image_path, position, transparency)
                    print(f"Converted PDF {filename} to image and watermarked, saved to {output_path}")

input_folder = 'D:\\BU Corner\\PastPaper\\WitoutWM'
output_folder = 'D:\\BU Corner\\PastPaper\\WithWM'
watermark_image_path = 'D:\\BU Corner\\PastPaper\\WM.png'
position = 'bottom-right'  # Change this to 'top-left', 'top-right', 'bottom-left', or 'bottom-right'
transparency = 0.3  # Set the transparency level (0.0 to 1.0)

process_folder(input_folder, output_folder, watermark_image_path, position, transparency)
