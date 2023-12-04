import time
start_time = time.time()

def get_elapsed_time():
    """返回自程序开始以来经过的时间（以秒为单位）"""
    current_time = time.time()
    elapsed_time = current_time - start_time
    return elapsed_time

# 示例使用
while True:
    elapsed = get_elapsed_time()
    print(f"程序已运行 {elapsed} 秒")

    # 暂停一段时间（例如1秒），以便观察输出
    time.sleep(1)