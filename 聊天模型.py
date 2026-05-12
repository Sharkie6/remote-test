from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.llms.tongyi import Tongyi

# 聊天模型
model=ChatTongyi(model="qwen3-max")

# 消息列表
messages=[
    ("system","你是一个浪漫主义诗人"),
    ("human","来首唐诗"),
    ("ai","我将奉上一首李白的诗"),
]

# 调用流式执行
res=model.stream(input=messages)

# for循环迭代输出
for chunk in res:
    print(chunk.content,end="",flush=True)