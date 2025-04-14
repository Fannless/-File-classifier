import os
import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import json
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# 定义文件类型及其对应的后缀
file_type_mapping = {
    "照片": ["jpg", "jpeg", "png", "gif", "bmp"],
    "视频": ["mp4", "avi", "mov", "mkv"],
    "压缩包": ["zip", "rar", "7z"],
    "文档": ["doc", "docx", "pdf", "txt", "ppt", "pptx", "xls", "xlsx"],
    "其他": []
}


def select_source_folders():
    try:
        source_folders = filedialog.askdirectory(multiple=True)
        source_folder_entry.delete(0, tk.END)
        source_folder_entry.insert(0, ", ".join(source_folders))
    except Exception as e:
        messagebox.showerror("错误", f"选择源文件夹时出现错误: {str(e)}")


def handle_duplicate(destination_path, conflict_count, rename_threshold):
    if conflict_count < rename_threshold:
        response = messagebox.askyesnocancel("文件冲突", f"文件 {os.path.basename(destination_path)} 已存在，是否覆盖？若取消，将跳过该文件；若选择否，将重命名文件。")
        if response is None:
            return None
        elif response:
            return "覆盖"
        else:
            return "重命名"
    else:
        return "重命名"


def add_file_type():
    try:
        category = simpledialog.askstring("添加文件类别", "请输入新的文件类别名称：")
        if category:
            extensions = simpledialog.askstring("添加文件后缀", f"请输入 {category} 类别的文件后缀，用逗号分隔：")
            if extensions:
                ext_list = [ext.strip().lower() for ext in extensions.split(",") if ext.strip()]
                file_type_mapping[category] = ext_list
                messagebox.showinfo("成功", f"{category} 类别的文件后缀已添加，为 {', '.join(ext_list)}")
    except Exception as e:
        messagebox.showerror("错误", f"添加文件定义时出现错误: {str(e)}")


def modify_file_type():
    try:
        if not file_type_mapping:
            messagebox.showinfo("提示", "当前没有可修改的文件定义。")
            return
        top = tk.Toplevel(root)
        top.title("选择要修改的文件定义")

        var = tk.StringVar(top)
        var.set(list(file_type_mapping.keys())[0])

        option_menu = tk.OptionMenu(top, var, *file_type_mapping.keys())
        option_menu.pack(pady=10)

        def confirm_modify():
            try:
                category = var.get()
                extensions = simpledialog.askstring("修改文件后缀", f"请输入 {category} 类别的新文件后缀，用逗号分隔：")
                if extensions:
                    ext_list = [ext.strip().lower() for ext in extensions.split(",") if ext.strip()]
                    file_type_mapping[category] = ext_list
                    messagebox.showinfo("成功", f"{category} 类别的文件后缀已更新为 {', '.join(ext_list)}")
                top.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"修改文件定义时出现错误: {str(e)}")

        confirm_button = ttk.Button(top, text="确认修改", command=confirm_modify)
        confirm_button.pack(pady=10)

        cancel_button = ttk.Button(top, text="取消", command=top.destroy)
        cancel_button.pack(pady=10)
    except Exception as e:
        messagebox.showerror("错误", f"打开修改文件定义窗口时出现错误: {str(e)}")


def delete_file_type():
    try:
        if not file_type_mapping:
            messagebox.showinfo("提示", "当前没有可删除的文件定义。")
            return
        top = tk.Toplevel(root)
        top.title("选择要删除的文件定义")

        var = tk.StringVar(top)
        var.set(list(file_type_mapping.keys())[0])

        option_menu = tk.OptionMenu(top, var, *file_type_mapping.keys())
        option_menu.pack(pady=10)

        def confirm_delete():
            try:
                category = var.get()
                if category in file_type_mapping:
                    del file_type_mapping[category]
                    messagebox.showinfo("成功", f"{category} 类别已删除。")
                top.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"删除文件定义时出现错误: {str(e)}")

        confirm_button = ttk.Button(top, text="确认删除", command=confirm_delete)
        confirm_button.pack(pady=10)

        cancel_button = ttk.Button(top, text="取消", command=top.destroy)
        cancel_button.pack(pady=10)
    except Exception as e:
        messagebox.showerror("错误", f"打开删除文件定义窗口时出现错误: {str(e)}")


