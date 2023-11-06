

# FPGA 统一实验平台后端服务

本仓库包含FPGA 统一实验平台的后端服务代码。这些服务包括用户认证、资料管理以及代码相关操作（目前未使用）的处理程序。

## 功能

- 用户登录和认证
- 用户资料管理
- 代码检索和组织 *（目前未使用）*
- 文件操作，包括添加和删除文件（目前未使用）

## 开始使用

### 先决条件

在开始之前，请确保您已经满足以下条件：

- 已安装Python 3.x。
- 已安装Tornado Web服务器。
- 可以访问系统的包管理器并根据需要安装包。

### 配置

在启动服务器之前，您需要配置脚本中的`log_file_path`变量，以指向您希望的日志文件位置：

```python
log_file_path = "/path/to/your/log/cedit.log"
```

### 运行服务器

要启动Tornado服务器，运行：

```sh
python cedit.py
```

服务器将在端口`9001`启动，但您可以通过修改脚本中的`http_server.listen(9001)`行来更改此端口。

## 使用

以下端点可用：

- `/` - MainHandler：根访问的基本处理程序，用于健康检查和服务器状态。
- `/login` - LoginHandler：管理用户登录，票据验证和令牌生成。
- `/profile` - ProfileHandler：处理用户资料数据的检索和展示。
- `/code` - CodeHandler：*（目前未使用）* 检索用于编辑的代码和目录结构。
- `/savecode` - SavecodeHandler：*（目前未使用）* 处理将编辑过的代码保存到服务器的操作。
- `/appendfile` - AppendfileHandler：*（目前未使用）*在服务器上创建新文件。
- `/deletefile` - DeletefileHandler：*（目前未使用）*从服务器上删除文件。
- `/sso/logout` - LogoutHandler：管理用户登出过程。

## 日志记录

应用程序使用`RotatingFileHandler`进行日志记录，以防止日志文件无限增长。当日志达到特定大小时，它们会进行轮转。

## 说明

- 代码中的`verify`函数用于验证认证令牌。



