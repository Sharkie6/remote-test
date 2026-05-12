from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="./data/stu.csv",
    csv_args={
        "delimiter": ",",#指定分隔符
        "quotechar": "“",#指定带有分隔符的引号包围是单引号还是双引号
    },
    encoding="utf-8"  # 关键修复
)

for document in loader.load():
    print(document)

for document in loader.lazy_load():
    print(document)