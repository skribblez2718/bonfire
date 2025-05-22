import base64
import math
import io
from typing import Callable, Optional, List, Dict, Any

from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont

from bonfire.utils.augment import BonfireEvasion
from bonfire.utils.logger import BonfireLogger
from bonfire.config.config import image_augmentations, text_augmentations_for


###################################[ start BonfireVisionEvasion ]###################################
class BonfireVisionEvasion(BonfireEvasion):
    """
    Class for vision augmentation with various methods to modify visual data.
    """

    #########################[ start __init__ ]#########################
    def __init__(
        self,
        prompts: List[Dict[str, Any]],
        output_file_path: Optional[str],
        format: str,
    ) -> None:
        # Initialize logger
        self.logger = BonfireLogger("BonfireVisionEvasion")

        super().__init__(
            data=prompts,
            output_file_path=output_file_path,
        )
        self.name: str = "BonfireVisionEvasion"
        self.format: str = format.lower()  # png | jpeg | gif

        # List of available fonts for text manipulation methods (reduced to common fonts)
        self.available_fonts = [
            "Arial",
            "Courier New",
            "Times New Roman",
            "Verdana",
            "DejaVuSans",
            "LiberationSans",
        ]
        # Font cache for fast repeated loading
        self.font_cache = {}

    #########################[ end __init__ ]###########################

    #########################[ start apply ]############################
    def apply(self) -> List[Dict[str, Any]]:
        """
        Apply all available text and image augmentation methods to the given data

        Returns:
            List of dictionaries describing original and augmented images.
        """
        results: List[Dict[str, Any]] = []
        image_methods = self.get_available_image_methods()
        text_methods = self.get_available_text_methods()

        for prompt_obj in tqdm(self.data, desc="Generating vision payloads"):
            intent = prompt_obj["intent"]
            method = prompt_obj["method"]
            method_name = prompt_obj["method_name"]
            prompt_name = prompt_obj["prompt_name"]
            prompt_text = prompt_obj["prompt"]

            def _make_vision_result(
                intent,
                method,
                method_name,
                prompt_name,
                text_augmentation,
                image_augmentation,
                original_text,
                prompt_text,
                original_image,
                augmented_image,
            ):
                return {
                    "intent": intent,
                    "method": method,
                    "method_name": method_name,
                    "prompt_name": prompt_name,
                    "text_augmentation": text_augmentation,
                    "image_augmentation": image_augmentation,
                    "original_text": original_text,
                    "prompt_text": prompt_text,
                    "original_image": original_image,
                    "augmented_image": augmented_image,
                }

            def _apply_vision_augmentations(
                intent,
                method,
                method_name,
                prompt_name,
                prompt_text,
                text_methods,
                image_methods,
            ):
                aug_results = []
                # ── 1. Prompt is a LIST ──────────────────────────────────
                if isinstance(prompt_text, list):
                    for text_method in text_methods:
                        augmented_prompts = [text_method(pt) for pt in prompt_text]
                        augmented_image_bytes_list = [
                            self.generate_image(pt, self.format)
                            for pt in augmented_prompts
                        ]
                        augmented_base64_list = [
                            base64.b64encode(img).decode("utf-8")
                            for img in augmented_image_bytes_list
                        ]
                        for image_method in image_methods:
                            aug_img_base64_list = []
                            for img_bytes, aug_prompt in zip(
                                augmented_image_bytes_list, augmented_prompts
                            ):
                                try:
                                    aug_bytes = image_method(
                                        img_bytes,
                                        prompt_text=aug_prompt,
                                        logger=self.logger,
                                    )
                                    if aug_bytes is None:
                                        self.logger.warning(
                                            f"{image_method.__name__} returned None, skipping"
                                        )
                                        aug_img_base64_list.append(None)
                                        continue
                                    if isinstance(aug_bytes, bytes):
                                        aug_img_base64 = base64.b64encode(
                                            aug_bytes
                                        ).decode("utf-8")
                                        aug_img_base64_list.append(aug_img_base64)
                                    else:
                                        self.logger.warning(
                                            f"{image_method.__name__} returned non-bytes, skipping"
                                        )
                                        aug_img_base64_list.append(None)
                                        continue
                                except Exception as exc:
                                    self.logger.error(
                                        f"Error applying {image_method.__name__}: {exc}"
                                    )
                                    aug_img_base64_list.append(None)
                            aug_results.append(
                                _make_vision_result(
                                    intent,
                                    method,
                                    method_name,
                                    prompt_name,
                                    text_method.__name__,
                                    image_method.__name__,
                                    prompt_text,
                                    augmented_prompts,
                                    augmented_base64_list,
                                    aug_img_base64_list,
                                )
                            )
                # ── 2. Prompt is a STRING ───────────────────────────────
                else:
                    for text_method in text_methods:
                        augmented_prompt = text_method(prompt_text)
                        augmented_image_bytes = self.generate_image(
                            augmented_prompt, self.format
                        )
                        augmented_base64 = base64.b64encode(
                            augmented_image_bytes
                        ).decode("utf-8")
                        for image_method in image_methods:
                            try:
                                aug_bytes = image_method(
                                    augmented_image_bytes,
                                    prompt_text=augmented_prompt,
                                    logger=self.logger,
                                )
                                if aug_bytes is None:
                                    self.logger.warning(
                                        f"{image_method.__name__} returned None, skipping"
                                    )
                                    continue
                                if not isinstance(aug_bytes, bytes):
                                    self.logger.warning(
                                        f"{image_method.__name__} returned non-bytes, skipping"
                                    )
                                    continue
                                aug_img_base64 = base64.b64encode(aug_bytes).decode(
                                    "utf-8"
                                )
                                aug_results.append(
                                    _make_vision_result(
                                        intent,
                                        method,
                                        method_name,
                                        prompt_name,
                                        text_method.__name__,
                                        image_method.__name__,
                                        prompt_text,
                                        augmented_prompt,
                                        augmented_base64,
                                        aug_img_base64,
                                    )
                                )
                            except Exception as exc:
                                self.logger.error(
                                    f"Error applying {image_method.__name__}: {exc}"
                                )
                return aug_results

            # ── Baseline (no augmentation) ──────────────────────────────
            if isinstance(prompt_text, list):
                original_image_bytes_list = [
                    self.generate_image(pt, self.format) for pt in prompt_text
                ]
                original_base64_list = [
                    base64.b64encode(img).decode("utf-8")
                    for img in original_image_bytes_list
                ]
                results.append(
                    _make_vision_result(
                        intent,
                        method,
                        method_name,
                        prompt_name,
                        "None",
                        "None",
                        prompt_text,
                        prompt_text,
                        original_base64_list,
                        original_base64_list,
                    )
                )
            else:
                original_image_bytes = self.generate_image(prompt_text, self.format)
                original_base64 = base64.b64encode(original_image_bytes).decode("utf-8")
                results.append(
                    _make_vision_result(
                        intent,
                        method,
                        method_name,
                        prompt_name,
                        "None",
                        "None",
                        prompt_text,
                        prompt_text,
                        original_base64,
                        original_base64,
                    )
                )
            # ── Augmented versions ───────────────────────────────────────
            results.extend(
                _apply_vision_augmentations(
                    intent,
                    method,
                    method_name,
                    prompt_name,
                    prompt_text,
                    text_methods,
                    image_methods,
                )
            )

        self.logger.info(f"Generated {len(results)} augmented images")
        return results

    #########################[ end apply ]##############################

    #########################[ start get_available_image_methods ]######
    def get_available_image_methods(self) -> List[Callable]:
        """
        Return a list of all augmentation callables.
        """
        available_image_methods = list(image_augmentations)
        available_image_methods.append(self.all_random_image_methods)
        return available_image_methods

    #########################[ end get_available_image_methods ]########

    #########################[ start get_available_text_methods ]########
    def get_available_text_methods(self) -> list:
        """
        Get a list of available text augmentation methods from config.
        """
        available_methods = list(text_augmentations_for["image"])
        available_methods.append(self.all_random_text_methods)
        return available_methods

    #########################[ end get_available_text_methods ]##########

    #########################[ start all_random_text_methods ]##########
    def all_random_text_methods(self, text: str) -> str:
        """
        Apply all available random augmentation methods to the given text.
        Only applies methods ending in '_random'.
        """
        result = text
        methods = [
            m
            for m in self.get_available_text_methods()
            if m.__name__.endswith("_random") and m != self.all_random_text_methods
        ]
        for method in methods:
            result = method(result)
        return result

    #########################[ end all_random_text_methods ]############

    #########################[ start all_random_image_methods ]##########
    def all_random_image_methods(
        self,
        image: bytes,
        *,
        prompt_text: Optional[str] = None,
        logger: Optional[BonfireLogger] = None,
    ) -> bytes:
        """
        Apply every *_random image-augmentation method in sequence.
        """
        result = image
        methods = [
            m
            for m in self.get_available_image_methods()
            if m.__name__.endswith("_random") and m != self.all_random_image_methods
        ]
        for method in methods:
            try:
                result = method(
                    result, prompt_text=prompt_text, logger=logger or self.logger
                )
            except Exception as exc:  # pragma: no cover
                (logger or self.logger).error(
                    f"Error applying {method.__name__} inside all_random_image_methods: {exc}"
                )
        return result

    #########################[ end all_random_image_methods ]############

    #########################[ start generate_image ]####################
    def generate_image(self, text: str, format: str = "png") -> bytes:
        """
        Generate an image with the specified text based on the format.
        """
        if format.lower() == "png":
            return self.generate_png(text)
        elif format.lower() == "jpeg":
            return self.generate_jpeg(text)
        elif format.lower() == "gif":
            return self.generate_gif(text)
        # Fallback
        return self.generate_png(text)

    #########################[ end generate_image ]######################

    #########################[ start generate_png ]######################
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
        # self._ensure_text_fits(draw, text, font, width, height)
        self._ensure_text_fits(text, font, width)

        # Draw text on the image (with wrapping if needed)
        self._draw_text_with_wrapping(draw, text, font, width, height)

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    #########################[ end generate_png ]########################

    #########################[ start generate_jpeg ]#####################
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
        # font = self._ensure_text_fits(draw, text, font, width, height)
        font = self._ensure_text_fits(text, font, width)
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
            self.draw_wrapping_and_shadow(draw, text, font, width, height)

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=95)
        return buffer.getvalue()

    #########################[ end generate_jpeg ]#######################

    #########################[ start generate_gif ]######################
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
        # font = self._ensure_text_fits(temp_draw, text, font, width, height)
        font = self._ensure_text_fits(text, font, width)

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

    #########################[ end generate_gif ]########################

    #########################[ start _ensure_text_fits ]#################
    def _ensure_text_fits(
        self,
        # draw: ImageDraw.Draw,
        text: str,
        font: ImageFont.FreeTypeFont,
        width: int,
        # height: int,
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

    #########################[ end _ensure_text_fits ]###################

    #########################[ start _draw_text_with_wrapping ]##########
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

    #########################[ end _draw_text_with_wrapping ]############

    #########################[ start draw_wrapping_and_shadow ]##########
    @staticmethod
    def draw_wrapping_and_shadow(
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

    #########################[ end draw_wrapping_and_shadow ]############


###################################[ end BonfireVisionEvasion ]#####################################
