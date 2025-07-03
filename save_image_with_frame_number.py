import os
import re
from PIL import Image
import numpy as np
import torch

class SaveImageForEach:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "directory": ("STRING", {"default": "output"}),
                "name": ("STRING", {"default": "image"}),
                "frame_number": ("INT", {"default": 0, "min": 0}),
                "use_next_available": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    FUNCTION = "save_image"
    CATEGORY = "image/save"

    def get_next_available_frame(self, directory, name):
        max_frame = -1
        pattern = re.compile(rf"{re.escape(name)}\.(\d{{4}})\.png")
        try:
            for fname in os.listdir(directory):
                match = pattern.fullmatch(fname)
                if match:
                    frame_num = int(match.group(1))
                    max_frame = max(max_frame, frame_num)
        except FileNotFoundError:
            pass
        return max_frame + 1

    def save_image(self, image, directory, name, frame_number, use_next_available):
        # Ensure directory exists
        os.makedirs(directory, exist_ok=True)

        # Use next available frame if toggled
        if use_next_available:
            frame_number = self.get_next_available_frame(directory, name)

        # Convert input to list of images if not already
        images = image if isinstance(image, list) else [image]

        saved_paths = []
        for idx, img in enumerate(images):
            frame_idx = frame_number + idx
            output_path = os.path.join(directory, f"{name}.{frame_idx:04d}.png")
            saved_paths.append(os.path.abspath(output_path))

            # Convert Torch tensor to NumPy, then to PIL
            if isinstance(img, torch.Tensor):
                img = img.squeeze(0).cpu().numpy()  # remove batch dim if present

            if img.ndim == 3 and img.shape[0] in [1, 3]:
                # Convert CHW to HWC
                img = np.transpose(img, (1, 2, 0))

            # Clip and convert to uint8
            img = (np.clip(img, 0, 1) * 255).astype(np.uint8)

            # Handle grayscale or color
            if img.ndim == 2:
                pil_img = Image.fromarray(img, mode="L")
            elif img.shape[2] == 1:
                pil_img = Image.fromarray(img[:, :, 0], mode="L")
            else:
                pil_img = Image.fromarray(img, mode="RGB")

            pil_img.save(output_path)

        result_str = "\n".join(saved_paths)
        return (image, result_str)

NODE_CLASS_MAPPINGS = {
    "SaveImageForEach": SaveImageForEach
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveImageForEach": "Save Image for Each"
}
