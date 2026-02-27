import torch

class IsImageEmpty:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ("BOOLEAN", "IMAGE", "INT",)
    RETURN_NAMES = ("Is Empty", "image", "int", "int_switch",)
    FUNCTION = "check_none"
    CATEGORY = "Cmfy_Utls"

    def check_none(self, image=None):

        is_invalid = image is None

        int_val = 1 if is_invalid else 0

        int_switch = int_val + 1

        if is_invalid:
            out_image = torch.zeros((1, 32, 32, 3), dtype=torch.float32)
        else:
            out_image = image

        return (out_image, is_invalid, int_val, int_switch,)

# Register the node in ComfyUI
NODE_CLASS_MAPPINGS = {
    "IsImageEmpty": IsImageEmpty,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IsImageEmpty": "Is Image Empty",
}
