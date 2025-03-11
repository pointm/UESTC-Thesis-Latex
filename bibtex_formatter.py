import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter
from datetime import datetime


def format_bibtex(input_file, output_file):
    # 读取原始文件
    with open(input_file, "r", encoding="utf-8") as f:
        parser = BibTexParser(common_strings=True)
        bib_database = bibtexparser.load(f, parser=parser)

    # 字段排序规则
    field_order = {
        "thesis": [
            "address",
            "language",
            "author",
            "institution",
            "pages",
            "title",
            "year",
        ],
        "article": ["author", "journal", "number", "pages", "title", "volume", "year"],
        "conference": ["address", "author", "booktitle", "pages", "title", "year"],
        "techreport": ["address", "author", "date", "institution", "title"],
        "newspaper": ["author", "date", "journal", "title"],
        "patent": ["author", "country", "date", "id", "title", "type"],
        "standard": ["address", "date", "id", "institution", "publisher", "title"],
    }

    # 处理每个条目
    # 添加在format_bibtex函数内
    # 处理特殊字段类型
    for entry in bib_database.entries:
        # 专利号格式处理
        if entry["ENTRYTYPE"] == "patent" and "id" in entry:
            entry["id"] = entry["id"].upper().replace(" ", "")

        # 页码范围格式化（示例：50-60 -> 50-60）
        if "pages" in entry:
            entry["pages"] = entry["pages"].replace("--", "-").replace("～", "-")

        # 中文文献强制语言字段
        if any(char in entry.get("title", "") for char in ["，", "。", "、"]):
            entry["language"] = "zh"

        # 统一中文作者分隔符
        if "author" in entry:
            entry["author"] = entry["author"].replace(" and ", " and ")

        # 转换日期格式（示例：July 16, 2010 -> 2010年7月16日）
        if "date" in entry:
            try:
                dt = datetime.strptime(entry["date"], "%B %d, %Y")
                entry["date"] = dt.strftime("%Y年%m月%d日")
            except ValueError:
                pass

    # 写入格式化文件
    writer = BibTexWriter()
    writer.indent = "    "  # 4空格缩进
    writer.comma_first = False
    writer.align_values = True

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(writer.write(bib_database))


# 使用示例
format_bibtex(
    r"C:\Users\Pachirisu\Documents\GithubWorkSpace\UESTC-Thesis-Latex\问题与解决方案\input.bib",
    r"C:\Users\Pachirisu\Documents\GithubWorkSpace\UESTC-Thesis-Latex\问题与解决方案\output.bib",
)
