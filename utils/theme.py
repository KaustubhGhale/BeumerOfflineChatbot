# utils/theme.py
class Theme:
    """
    Defines the color palette and font styles for the Beumer Chatbot application,
    inspired by the provided Beumer branding images.
    """
    # Beumer Brand Colors (approximated from images)
    PRIMARY_COLOR = "#004080"  # Dark Blue (e.g., header background)
    ACCENT_COLOR = "#007bff"   # Lighter Blue (e.g., buttons, highlights)
    BACKGROUND_COLOR = "#f0f2f5" # Light Grey/Off-white for main background
    CARD_BACKGROUND_COLOR = "#ffffff" # White for cards/content areas
    TEXT_COLOR = "#333333"     # Dark grey for general text
    LIGHT_TEXT_COLOR = "#666666" # Lighter grey for secondary text
    BORDER_COLOR = "#cccccc"   # Light grey for borders
    SUCCESS_COLOR = "#28a745"  # Green for success messages
    ERROR_COLOR = "#dc3545"    # Red for error messages
    INFO_COLOR = "#17a2b8"     # Cyan for info messages

    # Fonts
    FONT_FAMILY = "Inter" # A clean, modern sans-serif font
    FONT_SIZE_LARGE = 14
    FONT_SIZE_MEDIUM = 11
    FONT_SIZE_SMALL = 9

    # Padding and Spacing
    PADDING_LARGE = 20
    PADDING_MEDIUM = 10
    PADDING_SMALL = 5
    MARGIN_LARGE = 20
    MARGIN_MEDIUM = 10

