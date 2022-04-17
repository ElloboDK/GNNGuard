# Mettack

ADVERSARIAL ATTACKS ON GRAPH NEURAL NETWORKS VIA META LEARNING

ICLR'19

研究的是对模型**整体分类性能**的攻击

[知乎笔记]: https://zhuanlan.zhihu.com/p/88934914

主要思想：

​	元学习最初被用作超参学习。可以将图数据当作超参数，让元学习来优化。



问题描述：

![image-20220417204531328](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220417204531328.png)

![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D)表示对抗攻击的目标函数。在这里因为攻击者希望降低模型在测试集（未知标记的节点）上的泛化性能，而测试数据的label是未知的，因此一种方式是令 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D%3D-%5Cmathcal%7BL%7D_%7Btrain%7D) ，也就是最大化模型在训练集上的loss。除此以外，也可以借助self-learning的方式，令 ![[公式]](https://www.zhihu.com/equation?tex=%5Cmathcal%7BL%7D_%7Batk%7D%3D-%5Cmathcal%7BL%7D_%7Bself%7D%3D-%5Cmathcal%7BL%7D%28%5Cmathcal%7BV%7D_U%2C%5Chat%7BC%7D_U%29) ，这里 ![[公式]](https://www.zhihu.com/equation?tex=%5Chat%7BC%7D_U) 代表原模型在测试集上的预测结果，也就是让攻击后模型的预测结果尽可能与原模型不同。

