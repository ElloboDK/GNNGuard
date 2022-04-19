## **GNNGUARD: Defending Graph Neural Networks against Adversarial Attacks**

NeurIPS 2020

DOI:2006.08149

### 背景知识

[GCN原理]: https://www.163.com/dy/article/FP9HA24J0516EPQ9.html

隐藏层传递公式：

![image-20220330132805887](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330132805887.png)

只有一层隐藏层的GCN:

![image-20220330133202273](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330133202273.png)

loss（交叉熵）:

![image-20220330133405485](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330133405485.png)

GNN计算公式：

$$
f = (MSG,AGG,UPD)
$$
MSG:消息传递函数，计算两个节点的特征以及连接信息 ![image-20220419125030162](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419125030162.png)![image-20220419125039440](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419125039440.png)

AGG:聚合函数，将节点收到的所有消息聚合起来 ![image-20220419125059523](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419125059523.png)

UPD:更新函数，将节点特征和聚合信息传递到下一层![image-20220419125114107](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419125114107.png)

![image-20220225150752480](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220225150752480.png)

### 核心思想

GNNGUARD将一个现有的GNN模型作为输入。它通过修改GNN的**神经信息传递操作符**来减轻不利影响。特别是，它修改了**信息传递结构**，使修改后的模型对对抗性扰动具有鲁棒性，同时模型保持其表示学习能力

为此，GNNGUARD开发了两个关键组件，**用于估计每个节点的邻居重要性**，并通过一个有效的**记忆层粗化图**

- 前一个组件动态地调整节点的本地网络邻域的相关性，修剪可能的假边，并根据网络同源性理论为可疑的边分配较少的权重
- 后者通过保留GNN中前一层的部分记忆，稳定了图结构的演变![image-20220307125012629](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307125012629.png)

### **Neighbor Importance Estimation**

邻居节点的重要性估计

和GAT的区别：相似节点（即具有相似特征或相似结构作用的节点）比不相似的节点更有可能相互作用的关系（同质性）

计算方式：**余弦相似度**。在同亲图中，衡量节点特征之间的相似性；在异亲图中，衡量节点结构角色的相似性。

![image-20220307123221459](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307123221459.png)

对相似度进行正则化处理

![image-20220307125219357](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307125219357.png)

定义特征向量来描述边，虽然相似度相同，但是经过正则化处理会变得不同

![image-20220307133707534](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307133707534.png)

对边进行剪枝，设定阈值P0

![image-20220307134759440](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307134759440.png)

最终更新边的权重：

![image-20220307134919944](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307134919944.png)

###  **Layer-Wise Graph Memory**

邻居重要性估计和边缘修剪改变了相邻GNN层之间的图结构。这可能会破坏GNN训练的稳定性，特别是当相当数量的边缘在单层中被修剪（例如，由于权重的初始化）。为了允许对重要性权重的稳健估计和边缘修剪的平滑演变，我们使用了层级图记忆。这个单元应用于GNN的每一层，对上一层的修剪后的图结构保持部分记忆。

记忆公式：

![image-20220307141423614](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307141423614.png)

### 算法流程

![image-20220307141649370](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307141649370.png)

### 实验数据

Nettack-Di攻击：

![image-20220307144421963](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220307144421963.png)

Nettack-In攻击和Mettack攻击：

![image-20220419094216361](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419094216361.png)

Mettack攻击：

![image-20220419101515793](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419101515793.png)

**graphlet degree vector**

Graphlet是基础的由节点构成的基础子图单位，由两个节点开始

![preview](https://pic3.zhimg.com/v2-bb7fedb4f94cec1a876d7f017339e332_r.jpg)

由graphlet转换为节点的特征向量

![preview](https://pic1.zhimg.com/v2-0a04a3bb143b1c4de4029089c55f6eac_r.jpg)

构造了带有房屋形状的循环图，下图为例：

合成的图包含1,000个节点 (没有节点特征，但每个节点有一个73维的小图向量），3200条无向边，以及 6个节点标签（即不同的结构角色）

![image-20220419122038856](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419122038856.png)



![image-20220419122411919](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419122411919.png)



消融实验（测试各个组件之间的必要性）：

![image-20220419100909798](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419100909798.png)

原图上的准确率（现实中往往不知道图是否被攻击过）：

![image-20220419101244549](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220419101244549.png)



**想法**（同质性）：

1. 通过某种聚类的方法将节点分类，相似的节点会聚成一类。那么在一个类中边权重较高，类间的边权重较低

2. 类似Honeypot的思想，制造一个陷阱，将攻击数据剔除。

   如何制造陷阱？

   陷阱的制造是否会降低模型准确率

