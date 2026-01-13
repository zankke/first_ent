import os
from pdf2image import convert_from_path

pdf_path = './frontend/public/docs/R.book_03.pdf'
output_dir = '/Users/itsme/.gemini/tmp/8832996cc5a8c644c3eb4f11fbcd275fcadff3f865de234a4bd8246b0acc2a00'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        image.save(os.path.join(output_dir, f'page_{i+1}.png'), 'PNG')
    print(f"Successfully converted {len(images)} pages to PNGs in {output_dir}")
except Exception as e:
    print(f"Error during PDF conversion: {e}")
