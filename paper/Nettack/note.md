# Nettack

**Adversarial Attacks on Neural Networks for Graph Data**

KDD 2018 图神经网络对抗攻击开山之作

整个图：Mettack

单目标攻击：Nettack 通过攻击某个节点（攻击者 acttacker）实现让另一个节点（目标 target）的误分类

## 攻击

### 攻击理论

攻击目标分两类：

- 图结构攻击 structure attacks
- 特征攻击 feature attacks

攻击节点分两类：

- Target 目标节点：让模型错误分类的结点
- Attackers 攻击者结点：攻击者可以操作的结点

攻击方式：

- direct attack 直接攻击：攻击者可以直接操作目标结点，目标结点 == 攻击者结点
- influence attack 推理攻击：攻击者只能操作除目标结点以外的结点，目标结点 ∉ 攻击者结点

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201223085735256.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80OTM5MzQyNw==,size_16,color_FFFFFF,t_70)

设定攻击范围Δ：

![image-20220330135915735](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330135915735.png)

攻击目标：

![image-20220330140609169](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220330140609169.png)

对于参数𝜃的考虑，对于攻击后的图𝐺′，应当使用新训练的𝜃*，考虑到过渡性学习（transductive learning），使用静态参数：原始图像的训练参数。

### 场景

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201223085440564.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80OTM5MzQyNw==,size_16,color_FFFFFF,t_70)

- 投毒攻击（ poisoning attack）
  - 发生在模型被训练前，攻击者可以在训练数据中投毒，导致训练的模型出现故障
- 逃逸攻击（ evasion attack）
  - 发生在模型被训练以后或者测试阶段，模型已经固定了，攻击者无法对模型的参数或者结构产生影响

### 主要问题

#### 如何有效的攻击

图像：连续特征，可以采用基于梯度构造干扰

图：离散型数据，没有梯度



第一，扰动是不被注意到的

第二，确保攻击者不能修改整个图，允许的扰动数目是有限制的



#### 保留图的结构结构性（固有特征）

图结构最突出的特征是它的度分布，使用幂律分布来描述：

![image-20220405095444164](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405095444164.png)

缩放参数𝛼的表达式：

![image-20220405095419930](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405095419930.png)

最大似然估计：

![image-20220405100642040](C:\Users\Jin Xin Lei\AppData\Roaming\Typora\typora-user-images\image-20220405100642040.png)

#### 保留节点特征

特征的共现关系

反例：如果两个节点都没某个特征，经过攻击，两个节点都有了这个特征，就能增加节点的相似性。

在特征共现图上随机游走，如果有相当大的概率到达一个新加入的特征，那么就认为这个扰动的加入是不被注意的



### 攻击

代理模型 Surrogate model

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020122308594536.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80OTM5MzQyNw==,size_16,color_FFFFFF,t_70)

为了能够量化扰动的效果，同时简便计算，所以提出了一个替代模型

代理模型使用两层的GCN，把激活函数做了线性的替换

