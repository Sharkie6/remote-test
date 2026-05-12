import os,json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import  StrOutputParser,JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage


# message_to_dict: 单个消息对象（BaseMessage类实例） -> 字典
# messages_from_dict: [字典、字典....] -> [消息、消息....]
# AIMessage、HumanMessage、SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        #完整的文件路径
        self.file_path=os.path.join(self.storage_path,self.session_id)
        # 确保文件夹存在
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_messages=list(self.messages)
        all_messages.extend(messages)

        # 消息转为字典
        new_messages=[message_to_dict(message) for message in all_messages]

        # 将数据写入文件
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property # 装饰器：把方法变成“属性”，外面可以直接 .messages 调用
    def messages(self)->list[BaseMessage]:
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                message_data=json.load(f)
                return messages_from_dict(message_data)

        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)






def get_history(session_id):
   return FileChatMessageHistory(session_id,"./chat_history")

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




