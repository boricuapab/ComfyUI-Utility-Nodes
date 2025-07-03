class ListItemCount:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_list": ("ITEM_LIST",),
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("count",)
    FUNCTION = "count_items"
    CATEGORY = "Utilities"

    def count_items(self, input_list):
        return (len(input_list),)


NODE_CLASS_MAPPINGS = {
    "ListItemCount": ListItemCount,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListItemCount": "List Item Count",
}
