from openai import OpenAI

# 1.获取client对象，openAI类对象
client=OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2.调用模型
messages = [ {"role": "system", "content": "你是一个Python编程专家。"},
        {"role": "assistant", "content": "我是一个Python编程专家。请问有什么可以帮助您的吗？"},
        {"role": "user", "content": "for循环输出1到5的数字"},
        {"role": "assistant", "content": "好的，我会为您提供1种方式"},
        {"role": "user", "content": "我要2种"},
        {"role": "assistant", "content": "好的"},   ]

response = client.chat.completions.create(
    model="qwen3-max",  # 您可以按需更换为其它深度思考模型
    messages=messages,
    extra_body={"enable_thinking": False},
    # 开启流式输出
    stream=True
)

# 3.处理结果
for chunk in response:
    # 每段之间以空格分隔
    print(chunk.choices[0].delta.content,
          end="  ",
          # 立刻刷新缓冲区
          flush=True
          )
