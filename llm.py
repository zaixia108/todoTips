from volcenginesdkarkruntime import Ark

# 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
# 初始化Ark客户端，从环境变量中读取您的API Key
client = Ark(
    # 此为默认路径，您可根据业务所在地域进行配置
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
    api_key='e4c8d350-ce4d-46e9-9396-8a1a1dcdbb7a',
)

# 常量定义
CATEGORY_DISPLAY_NAMES = {
    "today": "本日",
    "week": "本周",
    "month": "本月"
}
MAX_DESC_PREVIEW_LENGTH = 30


def summarize_todos(todos_data):
    """
    使用LLM对待办事项进行智能汇总
    
    Args:
        todos_data: 包含待办事项信息的字典
    
    Returns:
        str: AI生成的汇总文本
    
    Raises:
        ValueError: 当LLM返回无效响应时
    """
    # 构建用于汇总的文本
    summary_parts = []
    
    # 汇总各个类别的待办事项
    for category_name, category_data in todos_data.items():
        category_display = CATEGORY_DISPLAY_NAMES.get(category_name, category_name)
        total = category_data.get('total', 0)
        completed = category_data.get('completed', 0)
        pending = total - completed
        
        summary_parts.append(f"\n【{category_display}待办】")
        summary_parts.append(f"总计: {total}项, 已完成: {completed}项, 待完成: {pending}项")
        
        todos = category_data.get('todos', [])
        if todos:
            summary_parts.append("待办事项列表:")
            for i, todo in enumerate(todos, 1):
                status = "✓" if todo.get('completed', False) else "○"
                title = todo.get('title', '无标题')
                desc = todo.get('description', '')
                if desc and len(desc) > MAX_DESC_PREVIEW_LENGTH:
                    desc_preview = f" - {desc[:MAX_DESC_PREVIEW_LENGTH]}..."
                elif desc:
                    desc_preview = f" - {desc}"
                else:
                    desc_preview = ""
                summary_parts.append(f"  {status} {title}{desc_preview}")
    
    full_text = "\n".join(summary_parts)
    
    # 使用LLM进行智能汇总
    prompt = f"""请作为一个专业的待办事项助手，对以下待办事项进行智能汇总分析。

待办事项数据：
{full_text}

请提供：
1. 整体概览：总结所有类别的完成情况
2. 重点关注：列出需要优先处理的未完成事项
3. 进度分析：分析当前的工作进度和完成率
4. 建议：给出合理的时间管理建议

请用简洁、专业的语言进行汇总，帮助用户更好地理解和管理自己的待办事项。"""
    
    response = client.chat.completions.create(
        model="doubao-seed-1-6-flash-250615",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    
    # 验证响应
    if not response.choices or not response.choices[0].message.content:
        raise ValueError("LLM返回了空响应，请稍后重试")
    
    return response.choices[0].message.content
