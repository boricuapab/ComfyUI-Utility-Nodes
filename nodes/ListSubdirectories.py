import os

class ListSubdirectories:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "root_dir": ("STRING", {"default": "./"}),
                "depth_limit": ("INT", {"default": -1, "min": -1}),
                "pattern_filter": ("STRING", {"default": ""}),
                "case_sensitive": ("BOOLEAN", {"default": True}),
                "load_cap": ("INT", {"default": 100, "min": 1}),
                "load_offset": ("INT", {"default": 0, "min": 0}),
                "index": ("INT", {"default": 0, "min": 0}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("subdirectory_paths", "indexed_path")
    FUNCTION = "list_dirs"
    CATEGORY = "Cmfy_Utls"
    OUTPUT_IS_LIST = (True, False)

    def list_dirs(self, root_dir, depth_limit, pattern_filter, case_sensitive, load_cap, load_offset, index ):
        if not os.path.isdir(root_dir):
            return ([f"Invalid directory: {root_dir}"], "")

        subdirs = []
        root_depth = root_dir.rstrip(os.sep).count(os.sep)

        include_groups = []
        exclude_patterns = []

        if pattern_filter:
            raw_patterns = [p.strip() for p in pattern_filter.split(',') if p.strip()]
            for p in raw_patterns:
                if p.startswith('^'):
                    exclude_patterns.append(p[1:])
                else:
                    include_groups.append([s.strip() for s in p.split('&&') if s.strip()])

        for dirpath, dirnames, _ in os.walk(root_dir):
            current_depth = dirpath.rstrip(os.sep).count(os.sep) - root_depth
            if depth_limit != -1 and current_depth >= depth_limit:
                dirnames[:] = []  # prevent deeper walk
                continue

            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                abs_path = os.path.abspath(full_path)
                rel_path = os.path.relpath(abs_path, root_dir)
                path_to_match = rel_path if case_sensitive else rel_path.lower()

                match_exclude = exclude_patterns if case_sensitive else [p.lower() for p in exclude_patterns]
                exclude_hit = any(p in path_to_match for p in match_exclude)
                if exclude_hit:
                    continue

                if include_groups:
                    group_match = False
                    for group in include_groups:
                        match_group = group if case_sensitive else [p.lower() for p in group]
                        if all(p in path_to_match for p in match_group):
                            group_match = True
                            break
                    if not group_match:
                        continue

                subdirs.append(abs_path)

        # Clamp slicing bounds within valid range, apply offset only if cap < total
        total = len(subdirs)
        if load_cap < total:
            start = min(load_offset, total)
            end = min(load_offset + load_cap, total)
            subdirs = subdirs[start:end]
        else:
            subdirs = subdirs[:total]

        safe_index = min(max(index, 0), len(subdirs) - 1) if subdirs else 0
        indexed_path = subdirs[safe_index] if subdirs else ""

        subdirs = [str(path) for path in subdirs]
        return (subdirs, indexed_path)


NODE_CLASS_MAPPINGS = {
    "ListSubdirectories": ListSubdirectories,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ListSubdirectories": "List Subdirectories",
}
