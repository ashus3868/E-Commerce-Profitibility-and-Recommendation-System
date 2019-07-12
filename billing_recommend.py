import time as tm,tkinter as tk,pandas as pd,matplotlib.pyplot as plt
from pandas import np
import os
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder    #object for apriori
from PIL import Image as IMG, ImageDraw     #for text to image

filename='database.csv'
columns=['Date','Time','Name','Mobile Number','Product','Total Amount']
root1=tk.Tk()
root=tk.Frame(root1)
root.pack()
root1.title('Retail billing and Recommend')
root1.geometry('1024x720')

row=9
num=1   #serial number
Product,Price='',[]
ItemsPurchased=[]
totalAmount=[]
global dataDict
def time():     #function to display date and time
    global TM,DT,q
    DT=""
    TM=""
    time1=q=tm.ctime(tm.time()).split(sep=' ')[-2]
    dateV=list(tm.localtime()[:3])
    q=q[:len(q)-3]
    for i in dateV:
        DT+=str(i)
        DT+='/'
    DT=DT[:len(DT)-1]
    date=tk.Label(root,bg='green',text='Date:  '+DT+'\t\tTime:  '+str(q),bd=3)
    date.grid(column=200,row=4)

from tkinter import *
import re
class AutocompleteEntry(Entry):
    def __init__(self, lista, *args, **kwargs):
        
        Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True
                    
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
                    
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

def readValues():
    global amo
    global pro
    global pri
    global qua

    pro=productE.get()
    pri=priceE.get()
    qua=quantityE.get()
    amo=float(pri)*float(qua)
    totalAmount.append(amo)
    ItemsPurchased.append(pro)  #add products to create a single bill
    
def addItem():      #add extra item to the bill
    global num
    global row
    global amountE
    global quantityE
    global priceE
    global productE,Product
    num+=1
    row+=1
    readValues()
    if os.path.isfile('price_list.csv'):
        priceF=pd.read_csv('price_list.csv')
        if str(productE.get()) not in list(priceF['Product']):
            priceF=priceF.append({'Product':str(productE.get()),'Price':str(priceE.get())},ignore_index=True)
    else:
        priceF=pd.DataFrame([[productE.get(),priceE.get()]],columns=['Product','Price'])
    priceF.to_csv('price_list.csv',index=False)
    Product+=str(productE.get())+','
    Price.append(priceE.get())
    productE=tk.Label(root,bg='green',text=str(pro),relief='flat',width=50)
    productE.grid(column=40,row=row)
    priceE=tk.Label(root,bg='green',text=str(pri),relief='flat')
    priceE.grid(column=80,row=row)
    quantityE=tk.Label(root,bg='green',text=str(qua),relief='flat')
    quantityE.grid(column=120,row=row)
    productE.destroy()
    priceE.destroy()
    quantityE.destroy()

    SNo=tk.Label(root,bg='green',text=str(num))
    SNo.grid(column=5,row=row)
    productE=AutocompleteEntry(listP,root)
    productE.grid(column=40,row=row)
    priceE=tk.Entry(root,relief='flat')
    priceE.grid(column=80,row=row)
    quantityE=tk.Entry(root,relief='flat')
    quantityE.grid(column=120,row=row)
    amountE=tk.Label(root,bg='green',text=str(amo),relief='flat')
    amountE.grid(column=200,row=row-1)
    Total=tk.Label(root,bg='green',text="Total Amount:"+str(sum(totalAmount)),fg='Red')
    Total.grid(column=120,row=row+1)
    time()
