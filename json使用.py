from langchain_community.document_loaders import JSONLoader

laoder = JSONLoader(
    file_path="./data/stu_json_lines.json",
    jq_schema=".name",
    json_lines=True,
    text_content=False,
)

documents = laoder.load()
print(documents)