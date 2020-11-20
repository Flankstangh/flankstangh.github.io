## Latex 语法

在 Markdown 中插入 Latex 公式：

- 单行公式：`$ latex code $`

<center>

```
${f(x)=a_nx^n+a_{n-1}x^{n-1}+a_{n-2}x^{n-2}}+\cdots$
```
</center>

&emsp;&emsp;显示效果：
<center>

${f(x)=a_nx^n+a_{n-1}x^{n-1}+a_{n-2}x^{n-2}}+\cdots$
</center>

- 多行公式：`$$ latex code $$`

<center>

```
$$a+\rlap{\overbrace{\phantom{b+c+d}}^m}b+\underbrace{c+d+e}_n+f$$
```
</center>

&emsp;&emsp;显示效果：
<center>

$$ a+\rlap{ \overbrace{ \phantom{b+c+d}}^m} b++\underbrace{c+d+e}_n+f $$
</center>


### Latex 数学规则

#### 上下标
` ^ `表示上标,` _ `表示下标。如果上下标的内容多于一个字符，要用大括号` { } `把这些内容括起来当成一个整体。上下标是可以嵌套的，也可以同时使用。

- 公式：`$\sum_i^na_i$`

- 效果：$\sum_i^na_i$

#### 分数
分数的输入形式为` \frac{分子}{分母}`

- 公式：`$P(v)=\frac{1}{1+exp(-v/T)}$`

- 效果：$P(v)=\frac{1}{1+exp(-v/T)}$

#### 上下划线和括号

- 上划线
  - 公式：`\overline{a+b+c}`
  - 效果：$\overline{a+b+c}$

- 下划线
  - 公式：`\underline{a+b+c}`
  - 效果：$\underline{a+b+c}$

- 上划左箭头
  - 公式：`\overleftarrow{a+b}`
  - 效果：$\overleftarrow{a+b}$

- 下划右箭头
  - 公式：`\underrightarrow{a+b}`
  - 效果：$\underrightarrow{a+b}$

- 下划双箭头
  - 公式：`\underleftrightarrow{a+b}`
  - 效果：$\underleftrightarrow{a+b}$

- 向量箭头
  - 公式：`\vec x = \vec{AB}`
  - 效果：$\vec x = \vec{AB}$

- 上括号
  - 公式：`\overbrace {a+b}^\text{a,b}`
  - 效果：$\overbrace {a+b}^\text{a,b}$

- 下括号
  - 公式：`\underbrace {d+e}^\text{d,e}`
  - 效果：$\underbrace {d+e}^\text{d,e}$

- 上下括号
  - 公式：`a+\rlap{\overbrace{\phantom{b+c+d}}^m}b+\underbrace{c+d+e}_n+f`
  - 效果：$a+\rlap{\overbrace{\phantom{b+c+d}}^m}b+\underbrace{c+d+e}_n+f$

#### 根号

- 二次根
  - 公式：`\sqrt{12}`
  - 效果：$\sqrt{12}$

- n次根
  - 公式：`\sqrt[n]{12}`
  - 效果：$\sqrt[n]{12}$

#### 括号
`(), [] , | `分别表示原尺寸的形状，由于大括号` {} `在 LaTeX 中有特定含义, 所以使用需要转义, 即`\{ `和` \} `分别表示表示`{ }`。当需要显示大尺寸的上述符号时, 在上述符号前加上` \left `和` \right `命令.

- 公式：`f(x,y,z) = \{3y^2z + \left( 3 +\frac{7x+5}{1+y^2} \right)\}+7`

- 效果：$f(x,y,z) = \{3y^2z + \left( 3 +\frac{7x+5}{1+y^2} \right)\}+7$

- 括号的其他用法