def print_bill():
    p=dataset[4].split(',')[:-1]
    referP=pd.read_csv('price_list.csv')
    if os.path.isfile('print.txt'):
        os.remove('print.txt')
    with open('print.txt','a') as file:
        file.write('\t\tInnovate Yourself\t\t\n')
        file.write('\t\t-----------------------\t\t\n')
        file.write(f'{DT}\t\t\t{q}\n')
        file.write('Product name\t|Price\n')
    for i in p:
        tup=tuple(referP.iloc[list(referP['Product']).index(i),:])
        with open('print.txt','a') as file:
            file.write(f'{tup[0]}\t\t\t{tup[1]}\n')
    with open('print.txt','a') as file:
        file.write(f'Payable Amount:\t{sum(totalAmount)}\n')
    os.startfile("print.txt", "print")  #print bill using printer
    
def Submit():
    dataDict={}
    global dataset
    dataset=[DT,q,nameE.get(),NumberE.get(),Product,sum(totalAmount)]
    for i in columns:
        for j in dataset:
            if columns.index(i)==dataset.index(j):
                dataDict.update({i:str(j)})
    #print(dataDict)
    if os.path.isfile('database.csv'):
        fileD=pd.read_csv('database.csv')
        fileD=fileD.append(dataDict,ignore_index=True)
    else:
        fileD=pd.DataFrame(dataDict,columns=columns,index=[0])
        #fileD.to_csv(filename,index=False)
    #print(fileD)
    fileD.to_csv(filename,index=False)
    #print(dataset)
    top=tk.Toplevel()
    lab=tk.Label(top,text='Submitted Successfully!!!',font=('Arial',15),fg='green')
    lab.pack()
    top.mainloop()
def recommend():
    df=pd.read_csv('database.csv')
    df1=df['Product'].apply(lambda x:x.split(','))
    te = TransactionEncoder()
    te_ary = te.fit(df1).transform(df1)
    df1 = pd.DataFrame(te_ary, columns=te.columns_).drop('',axis=1)
##    print(te.columns_)    
##    print(df1)
    frequent_itemsets = apriori(df1, min_support=0.03, use_colnames=True)
    #sup=sum(frequent_itemsets['support'])*2/len(frequent_itemsets['support'])
    #frequent_itemsets = apriori(df1, min_support=sup, use_colnames=True)
    #print(frequent_itemsets)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    items=frequent_itemsets[ (frequent_itemsets['length'] >= 2) &
                   (frequent_itemsets['support'] >= 0.04) ]
    recP=items['itemsets']
