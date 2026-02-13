from volcenginesdkarkruntime import Ark

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key='e4c8d350-ce4d-46e9-9396-8a1a1dcdbb7a',
)


def summarize_text(text):
    response = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="doubao-seed-1-6-flash-250615",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "请帮我总结以下内容：\n" + text},
                ],
            }
        ],
    )
    return response.choices[0]
