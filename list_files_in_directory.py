import os

class ListFiles:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "directory": ("STRING", {"default": "./"}),
                "filter": ("STRING", {"default": ""}),
                "case_sensitive": ("BOOLEAN", {"default": True}),
                "load_cap": ("INT", {"default": -1, "min": -1}),
                "index": ("INT", {"default": 0, "min": 0})
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("file_list", "indexed_path")
    FUNCTION = "list_files"
    CATEGORY = "Filesystem"
    OUTPUT_IS_LIST = (True, False)

    def list_files(self, directory, filter, case_sensitive, load_cap, index):
        if not os.path.isdir(directory):
            return ([f"Invalid directory: {directory}"], "")

        filters = [f.strip() for f in filter.split(',') if f.strip()] if filter else []
        include_filters = [f for f in filters if not f.startswith('^')]
        exclude_filters = [f[1:] for f in filters if f.startswith('^')]

        if not case_sensitive:
            include_filters = [f.lower() for f in include_filters]
            exclude_filters = [f.lower() for f in exclude_filters]

        files = []
        unlimited = load_cap == -1

        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                if not unlimited and len(files) >= load_cap:
                    break
                check_name = filename if case_sensitive else filename.lower()
                if (
                    (not include_filters or any(f in check_name for f in include_filters))
                    and not any(f in check_name for f in exclude_filters)
                ):
                    full_path = os.path.abspath(os.path.join(root, filename))
                    files.append(full_path)
            if not unlimited and len(files) >= load_cap:
                break

        # Clamp index to valid range
        safe_index = min(max(index, 0), len(files) - 1) if files else 0
        indexed_path = files[safe_index] if files else ""

        return (files, indexed_path)

NODE_CLASS_MAPPINGS = {
    "ListFiles": ListFiles,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListFiles": "List Files",
}
