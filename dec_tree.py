class node():
    def __init__(self,k_val,leaf,dict1,chi):
        self.k=k_val
        self.leaf=leaf
        self.left=None
        self.right=None
        self.dict1=dict1
        self.chi=chi


class DecTree():
    def __init__(self,depth=2):
        self.depth=depth
        self.pn=None

    def fit(self,x_train,y_train):
        k_val,dict1,chi=self.find_k(x_train,y_train,0)
        self.pn=node(k_val,False,dict1,chi)
        self.len=len(x_train[0])


        x_l=[]
        y_l=[]
        x_r=[]
        y_r=[]
        len1=len(x_train)
        for i in range(len1):
            if x_train[i][0]<=k_val:
                x_l.append(x_train[i])
                y_l.append(y_train[i])
            else:
                x_r.append(x_train[i])
                y_r.append(y_train[i])
        depth=self.depth
        self.pn.left=self.fit1(x_l,y_l,depth-1,1%self.len)
        self.pn.right=self.fit1(x_r,y_r,depth-1,1%self.len)


    def fit1(self,x_,y_,depth,pos):
        if depth>=1:
            k_val,dict1,chi=self.find_k(x_,y_,pos)
            if chi==0:
                node1=node(0,True,dict1,chi)
                return node1
            node1=node(k_val,False,dict1,chi)
            x_l=[]
            y_l=[]
            x_r=[]
            y_r=[]
            len1=len(x_)
            for i in range(len1):
                if x_[i][pos]<=k_val:
                    x_l.append(x_[i])
                    y_l.append(y_[i])
                else:
                    x_r.append(x_[i])
                    y_r.append(y_[i])
            node1.left=self.fit1(x_l,y_l,depth-1,(pos+1)%self.len)
            node1.right=self.fit1(x_r,y_r,depth-1,(pos+1)%self.len)
            return node1

        else:
            k_val,dict1,chi=self.find_k(x_,y_,pos%self.len)
            node1=node(k_val,True,dict1,chi)
            return node1


    def find_k(self,x,y,pos):
        k=int(x[0][pos])
        k_max=int(x[0][pos])+1
        chi=1
        dict1={}
        for i in x:
            if i[pos]>k_max:
                k_max=i[pos]
            if i[pos]<k:
                k=i[pos]
        j=k
        while j<k_max:
            chi_temp=self.chi_cal(x,y,pos,j)
            if chi_temp<chi:
                chi=chi_temp
                k=j
            j+=0.1
        for i in y:
            dict1[i]=0
        for i in y:
            dict1[i]+=1
        return k,dict1,chi


    def chi_cal(self,x,y,pos,k):
        x_l=[]
        y_l=[]
        x_r=[]
        y_r=[]
        len1=len(x)
        dict1={}
        dict2={}
        for i in range(len1):
            if x[i][pos]<k:
                x_l.append(x[i])
                y_l.append(y[i])
            else:
                x_r.append(x[i])
                y_r.append(y[i])
        
        for i in y_l:
            dict1[i]=0
        for i in y_l:
            dict1[i]+=1
        for i in y_r:
            dict2[i]=0
        for i in y_r:
            dict2[i]+=1
        sum1=0
        len1=len(y_l)
        for i in dict1:
            add=((dict1[i])/len1)**2
            sum1+=add
        sum1=1-sum1
        sum2=0
        len2=len(y_r)
        for i in dict2:
            add=((dict2[i])/len2)**2
            sum2+=add
        sum2=1-sum2
        return (sum1+sum2)/2

    def pred(self,x):
        node1=self.pn
        k_val,dict1,chi=self.pred1(node1,x,0)
        print(dict1)
        val=0
        pred=None
        tot=0
        for i in dict1:
            tot+=dict1[i]
            if dict1[i]>val:
                val=dict1[i]
                pred=i
        print("PREDICTION: ",pred,"\nDICT=",dict1)
        add=0
        for i in dict1:
            print("PERCENTAGE OF ",i," =",dict1[i]/tot)
            add+=(dict1[i]/tot)**2
        print("GINI VALUE=",1-add)

    def pred1(self,node,x,pos):
        if node.leaf==True:
            return node.k,node.dict1,node.chi

        k=node.k
        if x[pos]<=k:
            if node.left==None:
                return node.k,node.dict1,node.chi
            return self.pred1(node.left,x,(pos+1)%len(x))
        else:
            if node.right==None:
                return node.k,node.dict1,node.chi
            return self.pred1(node.right,x,(pos+1)%len(x))
            


x=[[5.1,3.5,1.4,0.2],
    [4.9,3.0,1.4,0.2],
    [4.7,3.2,1.3,0.2],
    [4.6,3.1,1.5,0.2],
    [7.0,3.2,4.7,1.4],
    [6.4,3.2,4.5,1.5],
    [6.9,3.1,4.9,1.5],
    [6.3,3.3,6.0,2.5],
    [5.8,2.7,5.1,1.9],
    [7.1,3.0,5.9,2.1]]

y=['ic','ic','ic','ic','iv','iv','iv','iv1','iv1','iv1']

tree=DecTree()
tree.fit(x,y)
tree.pred([6.3,3.3,6.0,2.5])












            
