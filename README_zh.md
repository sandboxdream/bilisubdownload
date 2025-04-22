# 哔哩哔哩字幕下载器

一个用于下载哔哩哔哩视频字幕的工具，使用BV号进行下载。

## 功能特点

- 使用BV号下载哔哩哔哩视频的字幕
- 支持单集和多集视频
- 将字幕保存为JSON和SRT两种格式
- 多种操作模式：
  - 交互模式：手动输入BV号
  - 命令行模式：通过命令行参数提供BV号
  - 文件模式：从文本文件中读取BV号

## 系统要求

- Python 3.6 或更高版本
- 所需Python包：
  - requests

## 安装方法

1. 克隆此仓库：
   ```
   git clone https://github.com/sandboxdream/bilisubdownload.git
   cd bilisubdownload
   ```


2. 安装所需包：
   ```
   pip install requests
   ```

## 使用方法

### 交互模式

不带任何参数运行脚本，进入交互模式：

```
python main.py
```

系统将提示您输入BV号。

### 命令行模式

在命令行参数中提供一个或多个BV号：

```
python main.py BV1Jm421p7RV
```

您可以提供多个BV号：

```
python main.py BV1Jm421p7RV BV2xxx BV3xxx
```

### 文件模式

创建一个文本文件，每行一个BV号，然后使用`-f`标志：

```
python main.py -f bv_ids.txt
```

`bv_ids.txt`文件内容示例：
```
BV1Jm421p7RV
BV2xxx
BV3xxx
```

### 帮助信息

显示使用帮助信息：

```
python main.py -h
```

## 身份验证

某些视频可能需要身份验证才能访问其字幕。您可以在脚本所在目录中的`cookies.txt`文件中提供cookies。

获取cookies的方法：
1. 在浏览器中登录哔哩哔哩
2. 使用浏览器开发者工具复制您的cookies
3. 将它们保存到项目目录中的`cookies.txt`文件

## 输出结果

字幕保存在名为`output_BVID`的目录中，其中`BVID`是视频的BV号。对于视频的每个部分，会创建两个文件：
- `part_N_CID.json`：JSON格式的字幕数据
- `part_N_CID.srt`：SRT格式的字幕数据（与大多数视频播放器兼容）

## 项目结构

```
bilisubdownload/
├── main.py              # 下载字幕的主脚本
├── cookies.txt          # 存储身份验证cookies的可选文件
├── bv_ids.txt           # 批处理BV号的示例文件
├── README.md            # 英文文档
├── README_zh.md         # 中文文档
├── LICENSE              # GNU GPL v3.0许可证
└── .gitignore           # Git忽略文件
```

## 贡献

欢迎贡献！以下是贡献的方法：

1. Fork此仓库
2. 创建新分支（`git checkout -b feature/your-feature-name`）
3. 进行更改
4. 提交更改（`git commit -m '添加某功能'`）
5. 推送到分支（`git push origin feature/your-feature-name`）
6. 打开Pull Request

## 报告问题

如果您遇到任何问题或有改进建议，请在GitHub仓库上开一个issue。

## 许可证

本项目采用GNU通用公共许可证v3.0授权 - 详情请参阅[LICENSE](LICENSE)文件。