| 功能	| 语法	| 显示 |
|:---|:---|:---:|
|圆括号，小括号|	`\left( \frac{a}{b} \right)`|$\left( \frac{a}{b} \right)$|
|方括号，中括号|	`\left[ \frac{a}{b} \right]` |$\left[\frac{a}{b} \right]$|
|花括号，大括号|	`\left\{ \frac{a}{b} \right\}` |$\left\{ \frac{a}{b} \right\}$|
|尖括号|	`\left \langle \frac{a}{b} \right \rangle`|$\left \langle \frac{a}{b} \right \rangle$|
|单竖线，绝对值|	```\left| \frac{a}{b} \right|```	|$\left | \frac{a}{b} \right|$|
|双竖线，范式|`\left \| \frac{a}{b} \right \|`| $\left \| \frac{a}{b} \right \|$|
|取整函数	|`\left \lfloor \frac{a}{b} \right \rfloor`|$\left \lfloor \frac{a}{b} \right \rfloor$|
|取顶函数|	`\left \lceil \frac{c}{d} \right \rceil`|$\left \lceil \frac{c}{d} \right \rceil$|
|斜线与反斜线|	`\left / \frac{a}{b} \right \backslash`	|$\left / \frac{a}{b} \right \backslash$|
|上下箭头|	`\left \uparrow \frac{a}{b} \right \downarrow`|	$\left \uparrow \frac{a}{b} \right \downarrow$|
|混合括号1|	`\left [ 0,1 \right )`|$\left [ 0,1 \right )$|
|混合括号2|	`\left \langle \psi \right\|`	|$\left \langle \psi \right\|$|
|单左括号|	`\left \{ \frac{a}{b} \right .`	|$\left \{ \frac{a}{b} \right .$|
|单右括号|	`\left . \frac{a}{b} \right \}`|$\left . \frac{a}{b} \right \}$|

#### 矩阵
矩阵中, 不同的列使用` & `分割, 行使用` \\ `分隔

下面展示一系列矩阵环境排版, 区别在于外面的括号不同

- 基本公式：
    ```LaTeX
    \begin{matrix type}
    a & b \\
    c & d
    \end{martrix type}
    ```

- 效果：
    $$
    \begin{pmatrix}
    a & b \\
    c & d
    \end{pmatrix}
    $$

- Martrix Type:


$$\begin{align*}

matrix \quad
\begin{matrix}
a & b \\
c & d
\end{matrix}
&

\qquad pmatrix \quad
\begin{pmatrix}
a & b \\
c & d
\end{pmatrix}
\\

\quad vmatrix \quad
\begin{vmatrix}
a & b \\
c & d
\end{vmatrix}
&

\qquad Vmatrix \quad
\begin{Vmatrix}
a & b \\
c & d
\end{Vmatrix}
\\

\qquad bmatrix \quad
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
&

\qquad Bmatrix \quad
\begin{Bmatrix}
a & b \\
c & d
\end{Bmatrix}

\end{align*}$$

#### 省略号

$$
\begin{eqnarray*}
&ldots \quad \ldots \\
&cdots \quad \cdots \\
&vdots \qquad \vdots \\
&ddots \quad \ddots \\
\end{eqnarray*}
$$

#### 公式环境
- `  equation `环境用来输入单行公式, 自动生成编号, 也可以使用`  \tag{...}  `自己对公式编号;

- 使用`  equation*  `环境, 不会自动生成公式编号, 后续介绍的公式输入环境都是在自动编号后面加上`  *  `便是不自动编号环境.

  - 公式：
    ```LaTeX
    \begin{equation}
    (a+b)+c = a+(b+c)\\
    (a+b) \times c = a\times c + b \times c \tag{1}
    \end{equation}
    ```

  - 效果：
  $$
  \begin{equation}
  (a+b)+c = a+(b+c)\\
  (a+b) \times c = a\times c + b \times c \tag{1}
  \end{equation}
  $$

- `\[ ... \] `是`  equation*  `环境的简写：
- `eqnarray `环境用来输入按照等号(或者其他关系符)对齐的方程组, 编号

  - 公式：
    ```LaTeX
    $$
    \begin{eqnarray}
    f(x) = a_nx^n \\
    g(x) = x^2
    \end{eqnarray}
    $$
    ```

  - 效果：
    $$
    \begin{eqnarray}
    f(x) = a_nx^n \\
    g(x) = x^2
    \end{eqnarray}
    $$

- 输入多行公式,`  gather  `环境得到的公式是每行居中的

  - 公式：
    ```LaTeX
    $$
    \begin{gather}
    (a+b) \times c = a\times c + b \times c \notag \\
    ac= a\times c \\
    \end{gather}
    $$
    ```

  - 效果：
  $$
  \begin{gather}
  (a+b) \times c = a\times c + b \times c \notag \\
  ac= a\times c \\
  \end{gather}
  $$

