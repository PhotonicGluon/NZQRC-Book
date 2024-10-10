from PIL import Image, ImageChops


def trim(im: Image.Image):
    # Ensure image is in RGB mode
    im = im.convert("RGB")  # RGBA will ruin things

    # Generate pure background based on top left-hand corner
    bg = Image.new(im.mode, im.size, im.getpixel((0, 0)))

    # Get main 'content' image
    diff = ImageChops.difference(im, bg)

    # Bound to content
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

    raise ValueError("No bounding box")


if __name__ == "__main__":
    im = Image.open(
        "../media/images/image-generation/0-relations-is-born-in.png"
    ).convert("RGB")
    im = trim(im)
    im.show()
