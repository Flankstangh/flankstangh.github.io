## Diffusing Knowledge notes

[TOC]

### Model 4.1：
这是一个变量比较多的OLS模型：

$$Y=\rho P+W\beta +\epsilon \tag{4.1}$$

- $Y$ : 城市化率
- $P$ : 新教教义的推广程度
- $\rho$ : coefficients，衡量新教对于经济增长的影响程度
- $W$ : Indenpendent variables
  $$
  W\in
  \begin{bmatrix}
  \rm
  {Catholicism \\
  \color{teal}
  {Treaty\ ports^* \\
  Railways^* \\}
  \color{purple}
  {Small\ city^*\\
  Middle\ city^*\\
  Large\ city^*\\}
  Prefectual\ government^*\\
  \color{maroon}{
  Grand\ Canal^*\\
  Yangtze\ river^*\\
  On\ the\ coast^*\\}
  Population\ density\\
  size\ of\ the\ county\\
  Province\ dummies\\
  Constant\ term}
  \end{bmatrix}
  $$

- $\beta$ : coefficients of control variables $W$

回归结果如下：

![](image\table2.png)


### Model 4.2:
面板数据和横断面数据的区别在于，面板数据多了时间的维度，个体和同期其他个体的差异称为组间差异，和不同时期自己的差异称为组内差异。

固定效应模型为每个个体单独设置一个变量，这个变量代表了个体不随时间变化的特质，这些固定效应变量就用于衡量个体的组间差异。

这篇文章的第二个模型是双向固定效应模型（Two-way fixed effect model），加入了时间$t$和个体$i$的固定效应变量：
$$Y_{it}=\rho P_{it}^d+\alpha_i+\lambda_t+\sigma_{it}  \tag{4.2.1} $$

对模型进行一阶差分，剔除了个体的固定效应变量，只留下不同period的时间效应：
$$\Delta Y_{it-1}=\rho \Delta P_{it}^d+\Delta \lambda_t+ \Delta \sigma_{it} \tag{4.2.2}$$

- $Y_{it}$：在$Period_t$时刻$County_i$中的企业数目
- $\Delta Y_{it-1}$：$County_i$中的企业数目的五年增长率
- $\alpha_i$：county fixed effect
- $\lambda_t$：period fixed effect
- $P_{it}^d$：$Period_t$时期新教在$County_i$中的持续时间
- $\Delta P_{it}^d$：可以理解为dummy variable，存在新教的County值为5，没有新教的County为0
- $\rho$：coefficients，衡量有新教\没有新教的County中公司数目的年度增长率

#### 修正1

为了保证 **新教County中modern industrial firms数量增长率高** 这个结果完全是由 $\Delta P_{it}^d$ 影响，而不是未观测的共同趋势，作者继续建立了下面这个模型：

$$Y_{it}=\rho P_{it}^d+(\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau})B_i+ \alpha_i+\lambda_t+\sigma_{it} \tag{4.2.3}$$

这个模型是$4.2.1$的修正，因此不是差分形式。

- $B_i$：dummy variable，表示截至1920年，新教在$County_i$中是否记载存在
- $I_{\tau} \phi_{\tau}$：代表$Period_\tau$时间效应的dummy variable

这一部分作者讲的非常不清楚， $(\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau})B_i$ 这一项中的 $I_{\tau}$ 和 $\phi_{\tau}$ 根本没有说明变量含义，而且也根本不解释为什么加入这一项就可以表示 $\rm{unobserved\ growth\ trend}$。

实际上，这种类似 $\sum_{k=2}^K\beta_k$的项在固定效应模型中很常见，可以简单地把 $\beta_k$理解成随时间变化的截距项。

对于 $\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau}$ 来说， $\phi_{\tau}$ 是常数，$I_{\tau}$ 才是真正的dummy variable，这一项展开是这样：
$$\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau}=\phi_2I_2+\phi_3I_3+\ldots+\phi_{15}I_{15} $$
为了更好理解，随便赋个值：
$$\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau}=3I_2+5I_3+\ldots+2I_{15} $$
把这个序列放在二维坐标轴上，实际上就是一条斜向上的线，这也就是作者所说的 $\rm{unobserved\ growth\ trend}$。

接下来说$B_i$，当$B_i=1$，表示$County_i$中存在新教，这时 $\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau}$ 就被加入了模型。

在模型中加入 $\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau}$ 和$B_i$的交互项，实际就是当County中存在新教时，趋势就成为了一个变量，被模型控制住了。


除了 $(\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau})B_i$，作者还说可以加入 $B_iT_{it}$ 表示趋势。这个相对就好理解多了，$T_{it}$ 是 $Period_t$ 时 $County_i$ 的趋势，当$B_i=1$，这个趋势也就成为了控制变量。

#### 修正2

在模型4.2.3基础上，作者继续进行修正：
$$Y_{it}=\rho P_{it}^d+(\sum_{\tau =2}^{15}\phi_{\tau}I_{\tau})B_i+Z_{it}\psi\\
+\sum_{\tau=2}^{15}I_{\tau}w_i\Phi_{\tau}+\alpha_i+\lambda_t+\sigma_{it} \tag{4.2.4} $$

- $Z_{it}$：条约开放港口和铁路网存在时段
- $\psi$：coefficients matrix
- $I_{\tau}W_i$：和上面一样，只不过$I_{\tau}$ 是真正的0-1虚拟变量
- $\Phi_{\tau}$：某个dummy variable，作者又没说

解释完上面那个模型，这个理解起来就会容易许多了，最终的回归结果为$Table\ 3$的column(4)~column(6)。

### Model 4.3

