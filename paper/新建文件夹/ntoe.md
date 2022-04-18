## 五、Topology Attack and Defense for Graph Neural Networks: An Optimization Perspective

这篇文章发表于IJCAI'19，前面两篇文章都采用贪心的策略（通过梯度信息／对Loss的贡献）在每一轮施加一个扰动，本文则采用了一种基于优化的方式实现图对抗攻击。和第二篇文章一样，这篇文章也是基于对图结构的修改降低模型的整体节点分类性能。

首先引入一个01对称矩阵 ![[公式]](https://www.zhihu.com/equation?tex=%7B%5Cbf+S%7D+%5Cin+%5C%7B+0%2C+1+%5C%7D%5E%7BN%5Ctimes+N%7D) 用来编码图上的某条边是否被修改（ ![[公式]](https://www.zhihu.com/equation?tex=S_%7Bij%7D%3DS_%7Bji%7D%3D1) 代表边 ![[公式]](https://www.zhihu.com/equation?tex=%28i%2Cj%29) 被修改）。对于图的邻接矩阵 ![[公式]](https://www.zhihu.com/equation?tex=A) ，有其补矩阵 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbar%7B%5Cbf+A%7D%3D%7B%5Cbf%7B1%7D%5Cbf%7B1%7D%5ET%7D-+%7B%5Cbf%7BI%7D%7D+-+%7B%5Cbf+A%7D)，其中 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+I) 是单位矩阵，这个式子的意思是在 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbar%7B%5Cbf+A%7D) 中原来邻接矩阵为1的地方现在等于-1，原来邻接矩阵为0的地方现在等于1。这样一来可以将扰动后的图表示为 ![[公式]](https://www.zhihu.com/equation?tex=%7B%5Cbf+A%27%7D%3D%7B%5Cbf+A%7D%2B%7B%5Cbf+C%7D+%5C+%5Ccirc++%5C+%7B%5Cbf+S%7D%2C++%5C+%7B%5Cbf+C%7D%3D+%5Cbar%7B%5Cbf+A%7D-%7B%5Cbf+A%7D) ，其中 ![[公式]](https://www.zhihu.com/equation?tex=%5Ccirc) 代表逐元素乘，也就是说原来邻接矩阵为1的地方（有边）如果有扰动（S中对应的位置为1），则扰动后 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+A%27) 对应的位置为1+(-1)*1=0（无边），反之亦然。由此，确定了 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+S) 就确定了 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+A%27) 。

接下来定义攻击目标：令 ![[公式]](https://www.zhihu.com/equation?tex=%7B%5Cbf+Z%7D%28%7B%5Cbf+S%7D%2C+%7B%5Cbf+W%7D%3B+%7B%5Cbf+A%7D%2C+%5C%7B+%7B%5Cbf+x%7D_i+%5C%7D+%29) 代表在扰动后的图上得到的预测概率，即 ![[公式]](https://www.zhihu.com/equation?tex=Z_%7Bi%2Cc%7D) 代表预测节点 ![[公式]](https://www.zhihu.com/equation?tex=i) 属于类别 ![[公式]](https://www.zhihu.com/equation?tex=c) 的概率。大部分工作基于交叉熵定义攻击的loss，本文提出了一种类似CW attack[[7\]](https://zhuanlan.zhihu.com/p/88934914#ref_7)的loss：

![[公式]](https://www.zhihu.com/equation?tex=f_i%28%7B%5Cbf+S%7D%2C+%7B%5Cbf+W%7D%3B+%7B%5Cbf+A%7D%2C+%5C%7B+%7B%5Cbf+x%7D_i+%5C%7D%2C+y_i%29+%3D+%5Cmax+%5C%7B+Z_%7Bi%2Cy_i%7D+-++%5Cmax%5Climits_%7Bc+%5Cne+y_i%7D+Z_%7Bi%2Cc%7D%2C+-+%5Ckappa+%5C%7D+%5C%5C)

和之前的工作一样，需要限制扰动的数量，本文用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+S) 编码对图结构的扰动，接下来为了简便用 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+s) 替代 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+S) （小写的 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+s) 代表 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+S) 取上三角并摊平成向量，因为研究的是无向图），那么优化目标可以写成：

