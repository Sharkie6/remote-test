# 导入文本加载器
from langchain_community.document_loaders import TextLoader

# 导入文本分割器
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. 加载 txt 文件
loader = TextLoader(
    "./data/python基础语法.txt",
    encoding="utf-8"
)
docs = loader.load()

# 2. 创建分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
    separators=["\n\n", "\n", " ", "", ".", "。", "?"]
)

# 3. 分割文档
docs = text_splitter.split_documents(docs)

# 4. 输出结果
print(docs)