# Mettack

ADVERSARIAL ATTACKS ON GRAPH NEURAL NETWORKS VIA META LEARNING

ICLR'19

研究的是对模型**整体分类性能**的攻击

[知乎]: https://zhuanlan.zhihu.com/p/88934914

**主要思想**：

​	元学习最初被用作超参学习。可以将图数据当作超参数，让元学习来优化。



**问题描述**：

![image-20220417204531328](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220417204531328.png)

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D)：对抗攻击的目标函数。攻击者希望降低模型在测试集（未知标记的节点）上的泛化性能，一种方式是令 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D%3D-%5Cmathcal%7BL%7D_%7Btrain%7D) ，也就是最大化模型在训练集上的loss。

除此以外，也可以借助self-learning的方式，令 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D%3D-%5Cmathcal%7BL%7D_%7Bself%7D%3D-%5Cmathcal%7BL%7D%28%5Cmathcal%7BV%7D_U%2C%5Chat%7BC%7D_U%29) ，这里 ![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7BC%7D_U) 代表原模型在测试集上的预测结果，也就是让攻击后模型的预测结果尽可能与原模型不同。



**元学习思想**：

meta-learning中meta-gradients概念。

将图的结构作为超参数，通过下式计算梯度：

![image-20220418150631738](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418150631738.png)

其中opt(·)是一个可微的优化过程（比如梯度下降法）而 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Btrain%7D) 代表训练误差。

现在假设这个内层优化过程是简单的梯度下降，其学习率为 ![[公式]](https://www.zhihu.com/equation?tex=%5Calpha) ，初识参数为 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta_0) ，那么

![image-20220418153211838](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418153211838.png)

如果优化了 ![[公式]](https://www.zhihu.com/equation?tex=T) 步后攻击者的loss为 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D%28f_%7B%5Ctheta_T%7D%28G%29%29) ，那么meta-gradient可以通过展开训练过程表示成：

![image-20220418153505444](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418153505444.png)

对于 ![[公式]](https://www.zhihu.com/equation?tex=%5Cnabla_G+%5Ctheta_T) 这一项，可以不断展开直到 ![[公式]](https://www.zhihu.com/equation?tex=%5Ctheta_0)。由此，可以根据计算出的meta-gradient对图执行 ![[公式]](https://www.zhihu.com/equation?tex=%5CDelta) 次meta update。由于图的离散性，在更新图时每一步还是根据贪心策略执行离散的更新：对于每一个点对 ![[公式]](https://www.zhihu.com/equation?tex=%28u%2Cv%29) ，计算 ![[公式]](https://www.zhihu.com/equation?tex=S%28u%2Cv%29%3D%5Cnabla_%7Ba_%7Buv%7D%7D%5E%7Bmeta%7D%5Ccdot+%28-2%5Ccdot+a_%7Buv%7D+%2B+1%29) ，然后每一轮选择 ![[公式]](https://www.zhihu.com/equation?tex=S%28u%2Cv%29) 最大的点对，执行相应的更新（如果原来有边就删边，原来无边就加边）。

本文还提供了几种近似meta-gradient的方法。

![img](https://pic2.zhimg.com/80/v2-a3d4c439bc58591247079e51e739a835_720w.png)

这种近似相当于直接取模型训练 ![[公式]](https://www.zhihu.com/equation?tex=T) 步后 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D) 对数据的梯度，忽略了中间的训练动态。

![img](https://pic4.zhimg.com/80/v2-81b303ea05cfd1da1762202c14c15f47_720w.png)

这种近似假设训练中每一步的参数之间独立，取每一步训练中计算的梯度的平均作为近似。



**实验**：

![image-20220418195026497](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418195026497.png)

**DICE** （‘delete internally, connect externally’） 随机制造扰动作为baseline

**First-order**（approximation）忽略所有二阶导数



十次迭代就能实现有效攻击：

![image-20220418213204682](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418213204682.png)

PUNMED数据集（19717个节点、44338条边、500维特征、3类）

![image-20220418213748794](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418213748794.png)

GCN模型在不同数量扰动下的准确率：

![image-20220418220825317](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418220825317.png)

训练权重：

![image-20220418222315371](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418222315371.png)

**对攻击边和原始边的分析**：

the edge betweeness centrality（Ce）

更倾向于连接略高于平均最短距离的两点，以及度比较低的点

![image-20220418223119945](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418223119945.png)

元攻击中的扰动大多是增加边

并且符合同质性假设（相似类别的节点之间存在边）

![image-20220418223528183](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418223528183.png)

选择10%的节点，并随机选择这些节点的邻居，直到有30%的节点组成子图，进行扰动，将扰动后的边加入原图：

![image-20220418230716652](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220418230716652.png)