##    win=tk.Tk()
##    win.title('Recommendations for you...')
##    win.geometry('500x500')
##    label=tk.Label(win,text='Recommended products for you...')
##    label.place(x=10,y=10)
##    listbox=tk.Listbox(win,relief='flat',width=50)
##    listbox.place(x=15,y=30)
##    for i in recP:
##        listbox.insert(tk.END,tuple(i))
##    
##    win.mainloop()
    GP=pd.read_csv('price_list.csv')
    class SampleApp(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            lb = tk.Listbox(self)
            for i in recP:
                lb.insert(tk.END,tuple(i))
            lb.bind("<Double-Button-1>", self.OnDouble)
            lb.pack(side="top", fill="both", expand=True)

        def OnDouble(self, event):
            widget = event.widget
            selection=widget.curselection()
            value = widget.get(selection[0]) 
            
            try:
            
                Rec_pric=(GP.iloc[[list(GP['Product']).index(value[0])],:].values[0][1]+GP.iloc[[list(GP['Product']).index(value[1])],:].values[0][1])-(0.1*(GP.iloc[[list(GP['Product']).index(value[0])],:].values[0][1]+GP.iloc[[list(GP['Product']).index(value[1])],:].values[0][1]))
                img = IMG.new('RGB', (60, 30), color = (0,0,0))
                d = ImageDraw.Draw(img)
                d.text((10,10), "Rs."+str(Rec_pric), fill=(255,255,255))
                img.save('images/recommend_price.png')
                list_file=os.scandir('images')
                item_list=[i.name for i in iter(list_file)]
                first,second='',''
                
                for i in item_list:
                    if str(value[0])==i[:len(str(value[0]))]:
                        first=i
                    if str(value[1])==i[:len(str(value[1]))]:
                        second=i
                #plt.title('Rs.'+str(Rec_pric))
                for j in [first,second,'recommend_price.png']:
                    plt.subplot(1,3,[first,second,'recommend_price.png'].index(j)+1)
                    img=plt.imread('images/'+j)
                    plt.imshow(img)
                    plt.xlabel(j[:-4])
                    plt.xticks([])
                    plt.yticks([])
                    plt.autoscale()
                plt.show()
                #label=tk.Label(roo,text=str(value[0])+'+'+str(value[1])+' = Rs.'+str(int(Rec_pric)),font=('Tahoma',30),fg='white',bg='black')
            
            except:
                  roo=tk.Tk()
                  roo.title('Offer for you...')
                  label=tk.Label(roo,text='Something went wrong!!!',font=('Tahoma',30),fg='white',bg='black')
                  label.pack()
                  roo.mainloop()
            

    if __name__ == "__main__":
        app = SampleApp()
        app.title('Recommended products')
        app.mainloop()



lista=list(set(pd.read_csv('database.csv')['Name']))
listP=list(set(pd.read_csv('price_list.csv')['Product']))
listN=list(set([str(i) for i in pd.read_csv('database.csv')['Mobile Number']]))
#title
heading=tk.Label(root,text='Products billing',font=('Tahoma',30),fg='Yellow',bg='Black',bd=3)
heading.grid(column=50,row=2)

#customer Details
nameL=tk.Label(root,bg='green',text='Name')
nameL.grid(column=2,row=4)
nameE=AutocompleteEntry(lista,root)
nameE.grid(column=40,row=4)
NumberL=tk.Label(root,bg='green',text='Mobile Number')
NumberL.grid(column=60,row=4)
NumberE=AutocompleteEntry(listN,root)
NumberE.grid(column=80,row=4)

#today's date and time
time()

#labeling for the product purchase details
SNO=tk.Label(root,bg='green',text='SNo.')
SNO.grid(column=40,row=7)
product=tk.Label(root,bg='green',text='Product')
product.grid(column=40,row=7)
price=tk.Label(root,bg='green',text='Price')
price.grid(column=80,row=7)
quantity=tk.Label(root,bg='green',text='Quantity')
quantity.grid(column=120,row=7)
amount=tk.Label(root,bg='green',text='Amount')
amount.grid(column=200,row=7)

#product that is purchased by customer to be entered by the 
SNo=tk.Label(root,bg='green',text=str(num))
SNo.grid(column=5,row=9)
productE=AutocompleteEntry(listP,root)
productE.grid(column=40,row=9)
priceE=tk.Entry(root)
priceE.grid(column=80,row=9)
quantityE=tk.Entry(root)
quantityE.grid(column=120,row=9)
amountE=tk.Label(root,bg='green',relief='flat')
amountE.grid(column=200,row=9)

addButton=tk.Button(root,text='Add+',font=('Tahoma'),width=20,command=addItem,bg='gray',fg='Black',bd=5)
addButton.grid(column=200,row=30)

SubmitButton=tk.Button(root,text='Submit',font=('Tahoma'),width=20,command=Submit,bg='gray',fg='Black',bd=5)
SubmitButton.grid(column=200,row=32)

PrintButton=tk.Button(root,text='Print Bill',font=('Tahoma'),width=20,command=print_bill,bg='gray',fg='Black',bd=5)
PrintButton.grid(column=200,row=34)

SubmitButton=tk.Button(root,text='Recommend',font=('Tahoma'),width=20,command=recommend,bg='gray',fg='Black',bd=5)
SubmitButton.grid(column=200,row=36)

##Total=tk.Label(root,bg='green',text="Total Amount:"+str(sum(totalAmount)))
##Total.grid(column=120,row=52)
root.configure(background='green')
root1.configure(background='green')
root1.mainloop()
