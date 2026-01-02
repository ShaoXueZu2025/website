import os
import re
import sys

CONFIG_REGEX = (
    r"<!-- AUTOGEN CONFIG START -->([\s\S]*)<!-- AUTOGEN CONFIG END -->"
)
CONFIG_ITEM_REGEX = r"<!-- (LIST|IGNORE|HEADER): \[(.+)\] -->"
AUTOGEN_REGEX = (
    r"<!-- AUTOGEN CONTENT START -->([\s\S]*)<!-- AUTOGEN CONTENT END -->"
)


def find_md_files(root_dir):
    """
    遍历指定目录，找出所有.md文件
    """
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                md_files.append((root, file))
    return md_files


def gen_github_link(root, file):
    link = root.replace("\\", "/").replace("docs/", "") + "/" + file
    return f"https://github.com/ShaoXueZu2025/website/raw/refs/heads/main/docs/{link}"


def gen_line(operation, data, root):
    if operation == "LIST":
        if os.path.splitext(data)[1] == ".pdf":
            return (
                f'??? note "{data} <a href="./{data}" download>[下载]</a> <a href="{gen_github_link(root, data)}" download>[GitHub下载]</a>"\n'
                f'    <iframe loading="lazy" src="{data}" width="100%" height="500px"></iframe>\n\n'
            )
        else:
            return (
                f'!!! note "{data} <a href="./{data}" download>[下载]</a> <a href="{gen_github_link(root, data)}" download>[GitHub下载]</a>"\n\n'
            )
    elif operation == "IGNORE":
        return ""
    elif operation == "HEADER":
        return f'<h2 id="{data}">{data}</h2>\n\n'


def generate_lists():
    docs_dir = "docs"
    md_files = find_md_files(docs_dir)
    for root, file in md_files:
        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
            content = f.read()
        if content.find("<!-- GEN -->") >= 0:
            print(f"{os.path.join(root, file)} has GEN FileList")
            content = content.replace(
                "<!-- GEN -->",
                (
                    "<!-- AUTOGEN CONFIG START -->\n"
                    "<!-- AUTOGEN CONFIG END --\n>"
                    "<!-- AUTOGEN CONTENT START -->\n"
                    "<!-- AUTOGEN CONTENT END -->",
                ),
            )

        match = re.search(CONFIG_REGEX, content)
        dir_files = os.listdir(root)
        dir_files = [name for name in dir_files if not name.endswith(".md")]
        existing_configs = []
        if not match:
            continue

        if not re.search(AUTOGEN_REGEX, content):
            raise Exception(f"{os.path.join(root, file)} has no content")

        config = match.group(1)
        files = [(m[0], m[1]) for m in re.findall(CONFIG_ITEM_REGEX, config)]
        for operation, name in files:
            if operation == "HEADER":
                existing_configs.append((operation, name))
                continue
            if name not in dir_files:
                raise Exception(
                    f"{name} not found in {root}, {os.path.join(root, file)}"
                )
            dir_files.remove(name)
            existing_configs.append((operation, name))

        final_config = existing_configs + [
            ("LIST", name) for name in dir_files
        ]

        generated_configs = (
            "<!-- AUTOGEN CONFIG START -->\n"
            + "\n".join(
                (
                    f"<!-- {operation}: [{name}] -->"
                    for operation, name in final_config
                ),
            )
            + "\n<!-- AUTOGEN CONFIG END -->"
        )

        content = re.sub(CONFIG_REGEX, generated_configs, content)

        # Generate content

        content = re.sub(
            AUTOGEN_REGEX,
            "<!-- AUTOGEN CONTENT START -->\n"
            "<!-- THESE CONTENT BETWEEN START & END TAGS ARE AUTO GENERATED. DO NOT EDIT!!! -->\n"
            "<!-- 这些内容是自动生成的喵，所有修改该都可能在未加确认的情况下直接覆盖喵，不要编辑喵!!! -->\n"
            + "".join(
                [
                    gen_line(operation, name, root)
                    for operation, name in final_config
                ]
            )
            + '\n!!! tip "使用提示"\n'
            "    点击“下载”以下载相应文件，部分文件可以展开文件查看详情。手机端预览功能可能不兼容，建议下载后浏览。"
            "DOCX文件建议下载后使用Word或兼容软件打开。\n\n"
            "<!-- AUTOGEN CONTENT END -->",
            content,
        )

        with open(os.path.join(root, file), "w", encoding="utf-8") as f:
            f.write(content)


def remove_lists():
    docs_dir = "docs"
    md_files = find_md_files(docs_dir)
    for root, file in md_files:
        with open(os.path.join(root, file), "r", encoding="utf-8") as f:
            content = f.read()

            content = re.sub(
                AUTOGEN_REGEX,
                "<!-- AUTOGEN CONTENT START -->\n<!-- AUTOGEN CONTENT END -->",
                content,
            )
            with open(os.path.join(root, file), "w", encoding="utf-8") as f:
                f.write(content)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "remove":
        remove_lists()
    else:
        generate_lists()
