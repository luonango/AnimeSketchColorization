# **AnimeSketchColorization**


  **将动漫人物的手绘素描图进行着色**

  **Colorize the sketch of anime character**

    这是我们的多媒体通信的作业。 = =

----------


** 整体框架**
===================

  - ** 数据集的获取：**
      + 爬虫：获取大量的动漫人物照片（RGB）
      + 整理：图片标准化（待定）
      + RGB图片转化成对应的手绘图并进行标注。
      
  - ** 模型设计及训练:**
      + 手绘图彩色化的模型设计及编写（生成对抗网络GAN)
      + 模型训练及调节参数
      + 将模型功能封装
      
  - ** Web展示端:**
      + 传入手绘动漫角色的图片，显示着色后的彩色图片
      + 传入彩色动漫角色图片，显示对应的手绘图片
      + 采用画廊显示着色后的彩色图片（直接阅览多张，或滚动显示更多）
      
  - ** 后台:**
      + 与前端功能衔接
      + 与手绘图彩色化功能衔接
      + 与生成手绘图功能衔接

----------

** 环境**
===================

  - ** Python2.7**
      + tornado
      + nginx
      + keras
      + tensorflow/theano
      + PIL
      + ...
      
  - ** Linux**
      + 64 bit

----------

** 工作区**
===================

  - ** luonango**
      + colorization
      + dataset
      + docs
      + logs
      + tests
      + utils
  - ** liaohuiqiang00**
      + dataset
      + docs
      + logs
      + tests
      + tornado
      + utils
      + web 
  - ** angelorlover**
      + docs
      + logs
      + tests
      + utils
  - ** cy-time**
      + dataset
      + docs
      + logs
      + tests
      + utils
      + web 
  - ** xiaoyunjun**
      + dataset
      + docs
      + logs
      + tests
      + utils
----------

待续...

----------
