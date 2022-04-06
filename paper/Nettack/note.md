# Nettack

**Adversarial Attacks on Neural Networks for Graph Data**

图结构的攻击目标：

1. nodes’ features：节点的特征
2. graph structure：图结构（图中的边）

攻击场景：

1. 整个图：Mettack
2. 单目标：Nettack 通过攻击某个节点（攻击者 acttacker）实现让另一个节点（目标 target）的误分类

攻击方法（由于是离散型数据，传统梯度攻击无效）

攻击效果：

​	样本偏差不被人所察觉，和图像的区别：图是离散型数据，大型图不适合人来察觉

​	攻击需要尽可能地保留图像中固有特征

## 攻击

### 攻击思想

攻击方式分两类：structure attacks、feature attacks

攻击节点分两类：Target、Attackers

​	influence attack（target不在攻击范围内）、direct attack

设定攻击范围Δ：

![image-20220330135915735](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330135915735.png)

攻击目标：

![image-20220330140609169](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330140609169.png)

对于参数𝜃的考虑，对于攻击后的图𝐺′，应当使用新训练的𝜃*，考虑到过渡性学习（transductive learning），使用静态参数：原始图像的训练参数。

### 主要问题

#### 保留图的结构结构性（固有特征）

图结构最突出的特征是它的度分布，使用幂律分布来描述：

![image-20220405095444164](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405095444164.png)

缩放参数𝛼的表达式：

![image-20220405095419930](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405095419930.png)

最大似然估计：

![image-20220405100642040](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405100642040.png)

#### 保留节点特征

反例：如果两个节点都没某个特征，经过攻击，两个节点都有了这个特征，就能增加节点的相似性