def view_all_file_types():
    try:
        if not file_type_mapping:
            messagebox.showinfo("所有文件定义", "当前没有文件定义。")
            return

        top = tk.Toplevel(root)
        top.title("所有文件定义")

        # 创建一个框架用于布局
        frame = ttk.Frame(top)
        frame.pack(pady=10)

        # 定义一个文本框用于显示文件定义信息
        text_widget = ttk.Text(frame, width=40, height=10)
        text_widget.pack()

        info = ""
        for category, extensions in file_type_mapping.items():
            info += f"{category}: {', '.join(extensions)}\n"

        text_widget.insert(tk.END, info)
        text_widget.config(state=tk.DISABLED)  # 设置为只读
    except Exception as e:
        messagebox.showerror("错误", f"查看所有文件定义时出现错误: {str(e)}")


def clear_all_file_types():
    try:
        confirm = messagebox.askyesno("确认清空", "确定要清空所有文件定义吗？")
        if confirm:
            file_type_mapping.clear()
            messagebox.showinfo("成功", "所有文件定义已清空。")
    except Exception as e:
        messagebox.showerror("错误", f"清空文件定义时出现错误: {str(e)}")


def save_file_types():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(file_type_mapping, f)
                messagebox.showinfo("成功", f"文件定义已保存到 {file_path}。")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件定义时出错：{e}")
    except Exception as e:
        messagebox.showerror("错误", f"选择保存文件路径时出现错误: {str(e)}")


def load_file_types():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    global file_type_mapping
                    file_type_mapping = json.load(f)
                messagebox.showinfo("成功", f"文件定义已从 {file_path} 加载。")
            except Exception as e:
                messagebox.showerror("错误", f"加载文件定义时出错：{e}")
    except Exception as e:
        messagebox.showerror("错误", f"选择加载文件路径时出现错误: {str(e)}")


def classify_files():
    try:
        source_folders = source_folder_entry.get().split(", ")
        filter_extensions = filter_entry.get().split(",")
        filter_extensions = [ext.strip().lower() for ext in filter_extensions if ext.strip()]
        try:
            rename_threshold = int(rename_threshold_entry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数作为重命名阈值。")
            return

        # 初始化分类结果
        classified_files = {category: [] for category in file_type_mapping}

        # 收集并分类所有文件
        for source_folder in source_folders:
            if not os.path.exists(source_folder):
                continue
            for filename in os.listdir(source_folder):
                file_path = os.path.join(source_folder, filename)
                if os.path.isfile(file_path):
                    file_extension = os.path.splitext(filename)[1][1:].lower()
                    if filter_extensions and file_extension not in filter_extensions:
                        continue
                    category_found = False
                    for category, extensions in file_type_mapping.items():
                        if file_extension in extensions:
                            classified_files[category].append(file_path)
                            category_found = True
                            break
                    if not category_found:
                        classified_files["其他"].append(file_path)

        # 为每个分类选择目标文件夹
        category_destinations = {}
        for category, files in classified_files.items():
            if files:
                destination_folder = filedialog.askdirectory(title=f"选择 {category} 文件的目标文件夹")
                if destination_folder:
                    # 检查目标文件夹是否存在，不存在则创建
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)
                    category_destinations[category] = destination_folder

        # 移动文件
        conflict_count = 0
        for category, files in classified_files.items():
            if category in category_destinations:
                destination_folder = category_destinations[category]
                for file_path in files:
                    filename = os.path.basename(file_path)
                    destination_path = os.path.join(destination_folder, filename)
                    if os.path.exists(destination_path):
                        conflict_count += 1
                        action = handle_duplicate(destination_path, conflict_count, rename_threshold)
                        if action is None:
                            continue
                        elif action == "覆盖":
                            try:
                                shutil.move(file_path, destination_path)
                            except Exception as e:
                                messagebox.showerror("错误", f"移动文件 {file_path} 时出现错误: {str(e)}")
                        elif action == "重命名":
                            base_name, ext = os.path.splitext(filename)
                            counter = 1
                            new_filename = f"{base_name}_{counter}{ext}"
                            new_destination_path = os.path.join(destination_folder, new_filename)
                            while os.path.exists(new_destination_path):
                                counter += 1
                                new_filename = f"{base_name}_{counter}{ext}"
                                new_destination_path = os.path.join(destination_folder, new_filename)
                            try:
                                shutil.move(file_path, new_destination_path)
                            except Exception as e:
                                messagebox.showerror("错误", f"移动文件 {file_path} 时出现错误: {str(e)}")
                    else:
                        try:
                            shutil.move(file_path, destination_path)
                        except Exception as e:
                            messagebox.showerror("错误", f"移动文件 {file_path} 时出现错误: {str(e)}")
    except Exception as e:
        messagebox.showerror("程序出错", f"程序运行过程中出现错误: {str(e)}")


