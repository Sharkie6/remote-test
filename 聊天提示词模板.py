from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.output_parsers import  StrOutputParser,JsonOutputParser

Chat_prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","你是一个情感陪伴机器人"),
        MessagesPlaceholder("history"),
        ("human","我最近学业压力很大")
    ]
)



history_data=[
    ("human","我有点不开心"),
    ("ai","去吃点好吃的吧！")
]

parse=StrOutputParser()
json_prompt=JsonOutputParser()
model=ChatTongyi(model="qwen3-max")

chain=Chat_prompt_template | model |parse |model
res=chain.invoke({"history":history_data})
print(res.content)