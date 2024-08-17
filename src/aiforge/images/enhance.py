# File: _enhance.py

from PIL import Image, ImageEnhance, ImageFilter

from aiforge.images.load import load_image


async def enhance_document_image(image_name: str) -> Image.Image:
    """
    Enhance a document image by increasing contrast, applying sharpening,
    and converting to grayscale.

    Args:
        image_name (str): Name of the input image file.

    Returns:
        Image.Image: Enhanced PIL Image object.
    """
    # Load the image
    image = await load_image(image_name)

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)

    # Apply sharpening filter
    image = image.filter(ImageFilter.SHARPEN)

    # Convert to grayscale
    image = image.convert("L")

    return image
