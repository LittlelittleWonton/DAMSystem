## Virtualenv
#### Introduction>>ISOLATE(隔离)
- virtualenv是用于创建隔离Python开发环境的工具（类似于docker）
- 解决依赖和版本冲突的问题
#### Install
- pip
- easy_install
- git
- use locally from sourse(在使用virtualenv.py脚本的时候需要有本地的pip/setuptools/virtualenv的环境支持)
- windows安装需要注意：①要在某个含有空格的目录下面创建virtualenv环境，就要安装 win32api 。②见激活
#### User Guide
- create
> virtualenv new_env
- active
> $ source /path/to/ENV/bin/activate
对于某些shell会提示‘source does not exist’，就需要使用‘.source’
> \>model_env\Scripts\activate
值得注意的是，如果在windows的PowerShell中执行的时候，文件的执行会受限，这样以来就需要更改文件的权限，比较麻烦，所以推荐使用cmd执行，需要修改PowerShell中执行策略的用户首选项(preference)
```
PS C:\> Set-ExecutionPolicy AllSigned

PS C:\> virtualenv .\foo
New python executable in C:\foo\Scripts\python.exe
Installing setuptools................done.
Installing pip...................done.
PS C:\> .\foo\scripts\activate

Do you want to run software from this untrusted publisher?
File C:\foo\scripts\activate.ps1 is published by E=jannis@leidel.info,
CN=Jannis Leidel, L=Berlin, S=Berlin, C=DE, Description=581796-Gh7xfJxkxQSIO4E0
and is not trusted on your system. Only run scripts from trusted publishers.
[V] Never run  [D] Do not run  [R] Run once  [A] Always run  [?] Help
(default is "D"):A
(foo) PS C:\>

```
- remove
```
(ENV)$ deactivate
$ rm -r /path/to/ENV
```
直接删掉就好
- Command
    1. $ virtualenv --system-site-packages:令隔离环境可以访问系统全局的site-packages目录。使用该命令可以创建一个跟本地一模一样的python环境
    2. —no-site-packages：令隔离环境不能访问系统全局的site-packages目录。
    3. $ virtualenv --extra-search-dir=/path/to/distributions ENV:创建新的隔离环境时，virtualenv会安装setuptools,distribute或是pip包管理器。一般情况下，它们都会从 Python Package Index (PyPI) 中寻找并安装最新的包。但在一些特定情况下，我们并不希望如此。例如，你在部署virtualenv时既不想从网上下载，也不想从PyPI中获取包。做为替代方案，可以让setuptools，distribute或是pip搜寻文件系统，让virtualenv使用本地发行包而不是从网上下载。
    4. $ virtualenv -p PYTHON_EXE, --python=PYTHON_EXE ENV :指定python版本
    5. --clear：清空非root用户的安装
    6. --never-download：禁止从网上下载任何数据，如果本地搜索失败就会报错
    7. --prompt==PROMPT
定义隔离环境的命令行前缀。
- Deploy
部署网站打包的时候就可以进行几步sao操作
1. 在本地的虚拟环境中pip freeze > requirements
2. 提交到github或者svn
3. 下载到服务器
4. 激活虚拟环境后pip install -r requirements
5. 收集静态文件python manage.py collectstatic
6. 生成数据库
7. 创建超级用户
