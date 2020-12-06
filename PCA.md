## 主成分分析 (Principle Component Analysis)

### PCA的作用
PCA的主要作用是降维。

如下图，数据点大部分都分布在$x_2$方向上，在$x_1$方向上的取值近似相同，那么对于有些问题就可以直接将$x_1$坐标的数值去掉，只取$x_2$坐标的值即可。但是有些情况不能直接这样取，例如：
<center>

![PCA1](https://imgconvert.csdnimg.cn/aHR0cDovL2Jsb2dpbWcucGlnZ3lnYWdhLnRvcC9ibG9nL1BDQXgyLnBuZw?x-oss-process=image/format,png)
</center>

这个时候就是PCA展现作用的时候了。黑色坐标系是原始坐标系，红色坐表系是我后面构建的坐标系，如果我的坐标系是红色的，那么这个问题是不是就和上面那个问题一样了，我只需要去掉$y_2$坐标系的数据即可。

<center>

![PCA2](https://imgconvert.csdnimg.cn/aHR0cDovL2Jsb2dpbWcucGlnZ3lnYWdhLnRvcC9ibG9nL1BDQXBwcC5wbmc?x-oss-process=image/format,png)
</center>

### PCA的数学原理

构建一个函数 $f(X_{m \times n})$，是这个函数可以将矩阵$X_{m \times n}$ 降维，矩阵$X$是原始数据，矩阵的每一行是一个样本的特征向量，即矩阵$X_{m\times n}$ 中有$m$个样本，每个样本有$n$个特征值。所以，所谓的降维，其实是减少$n$的数量。

假设降维后的结构为$Z_{m \times k}$ ,其中$k<n$，那么PCA的数学表达可以这样表示：
$$Z_{m×k}=f(X_{m×n}),k<n$$

为了找到上面说的$f(x)$ 我们需要做一些工作，在线性空间中，矩阵可以表示为一种映射，所以上面的问题可以转化为寻找这样一个矩阵$W$，该矩阵可以实现上面的映射目的：
$$Z_{m\times k} = W_{n\times k}X_{m\times n}$$

最大化新坐标轴上的方差，就是让数据更加分散：
$$
\begin{equation}
\max\limits_{w}\frac{1}{m}\sum\limits_{i}^{m}(z_i - \bar{z})^2 \\
s.t. \ \ \ \ \lVert W \rVert_2 = 1
\end{equation}
$$

将上面的优化问题转化一下：

$$
\begin{align}
&\ \ \ \ \ \max\limits_{w}\frac{1}{m}\sum\limits_{i}^{m}(z_i-\bar{z})^2\\
&=\max\limits_{w}\frac{1}{m}\sum\limits_{i}^{m}(wx_i-w\bar{x})^2\\
&=\max\limits_{w}\frac{1}{m}\sum\limits_{i}^{m}(w(x_i-\bar{x}))(w(x_i-\bar{x}))^T\\
&=\max\limits_{w}\frac{1}{m}\sum\limits_{i}^{m}(w(x_i-\bar{x})(x_i-\bar{x})^Tw^T )^T\\
&=\max\limits_{w}\frac{1}{m}w\sum\limits_{i}^{m}(x_i-\bar{x})(x_i-\bar{x})^Tw^T\\
&=\max\limits_{w}\frac{1}{m}wCov(x)w^T
\end{align}
$$

最终目标转化为：
$$
\begin{equation}
=\max\limits_{w}\frac{1}{m}wCov(x)w^T \\
s.t. \ \ \ \ \lVert W \rVert_2 = 1
\end{equation}
$$
