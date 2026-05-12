from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import  StrOutputParser,JsonOutputParser
from langchain_core.runnables import Runnable, RunnableLambda

example_prompt=PromptTemplate.from_template("单词：{word},反义词：{anto}")
second_prompt=PromptTemplate.from_template("请解释{name}的意思")

example_data=[
    {"word":"大","anto":"小"},
    {"word":"上","anto":"下"}
]
json_parser=JsonOutputParser()

my_func=RunnableLambda(lambda ai_msg:{"name":ai_msg.content})

few_shot_prompt=FewShotPromptTemplate(
    example_prompt=example_prompt,
    examples=example_data,
    prefix="给出定词的反义词，有如下定义：",
    suffix="基于示例告诉我,{input_word}的反义词是？只回答",
    input_variables=['input_word']
)
model = ChatTongyi(model="qwen-max")

chain=few_shot_prompt |model |my_func | second_prompt |model
for chunk in chain.stream(input={"input_word":"左"}):
    print(chunk,end= " ",flush=True)

