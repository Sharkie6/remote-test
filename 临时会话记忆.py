from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import  StrOutputParser,JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


store={} #key是session,value是InMemoryChatMessageHistory类对象

def get_history(session_id):
    global store
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()

    return store[session_id]

model=ChatTongyi(model="qwen3-max")
prompt=ChatPromptTemplate.from_messages(
    [
    ("system","请根据会话历史回答用户问题,对话历史:{chat_history}"),
    MessagesPlaceholder("chat_history"),
    ("human","请回答以下问题:{input}")
    ]

)

def print_prompt(full_prompt):

    print("="*20+"\n",full_prompt.to_string(),"\n"+"="*20)
    return full_prompt


str_parser=StrOutputParser()

base_chain=prompt | print_prompt | model | str_parser

# 创建一个新链，对原有的链增强功能：自动附加历史消息
conversation_chain=RunnableWithMessageHistory(
    base_chain, #被增强的原chain
    get_history, #通过会话ID获取InMemoryChatMessageHistory类对象
    input_messages_key="input", #用户输入在模板中的占位符
    history_messages_key="chat_history", #历史消息在模板中的占位符
)

if __name__ == '__main__':
    # 为当前程序配置所属的session_id
    session_config={
        "configurable":{
            "session_id":"user_001"
        }
    }


    res=conversation_chain.invoke({"input":"今天吃了一根雪糕"},session_config)
    print("第一次执行",res)
    res = conversation_chain.invoke({"input": "昨天吃了一根雪糕"}, session_config)
    print("第二次执行",res)
    res = conversation_chain.invoke({"input": "一共吃了几根雪糕"}, session_config)
    print("第三次执行",res)

