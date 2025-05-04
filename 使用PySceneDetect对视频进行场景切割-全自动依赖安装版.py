import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from tkinter import ttk
import locale

# 获取系统默认编码（如 Windows 通常为 GBK）
system_encoding = locale.getpreferredencoding(False)

def select_input_folder():
    folder = filedialog.askdirectory(title="选择导入文件夹")
    if folder:
        input_folder_var.set(folder)

def select_output_folder():
    folder = filedialog.askdirectory(title="选择导出文件夹")
    if folder:
        output_folder_var.set(folder)

def update_progress(count, total):
    progress_bar['value'] = count
    progress_label.config(text=f"{count} / {total}")

def update_log(msg):
    # 过滤掉替换字符
    cleaned = msg.replace("�", "")
    log_text.insert(tk.END, cleaned)
    log_text.see(tk.END)

def run_splitting():
    # 自动更新 scenedetect
    try:
        update_log("正在检查并更新 scenedetect，请稍候...\n")
        subprocess.check_call(["pip", "install", "--upgrade", "scenedetect"])
        update_log("scenedetect 已更新至最新版本。\n")
    except Exception as e:
        update_log(f"scenedetect 更新失败：{e}\n")

    # 自动安装 opencv-python
    try:
        update_log("正在安装 opencv-python，请稍候...\n")
        subprocess.check_call(["pip", "install", "--upgrade", "opencv-python"])
        update_log("opencv-python 安装完成。\n")
    except Exception as e:
        update_log(f"opencv-python 安装失败：{e}\n")

    # 自动添加 scenedetect.exe 所在路径到 PATH
    try:
        from pathlib import Path
        user_path = os.path.expandvars(r"%LOCALAPPDATA%\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\Scripts")
        current_path = os.environ.get("PATH", "")
        if user_path not in current_path:
            update_log("正在将 scenedetect 安装路径加入 PATH...\\n")
            subprocess.call(f'setx PATH "{current_path};{user_path}"', shell=True)
            update_log("已添加 scenedetect 路径到 PATH，请重启系统或命令行后生效。\\n")
        else:
            update_log("scenedetect 路径已存在于 PATH 中。\\n")
    except Exception as e:
        update_log(f"添加 PATH 时出错：{e}\\n")


    # 自动下载并安装 FFmpeg（仅适用于 Windows）
    try:
        import platform
        if platform.system() == "Windows":
            import urllib.request, zipfile
            from pathlib import Path

            ffmpeg_dir = Path(os.getenv('LOCALAPPDATA')) / "ffmpeg-auto"
            ffmpeg_bin = ffmpeg_dir / "ffmpeg" / "bin"
            ffmpeg_exe = ffmpeg_bin / "ffmpeg.exe"

            if not ffmpeg_exe.exists():
                update_log("正在下载并安装 FFmpeg...\\n")
                ffmpeg_zip_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
                zip_path = ffmpeg_dir / "ffmpeg.zip"

                ffmpeg_dir.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(ffmpeg_zip_url, zip_path)

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(ffmpeg_dir)
                
                # 找到解压后的子目录
                extracted_folders = list(ffmpeg_dir.glob("ffmpeg-*"))
                if extracted_folders:
                    (ffmpeg_dir / "ffmpeg").mkdir(exist_ok=True)
                    for item in extracted_folders[0].iterdir():
                        target = ffmpeg_dir / "ffmpeg" / item.name
                        if not target.exists():
                            if item.is_dir():
                                import shutil
                                shutil.copytree(item, target)
                            else:
                                shutil.copy2(item, target)
                
                update_log("FFmpeg 安装完成。\\n")

            # 添加到 PATH
            current_path = os.environ.get("PATH", "")
            if str(ffmpeg_bin) not in current_path:
                update_log("正在将 FFmpeg 路径加入 PATH...\\n")
                subprocess.call(f'setx PATH "{current_path};{ffmpeg_bin}"', shell=True)
                update_log("已添加 FFmpeg 路径到 PATH，请重启系统或命令行后生效。\\n")
            else:
                update_log("FFmpeg 路径已存在于 PATH 中。\\n")
    except Exception as e:
        update_log(f"安装 FFmpeg 时发生错误：{e}\\n")
    # 自动更新 scenedetect
    try:
        update_log("正在检查并更新 scenedetect，请稍候...\n")
        subprocess.check_call(["pip", "install", "--upgrade", "scenedetect"])
        update_log("scenedetect 已更新至最新版本。\n")
    except Exception as e:
        update_log(f"scenedetect 更新失败：{e}\n")

    input_folder = input_folder_var.get()
    output_folder = output_folder_var.get()
    if not input_folder or not output_folder:
        root.after(0, lambda: messagebox.showerror("错误", "请先选择导入和导出文件夹！"))
        root.after(0, lambda: btn_start.config(state=tk.NORMAL))
        return

    # 支持的常见视频扩展名
    video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv"]
    video_files = [f for f in os.listdir(input_folder)
                   if os.path.splitext(f)[1].lower() in video_extensions]

    total_videos = len(video_files)
    if total_videos == 0:
        root.after(0, lambda: messagebox.showerror("错误", "导入文件夹中没有找到视频文件！"))
        root.after(0, lambda: btn_start.config(state=tk.NORMAL))
        return

    # 初始化整体进度条和日志区域
    root.after(0, lambda: progress_bar.config(maximum=total_videos))
    root.after(0, lambda: progress_bar.config(value=0))
    root.after(0, lambda: progress_label.config(text=f"0 / {total_videos}"))
    root.after(0, lambda: log_text.delete(1.0, tk.END))

    processed_count = 0
    for video in video_files:
        video_path = os.path.join(input_folder, video)
        video_basename, _ = os.path.splitext(video)
        video_output_dir = os.path.join(output_folder, video_basename)
        os.makedirs(video_output_dir, exist_ok=True)

        root.after(0, lambda v=video: update_log(f"\n开始处理 {v} ...\n"))
        command = ["scenedetect", "-i", video_path, "split-video", "-o", video_output_dir]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding=system_encoding,
                errors='replace'
            )
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    root.after(0, lambda l=line: update_log(l))
            retcode = process.poll()
            if retcode:
                root.after(0, lambda v=video: update_log(f"处理 {v} 时出错，返回码：{retcode}\n"))
            else:
                root.after(0, lambda v=video: update_log(f"处理 {v} 完成。\n"))
        except Exception as e:
            root.after(0, lambda v=video, e=e: update_log(f"处理 {v} 时发生异常：{e}\n"))
        
        processed_count += 1
        root.after(0, lambda count=processed_count, total=total_videos: update_progress(count, total))
    
    root.after(0, lambda: messagebox.showinfo("完成", "所有视频切割完成！"))
    root.after(0, lambda: btn_start.config(state=tk.NORMAL))

