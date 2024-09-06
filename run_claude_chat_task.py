import asyncio
import os
from claude_chat import run_chat

async def custom_input():
    # 最初の入力としてタスクを提供
    return "Pythonのサンプルスクリプトを3つ作成して"

def save_result(result):
    # 結果を'results'ディレクトリに保存
    if not os.path.exists('results'):
        os.makedirs('results')
    
    with open('results/python_scripts.txt', 'w', encoding='utf-8') as f:
        f.write(result)

async def run_task():
    result = ""
    
    async def capture_output():
        nonlocal result
        while True:
            try:
                output = await asyncio.get_event_loop().run_in_executor(None, input)
                result += output + "\n"
            except EOFError:
                break

    # 出力をキャプチャするタスクを開始
    capture_task = asyncio.create_task(capture_output())

    # Claude chatを実行
    await run_chat(input_func=custom_input, auto_mode=True, auto_mode_iterations=1, script_mode=True)

    # 出力キャプチャタスクをキャンセル
    capture_task.cancel()
    try:
        await capture_task
    except asyncio.CancelledError:
        pass

    # 結果を保存
    save_result(result)
    print("Task completed. Results saved in 'results/python_scripts.txt'")

if __name__ == "__main__":
    asyncio.run(run_task())
