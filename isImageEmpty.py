class IsImageEmpty:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("Is Empty",)
    FUNCTION = "check_none"
    CATEGORY = "Utilities"

    def check_none(self, image=None):
        """
        Returns True if the image is None or not found (is_invalid).
        """
        is_invalid = image is None
        return (is_invalid,)

# Register the node in ComfyUI
NODE_CLASS_MAPPINGS = {
    "IsImageEmpty": IsImageEmpty,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsImageEmpty": "Is Image Empty",
}