def start_splitting():
    btn_start.config(state=tk.DISABLED)
    threading.Thread(target=run_splitting).start()

# 创建 GUI 窗口
root = tk.Tk()
root.title("视频切割工具")

input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()

# 添加使用说明框
instruction_frame = tk.LabelFrame(root, text="使用说明", padx=10, pady=10)
instruction_frame.pack(fill=tk.X, padx=10, pady=10)

instruction_text = """
使用步骤：
1. 点击"选择导入文件夹"按钮，选择包含视频文件的文件夹
2. 点击"选择导出文件夹"按钮，选择切割后视频片段的保存位置
3. 点击"开始切割"按钮，开始处理视频

注意事项：
- 支持的视频格式：MP4, AVI, MKV, MOV, FLV, WMV
- 每个视频将在输出文件夹中创建同名子文件夹存放切割片段
- 处理过程中请勿关闭程序
"""

instruction_label = tk.Label(instruction_frame, text=instruction_text, justify=tk.LEFT, anchor="w")
instruction_label.pack(fill=tk.X)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

# 导入文件夹选择
btn_select_input = tk.Button(frame, text="选择导入文件夹", command=select_input_folder)
btn_select_input.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_input = tk.Entry(frame, textvariable=input_folder_var, width=50)
entry_input.grid(row=0, column=1, padx=5, pady=5)

# 导出文件夹选择
btn_select_output = tk.Button(frame, text="选择导出文件夹", command=select_output_folder)
btn_select_output.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_output = tk.Entry(frame, textvariable=output_folder_var, width=50)
entry_output.grid(row=1, column=1, padx=5, pady=5)

# 开始切割按钮
btn_start = tk.Button(frame, text="开始切割", command=start_splitting)
btn_start.grid(row=2, column=0, columnspan=2, pady=10)

# 整体进度条及标签
progress_bar = ttk.Progressbar(frame, orient="horizontal", mode="determinate", length=300)
progress_bar.grid(row=3, column=0, columnspan=2, pady=5)
progress_label = tk.Label(frame, text="0 / 0")
progress_label.grid(row=4, column=0, columnspan=2)

# 日志输出区域（滚动文本框）
log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

log_text = tk.Text(log_frame, height=15)
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.config(yscrollcommand=scrollbar.set)

# 添加版权信息
copyright_label = tk.Label(root, text="© 2025 一模型Ai (https://jmlovestore.com) - 不会开发软件吗 🙂 Ai会哦", font=("Arial", 9), fg="gray")
copyright_label.pack(side=tk.BOTTOM, pady=5)

root.mainloop()