# 创建主窗口
root = ttk.Window(themename="superhero")
root.title("文件分类程序")
root.geometry("400x700")

# 源文件夹和过滤设置部分
source_frame = ttk.Frame(root)
source_frame.pack(pady=10, padx=10, fill=X)

source_folder_label = ttk.Label(source_frame, text="源文件夹:")
source_folder_label.pack(pady=5)
source_folder_entry = ttk.Entry(source_frame, width=50)
source_folder_entry.pack(pady=5)
source_folder_button = ttk.Button(source_frame, text="选择源文件夹", command=select_source_folders)
source_folder_button.pack(pady=5)

filter_label = ttk.Label(source_frame, text="文件后缀过滤 (逗号分隔, 留空不过滤):")
filter_label.pack(pady=5)
filter_entry = ttk.Entry(source_frame, width=50)
filter_entry.pack(pady=5)

# 重命名阈值输入
rename_threshold_label = ttk.Label(source_frame, text="文件名冲突达到此数量后自动重命名:")
rename_threshold_label.pack(pady=5)
rename_threshold_entry = ttk.Entry(source_frame, width=10)
rename_threshold_entry.insert(0, "3")
rename_threshold_entry.pack(pady=5)

# 分隔线
ttk.Separator(root, orient=HORIZONTAL).pack(pady=10, fill=X)

# 文件定义管理部分
definition_frame = ttk.Frame(root)
definition_frame.pack(pady=10, padx=10, fill=X)

definition_label = ttk.Label(definition_frame, text="文件定义管理", font=("Arial", 12, "bold"))
definition_label.pack(pady=5)

add_button = ttk.Button(definition_frame, text="添加文件定义", command=add_file_type)
add_button.pack(pady=5)

modify_button = ttk.Button(definition_frame, text="修改文件定义", command=modify_file_type)
modify_button.pack(pady=5)

delete_button = ttk.Button(definition_frame, text="删除文件定义", command=delete_file_type)
delete_button.pack(pady=5)

view_button = ttk.Button(definition_frame, text="查看所有文件定义", command=view_all_file_types)
view_button.pack(pady=5)

clear_button = ttk.Button(definition_frame, text="清空所有文件定义", command=clear_all_file_types)
clear_button.pack(pady=5)

save_button = ttk.Button(definition_frame, text="保存文件定义", command=save_file_types)
save_button.pack(pady=5)

load_button = ttk.Button(definition_frame, text="加载文件定义", command=load_file_types)
load_button.pack(pady=5)

# 分隔线
ttk.Separator(root, orient=HORIZONTAL).pack(pady=10, fill=X)

# 分类操作部分
classify_frame = ttk.Frame(root)
classify_frame.pack(pady=10, padx=10, fill=X)

classify_label = ttk.Label(classify_frame, text="分类操作", font=("Arial", 12, "bold"))
classify_label.pack(pady=5)

classify_button = ttk.Button(classify_frame, text="开始分类", command=classify_files)
classify_button.pack(pady=20)

# 运行主循环
root.mainloop()
    