![[公式]](https://www.zhihu.com/equation?tex=%5Cunderset+%7B%7B%5Cbf+s%7D%7D+%7B%5Ctext+%7Bminimize%7D%7D+%5Csum_%7Bi%5Cin+%5Cmathcal%7BV%7D%7D+f_i%28%7B%5Cbf+s%7D%3B+%7B%5Cbf+W%7D%2C+%7B%5Cbf+A%7D%2C+%5C%7B+%7B%5Cbf+x%7D_i+%5C%7D%2C+y_i%29+%5C%5C+%5Ctext%7Bsubject+to%7D+%5C+%5C+%5C+%5C+%7B%5Cbf+1%7D%5ET+%7B%5Cbf+s%7D+%5Cle+%5Cepsilon+%2C+%7B%5Cbf+s%7D+%5Cin+%5C%7B0%2C1%5C%7D%5En)

其中 ![[公式]](https://www.zhihu.com/equation?tex=%5Cepsilon) 就是对扰动数目的约束。这是一个组合优化问题，因此为了便于优化，将 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+s) 松弛成离散量，松弛后的优化目标写作下式：

![[公式]](https://www.zhihu.com/equation?tex=%5Cunderset+%7B%7B%5Cbf+s%7D%7D+%7B%5Ctext+%7Bminimize%7D%7D+%5Csum_%7Bi%5Cin+%5Cmathcal%7BV%7D%7D+f_i%28%7B%5Cbf+s%7D%3B+%7B%5Cbf+W%7D%2C+%7B%5Cbf+A%7D%2C+%5C%7B+%7B%5Cbf+x%7D_i+%5C%7D%2C+y_i%29+%2C+%5Ctext%7Bsubject+to%7D+%5C+++%7B%5Cbf+s%7D+%5Cin+%5Cmathcal%7BS%7D+%5C%5C)

其中 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BS%7D%3D%5C%7B+%7B%5Cbf+s%7D+%7C+%7B%5Cbf+1%7D%5ET+%7B%5Cbf+s%7D+%5Cle+%5Cepsilon%2C+%7B%5Cbf+s%7D+%5Cin+%5B0%2C1%5D%5En+%5C%7D) ，将 ![[公式]](https://www.zhihu.com/equation?tex=%5Cbf+s) 从二值的离散量松弛到0到1之间的离散量，这样一来就可以用优化方法求解，本文通过下面的算法将求解结果还原为最终解

![img](https://pic4.zhimg.com/80/v2-c38bb4f37908d7b653cc540cc55f36c7_720w.jpg)

在优化过程中，每一步通过梯度下降法更新，但由于存在扰动数量的约束，更新后的解可能会跳出约束条件，因此需要通过映射梯度下降法将解映射到满足约束条件的解空间中。

![img](https://pic1.zhimg.com/80/v2-a5880e9eae6a4d64ce31d644852b78b4_720w.jpg)

![img](https://pic2.zhimg.com/80/v2-111dcc5c3f40c1c64abb210bdddc2f71_720w.jpg)

这里的映射过程实际上相当于在扰动数量约束下找一个离待定解二阶距离最近的解。

![img](https://pic3.zhimg.com/80/v2-15d1ab88dafb10bf0d930a6510b7597e_720w.jpg)

通过使用拉格朗日乘子法求解可以得到前面的映射表达式。 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu) 是个非负数，其大小则可以根据二分法求解（若待定解已经满足约束，则 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu+%3D+0) ，否则 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmu+%3E+0) ）。

由此，循环使用映射梯度下降法，最后用前面的采样方法得到最终解，就可以生成扰动图。