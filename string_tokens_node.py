class StringTokens:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": False, "default": "Enter your text here."}),
                "tokenizer_splitter": ("STRING", {"default": " "}),
                "index": ("INT", {"default": 0, "min": -999}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("Tokens List", "Indexed Token", "token_count")
    FUNCTION = "tokenize"
    CATEGORY = "Text Processing"
    OUTPUT_IS_LIST = (True, False, False)

    def tokenize(self, input_text, tokenizer_splitter, index):
        if isinstance(input_text, list):
            tokens = input_text
        else:
            if not tokenizer_splitter:
                tokenizer_splitter = " "
            tokens = input_text.split(tokenizer_splitter)
            tokens = [t.strip() for t in tokens if t.strip()]  # Remove empty tokens & whitespace

        token_count = len(tokens)

        if token_count == 0:
            return ([], "-1", -1)

        # Get indexed token with bounds check
        if -len(tokens) <= index < len(tokens):
            indexed_token = tokens[index]
        else:
            indexed_token = tokens[-1]

        return (tokens, indexed_token, token_count)


NODE_CLASS_MAPPINGS = {
    "StringTokens": StringTokens,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StringTokens": "String Tokens",
}
