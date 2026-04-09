def greet(name):
    """一个简单的问候函数"""
    return f"你好，{name}！今天是你学Python的第二天"

if __name__ == "__main__":
    user_name = input("你叫什么名字？")
    message = greet(user_name)
    print(message)