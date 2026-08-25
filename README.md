# EchoTrace JSON 转 TXT

## 项目介绍

本项目用于将 EchoTrace 导出的 JSON 格式聊天记录转换为便于阅读和保存的 TXT 文本文件。

程序会保留每条消息的以下信息：

- 发送时间
- 发送人昵称
- 发送内容

支持批量处理程序或 EXE 所在目录下的所有 JSON 文件，也支持通过命令行指定单个 JSON 文件或目录。


## 快速开始

### 面向使用者(使用exe文件)

1. 将 `main.exe` 放到聊天记录 JSON 文件所在的目录。
2. 双击运行 `main.exe`。
3. 程序会自动处理当前目录中的所有 `.json` 文件，并在原目录生成同名 `.txt` 文件。
4. 程序处理完成后会显示成功和失败数量，按任意键退出。

也可以通过命令行指定输入文件或目录：

```bash
main.exe "王秉祥_1787667356649.json"
main.exe "D:\\聊天记录"
```

不指定参数时，程序始终以 EXE 所在目录作为默认输入目录，不受命令行当前工作目录影响。


### 面向开发者（从源码运行）

#### 环境要求

- Python 3.10 或更高版本
- Windows、Linux 或 macOS

#### 安装和运行

```bash
# 克隆项目
git clone <项目地址>

# 进入项目目录
cd <项目目录>

# 激活虚拟环境
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 批量转换程序所在目录中的 JSON 文件
python main.py

# 转换指定 JSON 文件或目录
python main.py "王秉祥_1787667356649.json"
```

## 实现方法

### 转换流程

1. 查找输入文件或目录中的 `.json` 文件。
2. 读取 JSON 顶层的 `messages` 数组。
3. 从每条消息中读取 `formattedTime`、`senderDisplayName` 和 `content`。
4. 按固定格式将消息逐行写入同名 TXT 文件。

输出示例：

```text
[2026-04-16 13:26:59] 王秉祥: [通话消息]
[2026-04-16 13:51:15] 青淮: [图片]
[2026-04-16 13:51:17] 青淮: 王哥
```

### 路径处理

程序使用 `os.path.dirname(os.path.abspath(__file__))` 获取源码文件所在目录。使用 PyInstaller 打包后，则使用 `sys.executable` 获取 EXE 文件所在目录。这样无论从哪里启动程序，默认输入和输出路径都与程序文件保持一致。

如果消息缺少 `formattedTime`，程序会回退使用 `createTime`；如果缺少 `senderDisplayName`，会回退使用 `senderUsername`。输入支持 UTF-8 和 UTF-8 BOM 编码，输出统一使用 UTF-8 编码。

### 打包 EXE

项目已在 `requirements.txt` 中声明 PyInstaller 依赖。安装依赖后执行：

```bash
pyinstaller -i my.ico -c -F main.py
```

参数说明：

- `-i my.ico`：使用项目中的图标文件。
- `-c`：保留控制台窗口，用于显示处理进度和错误信息。
- `-F`：生成单文件 EXE。

打包完成后，EXE 位于 `dist/main.exe`。将它复制到 JSON 文件目录即可使用。程序运行时会在 EXE 所在目录生成 TXT 文件。


## 版本日志

### v1.0.0    --2026.8.25

- 支持 EchoTrace 聊天记录 JSON 转 TXT。
- 支持单文件转换和目录批量转换。
- 保留发送时间、发送人昵称和发送内容。
- 兼容源码运行和 PyInstaller 打包运行的路径获取。
- 转换结束后等待用户按任意键退出。


## 许可证

本项目采用 Prosperity Public License 2.0.0 许可证，详见 LICENSE 文件。


