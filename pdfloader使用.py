from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./data/pdf2.pdf",mode="page",password="itheima")

i=0
for doc in loader.load():
    print(doc)
    i+=1
    print("="*20,"第",i,"页",sep="")