由于可能存在的新教传播指标$P$（每万人中的传教者数量）测量误差、反向因果关系和遗漏变量，新教对经济繁荣影响程度的计量会产生偏误。因此，作者试图寻找一个可用的工具变量，用来衡量新教的传播程度。

考虑到义和团运动导致传教士产生大规模向南移动，作者构建了如下一个工具变量$DS$：

- $D$：到最近义和团冲突地区的距离
- $S$：dummy variable，表示County是否属于长江协议（Yangtze Compact）缔约区域
- $DS$：$D$和$S$的交互项

接着，作者建立如下线性模型判断工具变量是否可靠：
$$P=\delta_1D+\delta_2S+\delta_3DS+v \tag{4.3.1}$$

模型$4.3.1$实际上就是2SLS的第一步。

为了确保$DS$和$P$之间的关系不受未观测到的地理因素影响，除了$S$，作者进一步控制了更多空间变量：
$$P=\delta_1D+\delta_3DS+\bar{W}\gamma+v \tag{4.3.2}$$

- $\bar{W}$：independent control variables，包括
$$
  \bar{W}\in
  \begin{bmatrix}
  \rm
  {模型4.1中W中所有变量\\
  Distance\ to\ the\ sea\\
  Distance\ to\ 5\ ports\\
  以上所有变量和S的交互项
  }
  \end{bmatrix}
$$

由于 $\bar{W}$ 包括了 $Province\ dummy$，因此$S$就被省略了。

#### Falsification Tests

一个有效的工具变量$IV$，除了要满足和内生变量$P$的强相关性，还应该满足和其他变量都不相关，为此，作者针对以下三个问题进行测试：

1. 按照逻辑，$DS$应该只在义和团运动后对$P$产生影响，若在义和团运动之前二者产生关联，则说明$DS$可能和其他变量有相关性；
2. $DS$应该对新教学校招生密度产生积极影响（Protestantism的一个Proxy），而不是对政府学校招生密度产生影响（Economic development的一个Proxy）。因此，如果$DS$影响了政府学校，则说明其可能与遗漏变量有关联；
3. $DS$还可能通过外国影响（西方商业）、普遍的城市化等对经济繁荣产生影响

**对于第一个问题**，作者对模型4.3.2进行拓展，建立了一个随机效应模型：
$$\begin{gather}
P_{it}^d=\psi_1\cdot Post\cdot D_iS_i+\psi_2\cdot D_iS_i+\psi_3\cdot Post \cdot D_i \\
+\psi_4 \cdot D_i+\bar{Z_{it}}\Pi+ui +\lambda_t+v_{it} \tag{4.3.3}
\end{gather}$$

- $\bar{Z_{it}}$：包含模型4.2.4中所有控制变量
- $Post$：一个判断义和团运动是否开始的 dummy variable
- $\Pi$：$\bar{Z_{it}}$ 的coefficient matrix
- 其余变量意义同4.3.2

对这个模型进行回归，根据回归结果可以得出结论，$DS$只在义和团运动后对$P$产生巨大影响。

**对于第三个问题**，作者将模型4.3.3中的因变量分别换为 $\rm{Domestically\ owned\ firms}$ 和 $\rm{Western\ firms}$ 进行回归，结果显示$DS$和本地企业有显著的相关性，和西方又不显著的相关性。

**对于第二个问题**，依旧是这种分析方法，将模型因变量换为两种学校的入学率，回归结果显示$DS$对教会学校入学率有显著的积极影响，对政府学校的入学率没有显著影响。

#### Instrumented Protestantism
验证了工具变量$DS$的有效性后，就可以利用2SLS再次对最开始的模型4.1进行回归：
$$
\begin{equation}
Y=\rho P+\eta_1 D+bar{W}\beta+\epsilon\\
P=\delta_3DS+\delta_1D+\bar{W}\gamma+v
\tag{4.3.4}
\end{equation}
$$

结果显示在 $Table 6$ Column(1)、(2)，和OLS进行对比，主要有以下区别：

  1. 在OLS中，当加入 $\rm{Initial\ economic\ conditions}$ 后，$P$的显著性和系数都变小了，而在2SLS中，加入后因变量的显著性和系数反而变大了；
  2. 当使用平均值估计时，2SLS结果显示，一万人中每增加一名传教者，总城镇化率将提高18.8%？（这也太高了）比OLS估计的结果要高出许多

这两条证明OLS估计确实产生了偏误，而2SLS可以纠正这种误差。

#### 义和团的影响
但目前为止还没能排除义和团直接影响$P$的可能性。因此，作者在模型4.3.4中加入了一个义和团兴起的dummy variable。

最终2SLS回归结果 $Table 6$ Column(3) 显示这个变量对结果没有显著影响。

进一步考虑地域的影响，义和团运动主要在中国北方兴起，南方省份的结果或许会导致整体数据产生误差。为此作者挑出了两个南方省份：广东和广西，并对它们单独进行2SLS。

最终的结果如 $Table 6$ Column(4) ，和整体区别不大，因此可以证明南北地区太大差异。

### 最终公式
第四节最后，作者综合了2SLS、Fixed effect、Random effect的所有模型，得到了衡量经济繁荣程度和新教传播范围的最终公式：
$$\begin{equation}
Y_{it}=\rho\cdot P_{it}^d+\bar{\omega}\cdot Post\cdot D_i+\bar{Z_{it}}\Phi+\alpha_i+\lambda_t+\epsilon_{it}\\
P_{it}^d=\psi_1\cdot Post\cdot D_iS_i+\psi_3\cdot Post\cdot D_i+\bar{Z_{it}}\Pi+\tilde{\alpha_i}+\tilde{\lambda_t}+v_{it}
\tag{4.3.5}
\end{equation}
$$
