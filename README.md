# file-search
# 暑假实训


# 答辩要求

- online: 给出访问域名地址 `url` 
- PPT & 演示 (5分钟)
- 答辩时分别展示：PPT、功能、性能、内存，并且给出源代码地址


# 技术要求
- Language: JAVA/C/GO/Shell/nodejs/python ...
- Database: file/mysql/mongodb ...
- Page: H5/CSS/JS/VUE/REACT ...
- Server: FTP/APACHE/NGINX/GIT ...



# 项目命题

要求实现一个APP文件检索系统，具体描述如下：

1. 选择硬盘一个文件夹作为查询的目录，此时将该目录下的所有检索文件 `pdf`/`word` 建立索引，保存到数据库中；
2. 输入查询的关键字，将符合要求的结果按下面格式显示出来
3. 点击选择多个查询结果内容，在点击保存可以将数据保存到文本，并下载。

```
路径A\子路径B\...\文件1      
-------------------------------
行号x    包括关键字的内容行   
行号y    包括关键字的内容行
...
行号z    包括关键字的内容行


路径C\子路径D\...\文件2     
-------------------------------
行号x    包括关键字的内容行   
行号y    包括关键字的内容行
...

1. python  版本  3.10

2. 包依赖见： package.txt
   pip install -r package.txt

3. 启动方式：
   先启动 mongo.bat                        
   再启动 python app.py


4. 二进制包：
   app.exe    不需要依赖安装环境，在启动 mongodb 后，直接运行即可。

5. mongodb  文档结构说明： ctg.pdfdoc

  {
        "_id" : ObjectId("649b48d51dca54f38f79a012"),                                唯一编码
        "page" : 20,                                                                 pdf:页码|docx:段落
        "line" : 19,                                                                 行号
        "content" : "1、一般检查：身高cm，体重kg，BMI；血压mmHg，腰围cm，臀围cm，腰臀比，贫血貌", 文本内容
        "path" : "D:/work/pdfdocsearch/data\\PCOS首诊.docx",                           文件路径
        "filename" : "PCOS首诊.docx"                                                   文件名称
}

6.目录说明：
  web   界面模板文件 样式单  脚本  字体
  app.py   python 主文件 程序入口
  mongo    数据库目录 windows  系统复制部署
  package.txt  依赖包清单
  cmd.txt      二进制打包命令
  readme.txt   说明文件
行号z    包括关键字的内容行


......
```
