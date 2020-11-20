## Markdown 原生语法

### 基础规则

#### 标题
```markdown
    # 一级标题  
    ## 二级标题    
    ### 三级标题  
    #### 四级标题
    ##### 五级标题
    ###### 六级标题
```

#### 列表

- 无序列表：
```mardown
    - 列1
    - 列2
    - 列3
```
- 有序列表
```mardown
    1. 列1     
    2. 列2
    3. 列3
```
- 任务列表：
```mardown
    - [ ] 任务一 未做任务
    - [x] 任务二 已做任务

    符号与文本之间保留一个字符的空格
```

#### 缩进与换行

- 缩进符：
```markdown
    &ensp; or &#8194; 表示一个半角的空格
    &emsp; or &#8195;  表示一个全角的空格
    &emsp;&emsp; 两个全角的空格（用的比较多）
    &nbsp; or &#160; 不断行的空白格
```
- 换行符：
```markdown
    单行 <p>
    多行 <br />
    br 和 / 之间有空格
```

#### 分割线

```markdown
    三个或以上的 *** 或 ---
```

#### 超链接

- 显示文本：
```markdown
    [显示文本](链接地址) 
```
&emsp;&emsp;显示效果：[百度链接](http://www.baidu.com)

- 显示图片：
```markdown
    ![图片名称](本地或网络图片链接)
```

- 脚注：

    在需要添加注脚的文字后加上脚注名字[^注脚名字],称为加注。 然后在文本的任意位置(一般在最后)添加脚注，脚注前必须有对应的脚注名字。

    注意：经测试注脚与注脚之间必须空一行，不然会失效。成功后会发现，即使你没有把注脚写在文末，经Markdown转换后，也会自动归类到文章的最后。

```markdown
  使用 Markdown[^1]可以效率的书写文档, 直接转换成 HTML[^2]。

  [^1]:Markdown是一种纯文本标记语言

  [^2]:HyperText Markup Language 超文本标记语言
```

- 参考式：

    参考式超链接一般用在学术论文上面，或者另一种情况，如果某一个链接在文章中多处使用，那么使用引用 的方式创建链接将非常好，它可以让你对链接进行统一的管理。
```markdown
  我经常去的几个网站[Google][1]、[Github][2]。

  [1]:http://www.google.com
  [2]:http://www.Github.com
```
&emsp;&emsp;显示效果：我经常去的几个网站[Google][1]、[Leanote][2]。

[1]:http://www.google.com
[2]:http://www.leanote.com

#### 引用

```markdown
    文字开始处加 > 和一个空格
    要实现嵌套可以用 >>
```

#### 代码块

```markdown
    单行使用: `代码`
    多行使用:
      ```Python (实现对应语法代码高亮)
      Python代码
      ```
    特殊使用：
      ```Markdown
      Markdown代码
      ```
      其中的markdown语法不会被转义
```

#### 文本强调

```markdown
    *斜体*   
    **加粗**   
    ***粗斜体*** 
    _强调_   
    __加粗__   
    ___粗斜体___
    ~删除线~
```

### 特殊规则

#### 表格

  - Markdown规则：
```markdown
    | Left-Aligned  | Center Aligned  | Right Aligned |
    | :------------ |:---------------:| -----:|
    | Content Cell  | Content Cell | Content Cell |
    | Content Cell  | Content Cell | Content Cell |
```
  - 效果：

  | Left-Aligned  | Center Aligned  | Right Aligned |
  | :------------ |:---------------:| -----:|
  | Content Cell  | Content Cell | Content Cell |
  | Content Cell  | Content Cell | Content Cell |

#### 流程图

  - 写法：
```markdown
  ```flow
  st=>start: 开始
  op=>operation: My Operation
  cond=>condition: Yes or No?
  e=>end
  st->op->cond
  cond(yes)->e
  cond(no)->op
  &```
```

  - 效果：
  ```flow
  st=>start: 开始
  op=>operation: My Operation
  cond=>condition: Yes or No?
  e=>end
  st->op->cond
  cond(yes)->e
  cond(no)->op
  ```


### 其他规则
1. 中英文混排应该「SHOULD」采用如下规则：

    - 英文和数字使用半角字符
    - 中文文字之间不加空格
    - 中文文字与英文、阿拉伯数字及 @ # $ % ^ & * . ( ) 等符号之间加空格
    - 中文标点之间不加空格
    - 中文标点与前后字符（无论全角或半角）之间不加空格
    - 如果括号内有中文，则使用中文括号
    - 如果括号中的内容全部都是英文，则使用半角英文括号
    -当半角符号 / 表示「或者」之意时，与前后的字符之间均不加空格
    其它具体例子推荐阅读这里


2. 中文符号应该「SHOULD」使用如下写法：

    - 用直角引号（「」）代替双引号（“”），不同输入法的具体设置方法请[参考这里](https://www.zhihu.com/question/19755746)
    - 省略号使用「……」，而「。。。」仅用于表示停顿


3. 表达方式，应当「SHOULD」遵循《The Element of Style》：

    - 使段落成为文章的单元：一个段落只表达一个主题
    - 通常在每一段落开始要点题，在段落结尾要扣题
    - 陈述句中使用肯定说法
    - 使用相同的结构表达并列的意思
