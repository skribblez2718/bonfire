from bonfire.utils.bon import BonfireTextEvasionBoN
from bonfire.utils.language import BonfireTextEvasionLanguage
from bonfire.utils.whitespace import BonfireTextEvasionWhitespace
from bonfire.utils.encode import BonfireTextEvasionEncode
from bonfire.utils.reverse import BonfireTextEvasionReverse
from bonfire.utils.decorate import BonfireTextEvasionDecorate
from bonfire.utils.sound import BonfireSoundManipulate
from bonfire.utils.image import BonfireImageManipulate

text_augmentations = [
    BonfireTextEvasionBoN.word_scrambling_random,
    BonfireTextEvasionBoN.capitalization_random,
    BonfireTextEvasionBoN.character_noising_random,
    BonfireTextEvasionLanguage.add_diacritics_random,
    BonfireTextEvasionLanguage.add_diacritics_all,
    BonfireTextEvasionLanguage.convert_to_l33t_random,
    BonfireTextEvasionLanguage.convert_to_l33t_all,
    BonfireTextEvasionLanguage.convert_to_futhark_random,
    BonfireTextEvasionLanguage.convert_to_futhark_all,
    BonfireTextEvasionLanguage.convert_to_medieval_random,
    BonfireTextEvasionLanguage.convert_to_medieval_all,
    BonfireTextEvasionLanguage.convert_morse_random,
    BonfireTextEvasionLanguage.convert_morse_all,
    BonfireTextEvasionWhitespace.add_spaces_random,
    BonfireTextEvasionWhitespace.add_spaces_all,
    BonfireTextEvasionWhitespace.add_zero_width_spaces_random,
    BonfireTextEvasionWhitespace.add_zero_width_spaces_all,
    BonfireTextEvasionWhitespace.newline_random,
    BonfireTextEvasionWhitespace.newline_all,
    BonfireTextEvasionEncode.similar_unicode_chars_random,
    BonfireTextEvasionEncode.similar_unicode_chars_all,
    BonfireTextEvasionEncode.math_symbols_random,
    BonfireTextEvasionEncode.math_symbols_all,
    BonfireTextEvasionEncode.base64_chars_random,
    BonfireTextEvasionEncode.base64_text_all,
    BonfireTextEvasionEncode.base64_words_all,
    BonfireTextEvasionEncode.base64_words_random,
    BonfireTextEvasionEncode.hex_encoding_random,
    BonfireTextEvasionEncode.hex_encoding_all,
    BonfireTextEvasionEncode.binary_encoding_random,
    BonfireTextEvasionEncode.binary_encoding_all,
    BonfireTextEvasionEncode.html_entities_random,
    BonfireTextEvasionEncode.html_entities_all,
    BonfireTextEvasionEncode.emoji_variation_selectors_all,
    BonfireTextEvasionEncode.emoji_variation_selectors_random,
    BonfireTextEvasionEncode.zalgo_random,
    BonfireTextEvasionEncode.zalgo_all,
    BonfireTextEvasionEncode.circled_random,
    BonfireTextEvasionEncode.circled_all,
    BonfireTextEvasionEncode.bubble_random,
    BonfireTextEvasionEncode.bubble_all,
    BonfireTextEvasionReverse.sentence_reverse_all,
    BonfireTextEvasionReverse.sentence_reverse_random,
    BonfireTextEvasionReverse.word_reverse_all,
    BonfireTextEvasionReverse.word_reverse_random,
    BonfireTextEvasionReverse.word_upside_down_all,
    BonfireTextEvasionReverse.word_upside_down_random,
    BonfireTextEvasionReverse.char_upside_down_random,
    BonfireTextEvasionReverse.word_mirrored_all,
    BonfireTextEvasionReverse.word_mirrored_random,
    BonfireTextEvasionReverse.char_mirrored_random,
    BonfireTextEvasionDecorate.make_wavy_random,
    BonfireTextEvasionDecorate.make_wavy_all,
    BonfireTextEvasionDecorate.make_strikethrough_random,
    BonfireTextEvasionDecorate.make_strikethrough_all,
    BonfireTextEvasionDecorate.make_fullwidth_random,
    BonfireTextEvasionDecorate.make_fullwidth_all,
    BonfireTextEvasionDecorate.make_wide_space_random,
    BonfireTextEvasionDecorate.make_wide_space_all,
]

text_augmentations_for = {
    "audio": [
        BonfireTextEvasionBoN.word_scrambling_random,
        BonfireTextEvasionBoN.capitalization_random,
        BonfireTextEvasionBoN.character_noising_random,
    ],
    "image": [
        BonfireTextEvasionBoN.word_scrambling_random,
        BonfireTextEvasionBoN.capitalization_random,
        BonfireTextEvasionBoN.character_noising_random,
    ],
}

audio_augmentations = [
    BonfireSoundManipulate.change_speed,
    BonfireSoundManipulate.change_pitch,
    BonfireSoundManipulate.change_volume,
    BonfireSoundManipulate.add_noise,
    BonfireSoundManipulate.add_noise,
]

image_augmentations = [
    BonfireImageManipulate.change_text_font_all,
    BonfireImageManipulate.change_text_font_random,
    BonfireImageManipulate.change_text_color_all,
    BonfireImageManipulate.change_text_color_random,
    BonfireImageManipulate.change_text_position_all,
    BonfireImageManipulate.change_text_position_random,
    BonfireImageManipulate.change_text_size_all,
    BonfireImageManipulate.change_text_size_random,
    BonfireImageManipulate.change_background_pixels_all,
    BonfireImageManipulate.change_background_pixels_random,
    BonfireImageManipulate.change_background_color_all,
    BonfireImageManipulate.change_background_color_random,
]
