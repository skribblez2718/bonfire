import random
import io
from typing import Optional, Union, Tuple, TypeVar

from PIL import Image, ImageDraw, ImageFont

# Define a type for image data
ImageType = TypeVar("ImageType")


###################################[ start BonfireImageManipulate ]###################################
class BonfireImageManipulate:
    """
    Class for image manipulation with various methods to modify image data.
    """

    # ── Shared class state ────────────────────────────────────────────
    available_fonts = [
        "Arial",
        "Courier New",
        "Times New Roman",
        "Verdana",
        "DejaVuSans",
        "LiberationSans",
    ]
    font_cache: dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}
    format: str = "PNG"  # default output format

    #########################[ start change_text_font_all ]##############
    @staticmethod
    def change_text_font_all(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Render the supplied text with a *single*, randomly-chosen font.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font(
                random.choice(BonfireImageManipulate.available_fonts), 36
            )
            pos = BonfireImageManipulate._center_position(text, font, width, height)
            draw.text(pos, text, fill="black", font=font)
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_font_all: {e}")
            return image

    #########################[ end change_text_font_all ]################

    #########################[ start change_text_font_random ]###########
    @staticmethod
    def change_text_font_random(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Randomly vary the font of individual characters.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            default_font = BonfireImageManipulate._select_font("Arial", 36)

            # Baseline starting point
            bbox = default_font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            start_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                font = (
                    BonfireImageManipulate._select_font(
                        random.choice(BonfireImageManipulate.available_fonts), 36
                    )
                    if random.random() < 0.5
                    else default_font
                )
                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                draw.text((current_x, start_y), ch, fill="black", font=font)
                current_x += ch_w

            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_font_random: {e}")
            return image

    #########################[ end change_text_font_random ]#############

    #########################[ start change_text_color_all ]#############
    @staticmethod
    def change_text_color_all(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Render text with a single random colour.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font("Arial", 36)
            colour = tuple(random.randint(0, 200) for _ in range(3))
            draw.text(
                BonfireImageManipulate._center_position(text, font, width, height),
                text,
                fill=colour,
                font=font,
            )
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_color_all: {e}")
            return image

    #########################[ end change_text_color_all ]###############

    #########################[ start change_text_color_random ]##########
    @staticmethod
    def change_text_color_random(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Give each character a 50 % chance of being a random colour.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font("Arial", 36)

            bbox = font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            base_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                colour = (
                    tuple(random.randint(0, 200) for _ in range(3))
                    if random.random() < 0.5
                    else (0, 0, 0)
                )
                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                draw.text((current_x, base_y), ch, fill=colour, font=font)
                current_x += ch_w

            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_color_random: {e}")
            return image

    #########################[ end change_text_color_random ]############

    #########################[ start change_text_position_all ]##########
    @staticmethod
    def change_text_position_all(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Move the entire string to a random position on the canvas.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font("Arial", 36)
            bbox = font.getbbox(text)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]
            margin = 20
            pos_x = random.randint(margin, max(margin, width - text_w - margin))
            pos_y = random.randint(margin, max(margin, height - text_h - margin))
            draw.text((pos_x, pos_y), text, fill="black", font=font)
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_position_all: {e}")
            return image

    #########################[ end change_text_position_all ]############

    #########################[ start change_text_position_random ]#######
    @staticmethod
    def change_text_position_random(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Randomly offset individual characters around the baseline.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font("Arial", 36)

            bbox = font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            base_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                offset_x, offset_y = (
                    (random.randint(-10, 10), random.randint(-10, 10))
                    if random.random() < 0.5
                    else (0, 0)
                )
                draw.text(
                    (current_x + offset_x, base_y + offset_y),
                    ch,
                    fill="black",
                    font=font,
                )
                current_x += font.getbbox(ch)[2] - font.getbbox(ch)[0]

            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_position_random: {e}")
            return image

    #########################[ end change_text_position_random ]#########

    #########################[ start change_text_size_all ]##############
    @staticmethod
    def change_text_size_all(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Render all characters at a single random size.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            font = BonfireImageManipulate._select_font("Arial", random.randint(20, 50))
            draw.text(
                BonfireImageManipulate._center_position(text, font, width, height),
                text,
                fill="black",
                font=font,
            )
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_size_all: {e}")
            return image

    #########################[ end change_text_size_all ]################

    #########################[ start change_text_size_random ]###########
    @staticmethod
    def change_text_size_random(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Vary character sizes randomly.
        """
        try:
            canvas, draw, width, height = BonfireImageManipulate._prepare_canvas(image)
            text = prompt_text or ""
            default_font = BonfireImageManipulate._select_font("Arial", 36)

            bbox = default_font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            baseline_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                font = (
                    BonfireImageManipulate._select_font("Arial", random.randint(20, 50))
                    if random.random() < 0.5
                    else default_font
                )
                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                ch_h = font.getbbox(ch)[3] - font.getbbox(ch)[1]
                y = baseline_y - (ch_h - (bbox[3] - bbox[1])) // 2
                draw.text((current_x, y), ch, fill="black", font=font)
                current_x += ch_w

            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_text_size_random: {e}")
            return image

    #########################[ end change_text_size_random ]#############

    #########################[ start change_background_pixels_all ]######
    @staticmethod
    def change_background_pixels_all(
        image: ImageType, *, prompt_text: Optional[str] = None, logger
    ) -> ImageType:
        """
        Apply random noise to every pixel.
        """
        try:
            img = Image.open(io.BytesIO(image))
            new_img = Image.new("RGB", img.size)
            pixels = []

            for px in img.getdata():
                if isinstance(px, tuple):
                    noisy = tuple(
                        min(255, max(0, c + random.randint(-50, 50))) for c in px[:3]
                    )
                    pixels.append(noisy + px[3:] if len(px) > 3 else noisy)
                else:
                    pixels.append(min(255, max(0, px + random.randint(-50, 50))))

            new_img.putdata(pixels)
            return BonfireImageManipulate._finalise_image(new_img)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_background_pixels_all: {e}")
            return image

    #########################[ end change_background_pixels_all ]########

    #########################[ start change_background_pixels_random ]###
    @staticmethod
    def change_background_pixels_random(
        image: ImageType, *, prompt_text: Optional[str] = None, logger
    ) -> ImageType:
        """
        Randomly perturb ~30 % of pixels.
        """
        try:
            img = Image.open(io.BytesIO(image))
            new_img = img.copy()
            width, height = img.size
            total = int(width * height * 0.3)

            for _ in range(total):
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                px = img.getpixel((x, y))
                if isinstance(px, tuple):
                    noisy = tuple(
                        min(255, max(0, c + random.randint(-70, 70))) for c in px[:3]
                    )
                    new_img.putpixel((x, y), noisy + px[3:] if len(px) > 3 else noisy)
                elif isinstance(px, int):
                    new_img.putpixel(
                        (x, y), min(255, max(0, px + random.randint(-70, 70)))
                    )

            return BonfireImageManipulate._finalise_image(new_img)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_background_pixels_random: {e}")
            return image

    #########################[ end change_background_pixels_random ]#####

    #########################[ start change_background_color_all ]#######
    @staticmethod
    def change_background_color_all(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Replace background with a uniform random colour.
        """
        try:
            text = prompt_text or ""
            img = Image.open(io.BytesIO(image))
            width, height = img.size
            bg_colour = tuple(random.randint(100, 255) for _ in range(3))
            canvas = Image.new("RGB", (width, height), color=bg_colour)
            draw = ImageDraw.Draw(canvas)
            font = BonfireImageManipulate._select_font("Arial", 36)
            text_colour = tuple(255 - c for c in bg_colour)
            draw.text(
                BonfireImageManipulate._center_position(text, font, width, height),
                text,
                fill=text_colour,
                font=font,
            )
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_background_color_all: {e}")
            return image

    #########################[ end change_background_color_all ]#########

    #########################[ start change_background_color_random ]####
    @staticmethod
    def change_background_color_random(
        image: ImageType, *, prompt_text: Optional[str], logger
    ) -> ImageType:
        """
        Paint several random-coloured rectangles behind the text.
        """
        try:
            text = prompt_text or ""
            img = Image.open(io.BytesIO(image))
            width, height = img.size
            canvas = Image.new("RGB", (width, height), color="white")
            draw = ImageDraw.Draw(canvas)
            font = BonfireImageManipulate._select_font("Arial", 36)

            for _ in range(random.randint(3, 7)):
                colour = tuple(random.randint(100, 255) for _ in range(3))
                rw, rh = random.randint(width // 5, width // 2), random.randint(
                    height // 5, height // 2
                )
                rx, ry = random.randint(0, width - rw), random.randint(0, height - rh)
                draw.rectangle([(rx, ry), (rx + rw, ry + rh)], fill=colour)

            draw.text(
                BonfireImageManipulate._center_position(text, font, width, height),
                text,
                fill="black",
                font=font,
            )
            return BonfireImageManipulate._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            logger.error(f"change_background_color_random: {e}")
            return image

    #########################[ end change_background_color_random ]######

    # ── Internal helpers (unchanged public API) ────────────────────────
    #########################[ start _prepare_canvas ]###################
    @staticmethod
    def _prepare_canvas(
        image_bytes: bytes,
        background_color: Union[str, Tuple[int, int, int]] = "white",
    ) -> Tuple[Image.Image, ImageDraw.ImageDraw, int, int]:
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        canvas = Image.new("RGB", (width, height), color=background_color)
        draw = ImageDraw.Draw(canvas)
        return canvas, draw, width, height

    #########################[ start _select_font ]######################
    @staticmethod
    def _select_font(
        font_name: str = "Arial", font_size: int = 36
    ) -> ImageFont.FreeTypeFont:
        key = (font_name, font_size)
        if key in BonfireImageManipulate.font_cache:
            return BonfireImageManipulate.font_cache[key]
        try:
            font = ImageFont.truetype(font_name, font_size)
        except IOError:
            font = ImageFont.load_default()
        BonfireImageManipulate.font_cache[key] = font
        return font

    #########################[ start _center_position ]##################
    @staticmethod
    def _center_position(
        text: str, font: ImageFont.FreeTypeFont, width: int, height: int
    ) -> Tuple[int, int]:
        bbox = font.getbbox(text)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        return (width - text_w) // 2, (height - text_h) // 2

    #########################[ start _finalise_image ]###################
    @staticmethod
    def _finalise_image(img: Image.Image) -> bytes:
        buf = io.BytesIO()
        img.save(buf, format=BonfireImageManipulate.format.upper())
        return buf.getvalue()

    #########################[ end _finalise_image ]#####################


###################################[ end BonfireImageManipulate ]#####################################