- `  align `环境则允许公式按照等号或者其他关系符对齐, 在关系符前加` & `表示对齐

  - 公式：
    ```LaTeX
    $$
    \begin{align}
    y &= \cos t + 1 \\
    y &= 2sin t \\
    \end{align}
    $$
    ```

  - 效果：
  $$
  \begin{align}
  y &= \cos t + 1 \\
  y &= 2sin t \\
  \end{align}
  $$

- ` align `环境还允许排列多列对齐公式, 列与列之间使用` & `分割

  - 公式：
    ```LaTeX
    $$
    \begin{align*}
     x &= t & x &= \cos t &  x &= t \\
     y &= 2t & y &= \sin (t+1) & y &= \sin t \\
    \end{align*}
    $$
    ```

  - 效果：
  $$
  \begin{align*}
   x &= t & x &= \cos t &  x &= t \\
   y &= 2t & y &= \sin (t+1) & y &= \sin t \\
  \end{align*}
  $$

- align 环境中列分隔符 & 一般放在关系符前面, 如果个别需要再关系符后面或者别的地方对齐的, 则应该注意使用的符号类型

  - 公式：
    ```LaTeX
    $$
    % 关系符后对齐，需要使用空的分组
    % 代替关系符右侧符号，保证间距
    \begin{align*}
    & (a+b)(a^2-ab+b^2) \notag \\
    ={ } & a^3 - a^2b + ab^2 + a^2b - ab^2 + b^2 \notag \\
    ={ } & a^3 + b^3 \label{eq:cubesum}
    \end{align*}
    $$
    ```

  - 效果：
  $$
  % 关系符后对齐，需要使用空的分组
  % 代替关系符右侧符号，保证间距
  \begin{align*}
  & (a+b)(a^2-ab+b^2) \notag \\
  ={ } & a^3 - a^2b + ab^2 + a^2b - ab^2 + b^2 \notag \\
  ={ } & a^3 + b^3 \label{eq:cubesum}
  \end{align*}
  $$

#### 跨行公式

- 单个公式很长的时候需要换行，但仅允许生成一个编号时，可以用 split 环境包围公式代码，在需要转行的地方使用 \. split 环境一般用在 equation, gather 环境里面, 可以把单个公式拆成多行, 同时支持 align 那样对齐公式.

  split 环境不产生编号, 编号由外面的数学环境产生; 每行需要使用1个&来标识对齐的位置，结束后可使用 \tag{...} 标签编号。 如果 split 环境中某一行不是在二元关系符前面对齐, 需要通过 \quad 等手段设置间距或对齐方式.

  - 公式：
    ```LaTeX
    $$
    % 注意 \tag{...} 编号的位置
    \begin{equation}
    \begin{split}
    \cos 2x &= \cos^2 x - \sin^2 x \\
            &= 2\cos^2 x - 1
    \end{split} \tag{3.1}
    \end{equation}
    $$
    ```

  - 效果：
  $$
  % 注意 \tag{...} 编号的位置
  \begin{equation}
  \begin{split}
  \cos 2x &= \cos^2 x - \sin^2 x \\
          &= 2\cos^2 x - 1
  \end{split} \tag{3.1}
  \end{equation}
  $$

#### 公式块

- 最常见的是` case `环境, 他在几行公式前面用花括号括起来, 表示几种不同的情况; 每行公式使用` & `分隔, 便是表达式与条件, 例如

  - 公式：
    ```LaTeX
    $$
    \begin{equation}
    D(x) = \begin{cases}
    1, & \text{if } x \in \mathbb{Q}; \\
    0, & \text{if } x \in
         \mathbb{R}\setminus\mathbb{Q}.
    \end{cases}
    \end{equation}
    $$
    ```

  - 效果：
  $$
  \begin{equation}
  D(x) = \begin{cases}
  1, & \text{if } x \in \mathbb{Q}; \\
  0, & \text{if } x \in
       \mathbb{R}\setminus\mathbb{Q}.
  \end{cases}
  \end{equation}
  $$

  - ` gathered `环境 将几行公式居中排列, 组合为一个整体;

    - 公式：
      ```LaTeX
      $$
      \left. \begin{gathered}
      S \subseteq T \\
      S \supseteq T
      \end{gathered} \right\}
      \implies S = T
      $$
      ```

    - 效果：
    $$
    \left. \begin{gathered}
    S \subseteq T \\
    S \supseteq T
    \end{gathered} \right\}
    \implies S = T
    $$
