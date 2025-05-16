import random
import math
import base64
import io
from typing import Callable, Optional, TypeVar, List, Dict, Any, Union, Tuple
from tqdm import tqdm

from PIL import Image, ImageDraw, ImageFont

from bonfire.utils.augment import BonfireEvasion
from bonfire.utils.logger import BonfireLogger

# Define a type for image data
ImageType = TypeVar("ImageType")


###################################[ start BonfireVisionEvasion ]##############################################
class BonfireVisionEvasion(BonfireEvasion):
    """
    Class for vision augmentation with various methods to modify visual data.
    """

    #########################[ start __init__ ]##############################################
    def __init__(
        self,
        prompts: List[Dict[str, Any]],
        output_file_path: Optional[str] = None,
        format: str = "png",
    ) -> None:
        # Initialize logger
        self.logger = BonfireLogger("BonfireVisionEvasion")

        super().__init__(
            data=prompts,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireVisionEvasion"
        self.format: str = format

        # List of available fonts for text manipulation methods (reduced to common fonts)
        self.available_fonts = [
            "Arial",
            "Courier New",
            "Times New Roman",
            "Verdana",
            "DejaVuSans",
            "LiberationSans"
        ]
        # Font cache for fast repeated loading
        self.font_cache = {}

    #########################[ end __init__ ]################################################

    #########################[ start apply ]################################################
    def apply(self) -> List[Dict[str, Any]]:
        """
        Apply all available augmentation methods to the given data

        Returns:
            List of dictionaries describing original and augmented images.
        """
        results: List[Dict[str, Any]] = []
        image_methods = self.get_available_methods()

        for prompt_obj in tqdm(self.data, desc="Generating vision payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            original_image_bytes = self.generate_image(prompt_text, self.format)
            original_base64 = base64.b64encode(original_image_bytes).decode("utf-8")

            # Unmodified baseline
            results.append(
                {
                    "intent": intent,
                    "method": method,
                    "method_name": method_name,
                    "prompt_name": prompt_name,
                    "image_augmentation": "None",
                    "original_text": prompt_text,
                    "prompt_text": prompt_text,
                    "original_image": original_base64,
                    "augmented_image": original_base64,
                }
            )

            # Augmentations
            for augmentation_method in image_methods:
                try:
                    aug_bytes = augmentation_method(
                        original_image_bytes, prompt_text=prompt_text
                    )

                    if aug_bytes is None:
                        self.logger.warning(
                            f"{augmentation_method.__name__} returned None, skipping"
                        )
                        continue

                    if isinstance(aug_bytes, bytes):
                        augmented_base64 = base64.b64encode(aug_bytes).decode("utf-8")
                    else:
                        self.logger.warning(
                            f"{augmentation_method.__name__} returned non-bytes, skipping"
                        )
                        continue

                    results.append(
                        {
                            "intent": intent,
                            "method": method,
                            "method_name": method_name,
                            "prompt_name": prompt_name,
                            "image_augmentation": augmentation_method.__name__,
                            "original_text": prompt_text,
                            "prompt_text": prompt_text,
                            "original_image": original_base64,
                            "augmented_image": augmented_base64,
                        }
                    )
                except Exception as exc:  # pragma: no cover
                    self.logger.error(
                        f"Error applying {augmentation_method.__name__}: {exc}"
                    )

        self.logger.info(f"Generated {len(results)} augmented images")
        return results

    #########################[ end apply ]################################################

    #########################[ start get_available_methods ]##############################################
    def get_available_methods(self) -> List[Callable]:
        """
        Return a list of all augmentation callables.
        """
        return [
            self.change_text_font_all,
            self.change_text_font_random,
            self.change_text_color_all,
            self.change_text_color_random,
            self.change_text_position_all,
            self.change_text_position_random,
            self.change_text_size_all,
            self.change_text_size_random,
            self.change_background_pixels_all,
            self.change_background_pixels_random,
            self.change_background_color_all,
            self.change_background_color_random,
            self.all,
        ]

    #########################[ end get_available_methods ]################################################

    #########################[ start change_text_font_all ]##############################################
    def change_text_font_all(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Render the supplied text with a *single*, randomly-chosen font.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font(random.choice(self.available_fonts), 36)
            pos = self._center_position(text, font, width, height)
            draw.text(pos, text, fill="black", font=font)
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_font_all: %s", e)
            return image

    #########################[ end change_text_font_all ]################################################

    #########################[ start change_text_font_random ]##############################################
    def change_text_font_random(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Randomly vary the font of individual characters.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            default_font = self._select_font("Arial", 36)

            # Baseline starting point
            bbox = default_font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            start_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                font = (
                    self._select_font(random.choice(self.available_fonts), 36)
                    if random.random() < 0.5
                    else default_font
                )
                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                draw.text((current_x, start_y), ch, fill="black", font=font)
                current_x += ch_w

            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_font_random: %s", e)
            return image

    #########################[ end change_text_font_random ]################################################

    #########################[ start change_text_color_all ]##############################################
    def change_text_color_all(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Render text with a single random colour.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font("Arial", 36)
            colour = tuple(random.randint(0, 200) for _ in range(3))
            draw.text(
                self._center_position(text, font, width, height),
                text,
                fill=colour,
                font=font,
            )
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_color_all: %s", e)
            return image

    #########################[ end change_text_color_all ]################################################

    #########################[ start change_text_color_random ]##############################################
    def change_text_color_random(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Give each character a 50 % chance of being a random colour.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font("Arial", 36)

            bbox = font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            base_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                colour = (0, 0, 0)
                if random.random() < 0.5:
                    colour = tuple(random.randint(0, 200) for _ in range(3))
                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                draw.text((current_x, base_y), ch, fill=colour, font=font)
                current_x += ch_w

            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_color_random: %s", e)
            return image

    #########################[ end change_text_color_random ]################################################

    #########################[ start change_text_position_all ]##############################################
    def change_text_position_all(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Move the entire string to a random position on the canvas.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font("Arial", 36)
            text_w, text_h = font.getbbox(text)[2:]
            margin = 20
            pos_x = random.randint(margin, max(margin, width - text_w - margin))
            pos_y = random.randint(margin, max(margin, height - text_h - margin))
            draw.text((pos_x, pos_y), text, fill="black", font=font)
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_position_all: %s", e)
            return image

    #########################[ end change_text_position_all ]################################################

    #########################[ start change_text_position_random ]##############################################
    def change_text_position_random(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Randomly offset individual characters around the baseline.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font("Arial", 36)

            bbox = font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            base_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                if random.random() < 0.5:
                    offset_x = random.randint(-10, 10)
                    offset_y = random.randint(-10, 10)
                else:
                    offset_x = offset_y = 0

                draw.text(
                    (current_x + offset_x, base_y + offset_y),
                    ch,
                    fill="black",
                    font=font,
                )
                current_x += font.getbbox(ch)[2] - font.getbbox(ch)[0]

            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_position_random: %s", e)
            return image

    #########################[ end change_text_position_random ]################################################

    #########################[ start change_text_size_all ]##############################################
    def change_text_size_all(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Render all characters at a single random size.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            font = self._select_font("Arial", random.randint(20, 50))
            draw.text(
                self._center_position(text, font, width, height),
                text,
                fill="black",
                font=font,
            )
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_size_all: %s", e)
            return image

    #########################[ end change_text_size_all ]################################################

    #########################[ start change_text_size_random ]##############################################
    def change_text_size_random(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Vary character sizes randomly.
        """
        try:
            canvas, draw, width, height = self._prepare_canvas(image)
            text = prompt_text or ""
            default_font = self._select_font("Arial", 36)

            bbox = default_font.getbbox(text)
            current_x = (width - (bbox[2] - bbox[0])) // 2
            baseline_y = (height - (bbox[3] - bbox[1])) // 2

            for ch in text:
                if random.random() < 0.5:
                    font = self._select_font("Arial", random.randint(20, 50))
                else:
                    font = default_font

                ch_w = font.getbbox(ch)[2] - font.getbbox(ch)[0]
                ch_h = font.getbbox(ch)[3] - font.getbbox(ch)[1]
                y = baseline_y - (ch_h - (bbox[3] - bbox[1])) // 2
                draw.text((current_x, y), ch, fill="black", font=font)
                current_x += ch_w

            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_text_size_random: %s", e)
            return image

    #########################[ end change_text_size_random ]################################################

    #########################[ start change_background_pixels_all ]##############################################
    def change_background_pixels_all(self, image: ImageType, **kwargs) -> ImageType:
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
            return self._finalise_image(new_img)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_background_pixels_all: %s", e)
            return image

    #########################[ end change_background_pixels_all ]################################################

    #########################[ start change_background_pixels_random ]##############################################
    def change_background_pixels_random(self, image: ImageType, **kwargs) -> ImageType:
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

            return self._finalise_image(new_img)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_background_pixels_random: %s", e)
            return image

    #########################[ end change_background_pixels_random ]################################################

    #########################[ start change_background_color_all ]##############################################
    def change_background_color_all(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
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
            font = self._select_font("Arial", 36)
            text_colour = tuple(255 - c for c in bg_colour)
            draw.text(
                self._center_position(text, font, width, height),
                text,
                fill=text_colour,
                font=font,
            )
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_background_color_all: %s", e)
            return image

    #########################[ end change_background_color_all ]################################################

    #########################[ start change_background_color_random ]##############################################
    def change_background_color_random(
        self, image: ImageType, *, prompt_text: Optional[str] = None, **kwargs
    ) -> ImageType:
        """
        Paint several random coloured rectangles behind the text.
        """
        try:
            text = prompt_text or ""
            img = Image.open(io.BytesIO(image))
            width, height = img.size
            canvas = Image.new("RGB", (width, height), color="white")
            draw = ImageDraw.Draw(canvas)
            font = self._select_font("Arial", 36)

            for _ in range(random.randint(3, 7)):
                colour = tuple(random.randint(100, 255) for _ in range(3))
                rw, rh = random.randint(width // 5, width // 2), random.randint(
                    height // 5, height // 2
                )
                rx, ry = random.randint(0, width - rw), random.randint(0, height - rh)
                draw.rectangle([(rx, ry), (rx + rw, ry + rh)], fill=colour)

            draw.text(
                self._center_position(text, font, width, height),
                text,
                fill="black",
                font=font,
            )
            return self._finalise_image(canvas)
        except Exception as e:  # pragma: no cover
            self.logger.error("change_background_color_random: %s", e)
            return image

    #########################[ end change_background_color_random ]################################################

    #########################[ start all ]##############################################
    def all(self, image: ImageType, **kwargs) -> ImageType:
        """
        Sequentially apply every augmentation (except this one).
        Skips self.all to avoid infinite recursion (pattern from audio.py).
        """
        result = image
        # Skip the 'all' method itself to avoid infinite recursion
        methods = [m for m in self.get_available_methods() if m != self.all]
        for method in methods:
            result = method(result, **kwargs)
        return result

    #########################[ end all ]################################################

    #########################[ start generate_image ]##############################################
    def generate_image(self, text: str, format: str = "png") -> bytes:
        """
        Generate an image with the specified text based on the format.

        Args:
            text: The text to display in the image
            format: The image format (png, jpeg, gif)

        Returns:
            bytes: The generated image as bytes
        """
        if format.lower() == "png":
            return self.generate_png(text)
        elif format.lower() == "jpeg":
            return self.generate_jpeg(text)
        elif format.lower() == "gif":
            return self.generate_gif(text)
        else:
            # Default to PNG if format is not recognized
            return self.generate_png(text)

    #########################[ end generate_image ]################################################

    #########################[ start generate_png ]##############################################
    def generate_png(self, text: str) -> bytes:
        """
        Generate a PNG image with the specified text.

        Args:
            text: The text to display in the image

        Returns:
            bytes: The generated PNG image as bytes
        """
        # Create a new image with white background
        width, height = 800, 400
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)

        # Try to use a standard font, fallback to default if not available
        try:
            # Start with a reasonable font size
            font_size = 36
            font = ImageFont.truetype("Arial", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Ensure text fits within the image width by adjusting font size if needed
        self._ensure_text_fits(draw, text, font, width, height)

        # Draw text on the image (with wrapping if needed)
        self._draw_text_with_wrapping(draw, text, font, width, height)

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    #########################[ end generate_png ]################################################

    #########################[ start generate_jpeg ]##############################################
    def generate_jpeg(self, text: str) -> bytes:
        """
        Generate a JPEG image with the specified text.

        Args:
            text: The text to display in the image

        Returns:
            bytes: The generated JPEG image as bytes
        """
        # Create a new image with gradient background
        width, height = 800, 400
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)

        # Create a simple gradient background
        for y in range(height):
            r = int(255 * (1 - y / height))
            g = int(200 * (y / height))
            b = int(255 * (y / height))
            for x in range(width):
                draw.point((x, y), fill=(r, g, b))

        # Try to use a standard font, fallback to default if not available
        try:
            # Start with a reasonable font size
            font_size = 36
            font = ImageFont.truetype("Arial", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Ensure text fits within the image width by adjusting font size if needed
        font = self._ensure_text_fits(draw, text, font, width, height)

        # Check if we need to wrap text
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        max_width = int(width * 0.8)

        if text_width <= max_width:
            # Text fits on a single line, center it
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)

            # Draw text on the image with a slight shadow for better visibility
            draw.text((position[0] + 2, position[1] + 2), text, fill="black", font=font)
            draw.text(position, text, fill="white", font=font)
        else:
            # Use the wrapping method with custom drawing for shadow effect
            self._draw_text_with_wrapping_and_shadow(draw, text, font, width, height)

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        return buffer.getvalue()

    #########################[ end generate_jpeg ]################################################

    #########################[ start generate_gif ]##############################################
    def generate_gif(self, text: str) -> bytes:
        """
        Generate an animated GIF with the specified text.

        Args:
            text: The text to display in the image

        Returns:
            bytes: The generated GIF image as bytes
        """
        # Create a series of frames for the animation
        width, height = 800, 400
        frames = []

        # Try to use a standard font, fallback to default if not available
        try:
            # Start with a reasonable font size
            font_size = 36
            font = ImageFont.truetype("Arial", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Create a temporary image to ensure text fits
        temp_image = Image.new("RGB", (width, height), color="white")
        temp_draw = ImageDraw.Draw(temp_image)

        # Ensure text fits within the image width by adjusting font size if needed
        font = self._ensure_text_fits(temp_draw, text, font, width, height)

        # Check if we need to wrap text
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        max_width = int(width * 0.8)

        # Prepare text lines for wrapping if needed
        if text_width > max_width:
            words = text.split()
            lines = []
            current_line = []

            # Group words into lines that fit within max_width
            for word in words:
                # Try adding this word to the current line
                test_line = " ".join(current_line + [word])
                bbox = font.getbbox(test_line)
                test_width = bbox[2] - bbox[0]

                if test_width <= max_width:
                    # Word fits, add it to the current line
                    current_line.append(word)
                else:
                    # Word doesn't fit, start a new line
                    if current_line:  # Don't add empty lines
                        lines.append(" ".join(current_line))
                    current_line = [word]

            # Add the last line if it's not empty
            if current_line:
                lines.append(" ".join(current_line))
        else:
            # Single line case
            lines = [text]

        # Calculate line height for positioning
        line_height = (
            font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
        )  # Approximate line height
        total_text_height = len(lines) * line_height * 1.2  # Add 20% for line spacing

        # Generate 10 frames with different background colors
        for i in range(10):
            # Create a new frame with a gradient background
            image = Image.new("RGB", (width, height), color="white")
            draw = ImageDraw.Draw(image)

            # Create a gradient background with shifting colors based on frame number
            for y in range(height):
                r = int(255 * (1 - y / height) * (1 - i / 10))
                g = int(200 * (y / height) * (i / 10))
                b = int(255 * (y / height) * (1 - i / 10))
                for x in range(width):
                    draw.point((x, y), fill=(r, g, b))

            # Add a slight animation effect by moving the text position
            offset_x = int(10 * math.sin(i * math.pi / 5))  # Sine wave movement
            offset_y = int(5 * math.cos(i * math.pi / 5))  # Cosine wave movement

            # Calculate starting Y position to center all lines vertically
            start_y = (height - total_text_height) // 2 + offset_y

            # Draw each line centered horizontally with shadow effect
            for j, line in enumerate(lines):
                bbox = font.getbbox(line)
                line_width = bbox[2] - bbox[0]
                position = (
                    (width - line_width) // 2 + offset_x,
                    int(start_y + j * line_height * 1.2),
                )

                # Draw shadow (offset by 2 pixels)
                draw.text(
                    (position[0] + 2, position[1] + 2), line, fill="black", font=font
                )
                # Draw text in white on top
                draw.text(position, line, fill="white", font=font)

            frames.append(image)

        # Save the frames as an animated GIF
        buffer = io.BytesIO()
        frames[0].save(
            buffer,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=100,  # 100ms per frame
            loop=0,  # Loop forever
        )
        return buffer.getvalue()

    #########################[ end generate_gif ]################################################

    #########################[ start _prepare_canvas ]########################################
    def _prepare_canvas(
        self,
        image_bytes: bytes,
        background_color: Union[str, Tuple[int, int, int]] = "white",
    ) -> Tuple[Image.Image, ImageDraw.ImageDraw, int, int]:
        """
        Load bytes into an image and return a blank canvas (same size) plus a draw
        context and its dimensions.

        Args:
            image_bytes: Raw image bytes.
            background_color: Fill colour for the new canvas.

        Returns:
            Tuple containing (blank canvas image, draw context, width, height).
        """
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        canvas = Image.new("RGB", (width, height), color=background_color)
        draw = ImageDraw.Draw(canvas)
        return canvas, draw, width, height

    #########################[ end _prepare_canvas ]########################################

    #########################[ start _select_font ]########################################
    def _select_font(
        self, font_name: str = "Arial", font_size: int = 36
    ) -> ImageFont.FreeTypeFont:
        """
        Safely select a truetype font, falling back to the default font if the
        requested face cannot be loaded. Uses a cache for efficiency.

        Args:
            font_name: Font family name.
            font_size: Desired point size.

        Returns:
            A PIL ImageFont object.
        """
        key = (font_name, font_size)
        if key in self.font_cache:
            return self.font_cache[key]
        try:
            font = ImageFont.truetype(font_name, font_size)
        except IOError:
            font = ImageFont.load_default()
        self.font_cache[key] = font
        return font


    #########################[ end _select_font ]########################################

    #########################[ start _center_position ]########################################
    def _center_position(
        self, text: str, font: ImageFont.FreeTypeFont, width: int, height: int
    ) -> Tuple[int, int]:
        """
        Calculate x, y coordinates that centre the supplied text.

        Args:
            text: The text string.
            font: Font used to measure the text.
            width: Canvas width.
            height: Canvas height.

        Returns:
            Tuple of (x, y) coordinates.
        """
        bbox = font.getbbox(text)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        return (width - text_w) // 2, (height - text_h) // 2

    #########################[ end _center_position ]########################################

    #########################[ start _finalise_image ]########################################
    def _finalise_image(self, img: Image.Image) -> bytes:
        """
        Convert a PIL Image into raw bytes using the class' configured format.

        Args:
            img: PIL Image instance.

        Returns:
            Image encoded as bytes.
        """
        buf = io.BytesIO()
        img.save(buf, format=self.format.upper())
        return buf.getvalue()

    #########################[ end _finalise_image ]################################################

    #########################[ start _ensure_text_fits ]##############################################
    def _ensure_text_fits(
        self,
        draw: ImageDraw.Draw,
        text: str,
        font: ImageFont.FreeTypeFont,
        width: int,
        height: int,
    ) -> ImageFont.FreeTypeFont:
        """
        Ensure text fits within the image by adjusting font size if needed.

        Args:
            draw: ImageDraw object
            text: Text to display
            font: Font to use
            width: Image width
            height: Image height

        Returns:
            ImageFont.FreeTypeFont: Adjusted font that ensures text fits
        """
        # Maximum width we want text to occupy (80% of image width)
        max_width = int(width * 0.8)
        max_height = int(height * 0.8)

        # Check if text is too long for a single line
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]

        # If text is too wide, we need to either wrap it or reduce font size
        if text_width > max_width:
            # Try to reduce font size first (for very long text)
            font_size = font.size
            while text_width > max_width and font_size > 12:  # Don't go below 12pt font
                font_size -= 2
                try:
                    font = ImageFont.truetype("Arial", font_size)
                except IOError:
                    # If we can't load the font, use default
                    font = ImageFont.load_default()
                    break

                bbox = font.getbbox(text)
                text_width = bbox[2] - bbox[0]

        return font

    #########################[ end _ensure_text_fits ]################################################

    #########################[ start _draw_text_with_wrapping ]##############################################
    def _draw_text_with_wrapping(
        self,
        draw: ImageDraw.Draw,
        text: str,
        font: ImageFont.FreeTypeFont,
        width: int,
        height: int,
    ) -> None:
        """
        Draw text on the image with wrapping if needed.

        Args:
            draw: ImageDraw object
            text: Text to display
            font: Font to use
            width: Image width
            height: Image height
        """
        # Maximum width we want text to occupy (80% of image width)
        max_width = int(width * 0.8)

        # Check if we need to wrap text
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]

        if text_width <= max_width:
            # Text fits on a single line, center it
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)
            draw.text(position, text, fill="black", font=font)
        else:
            # Need to wrap text
            words = text.split()
            lines = []
            current_line = []

            # Group words into lines that fit within max_width
            for word in words:
                # Try adding this word to the current line
                test_line = " ".join(current_line + [word])
                bbox = font.getbbox(test_line)
                test_width = bbox[2] - bbox[0]

                if test_width <= max_width:
                    # Word fits, add it to the current line
                    current_line.append(word)
                else:
                    # Word doesn't fit, start a new line
                    if current_line:  # Don't add empty lines
                        lines.append(" ".join(current_line))
                    current_line = [word]

            # Add the last line if it's not empty
            if current_line:
                lines.append(" ".join(current_line))

            # Calculate total height of all lines
            line_height = (
                font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
            )  # Approximate line height
            total_text_height = (
                len(lines) * line_height * 1.2
            )  # Add 20% for line spacing

            # Calculate starting Y position to center all lines vertically
            start_y = (height - total_text_height) // 2

            # Draw each line centered horizontally
            for i, line in enumerate(lines):
                bbox = font.getbbox(line)
                line_width = bbox[2] - bbox[0]
                position = (
                    (width - line_width) // 2,
                    int(start_y + i * line_height * 1.2),
                )
                draw.text(position, line, fill="black", font=font)

    #########################[ end _draw_text_with_wrapping ]################################################

    #########################[ start _draw_text_with_wrapping_and_shadow ]##############################################
    def _draw_text_with_wrapping_and_shadow(
        self,
        draw: ImageDraw.Draw,
        text: str,
        font: ImageFont.FreeTypeFont,
        width: int,
        height: int,
    ) -> None:
        """
        Draw text on the image with wrapping and shadow effect for better visibility.

        Args:
            draw: ImageDraw object
            text: Text to display
            font: Font to use
            width: Image width
            height: Image height
        """
        # Maximum width we want text to occupy (80% of image width)
        max_width = int(width * 0.8)

        # Need to wrap text
        words = text.split()
        lines = []
        current_line = []

        # Group words into lines that fit within max_width
        for word in words:
            # Try adding this word to the current line
            test_line = " ".join(current_line + [word])
            bbox = font.getbbox(test_line)
            test_width = bbox[2] - bbox[0]

            if test_width <= max_width:
                # Word fits, add it to the current line
                current_line.append(word)
            else:
                # Word doesn't fit, start a new line
                if current_line:  # Don't add empty lines
                    lines.append(" ".join(current_line))
                current_line = [word]

        # Add the last line if it's not empty
        if current_line:
            lines.append(" ".join(current_line))

        # Calculate total height of all lines
        line_height = (
            font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
        )  # Approximate line height
        total_text_height = len(lines) * line_height * 1.2  # Add 20% for line spacing

        # Calculate starting Y position to center all lines vertically
        start_y = (height - total_text_height) // 2

        # Draw each line centered horizontally with shadow effect
        for i, line in enumerate(lines):
            bbox = font.getbbox(line)
            line_width = bbox[2] - bbox[0]
            position = ((width - line_width) // 2, int(start_y + i * line_height * 1.2))

            # Draw shadow (offset by 2 pixels)
            draw.text((position[0] + 2, position[1] + 2), line, fill="black", font=font)
            # Draw text in white on top
            draw.text(position, line, fill="white", font=font)

    #########################[ end _draw_text_with_wrapping_and_shadow ]################################################


###################################[ end BonfireVisionEvasion ]##############################################
