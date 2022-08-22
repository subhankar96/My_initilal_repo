#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# RESET OF BOOKS AVAILABLE(INITIALISATION)

# In[2]:


# df_book=pd.read_csv("Book Data Clean 2.csv")
# df_book.to_csv('BOOKS AVAILABLE.csv',index=False)


# In[3]:


df_book=pd.read_csv('BOOKS AVAILABLE.csv')
df_book


# In[4]:


pd.read_csv('USER_LIST.csv')


# FINDING A BOOK IN FRAME
# --
# 

# In[5]:


def find_book():
    import regex as rg
    df_user=pd.read_csv('USER_LIST.csv')
    df_book==pd.read_csv('BOOKS AVAILABLE.csv')
    
    t=user_check()

    while t==True:
        ch=input('Do You Wish To Continue(Y/N): ')
        if ch.lower()=='y':
            print('''HOW DO YOU WANT TO SEARCH:
                         1. BY NAME OF BOOK
                         2. BY NAME OF AUTHOR
                                     ''')
            x=input('Select option(1,2): ')

            if x=='1':
                n=input('Enter name of the book: ')
                if n.lower() in list(df_book['Name of the book']):
                    print('DETAILS OF BOOK \n')
                    print(df_book[df_book['Name of Book']==n])
            elif x=='2':
                f=input('ENTER AUTHOR FIRST NAME(include middle name with a space, if any): ')
                l=input('ENTER THE LAST NAME: ')
                fn=f+' '+l
                if fn in list(df_book['Author']):
                    dfmin=df_book[df_book['Author']==fn]
                    print(dfmin['Name of Book'])
            else:
                print('Sorry! Invalid Choice')

                continue
        elif ch.lower()=='n':
            break
        else:
            print('Invalid choice,  please choose "y" or "n" ')

        
        


# USER ID & PASSWORD CHECK FUNCT (FOR CUSTOMER)
# --

# In[6]:


def user_check():
    df_user=pd.read_csv('USER_LIST.csv')
    
    un=input('Enter User Name : ')
    up=input('Enter the password: ')
    
    x=df_user[(df_user.USERNAME==un) & (df_user.PASSWORD==up)]
    if x.empty==True:
        print('\n \n Invalid Username or password')
        return (False)
    else:
        return (True)
        
    


# ADMIN USER ID CHECK
# --

# In[7]:


def user_check_admin():    
    un=input('Enter Admin ID: ')
    up=input('Enter the password: ')
    
    if un=='LIBRARY' and up=='@lib@':
        return (True)
        
    else:
        print('\n \n Invalid Username or password')
        return (False)


# ISSUE OF BOOK
# --

# In[8]:


# RESET STATEMENT for ISSUE LOG 
# df_issue=pd.DataFrame(columns=['book_id','issuer','date of issue','date of return'])
# df_issue.to_csv('Issue Log.csv',index=False)


# In[9]:



def book_issue():
    x=user_check_admin()
    import datetime
    df_book=pd.read_csv('BOOKS AVAILABLE.csv')
    df_issue=pd.read_csv('Issue Log.csv')
    
    if x==True:
        idb= int(input('Enter ID of book to be issued: '))
        issuer= input('Name of issuer: ')
        if issuer in list(df_user['USERNAME']):
            if idb in list(df_book['ID']):
                unitsavail=df_book.loc[idb-1,'Units']-df_book.loc[idb-1,'Units Issued']
                x=df_book[(df_book['ID']==idb) & (unitsavail>0)]
                if x.empty==False:
                    l=df_issue['book_id'].size
                    df_issue.loc[l]=[idb,issuer,datetime.date.today(),None]
                    df_issue.to_csv('Issue Log.csv',index=False)
                    
                    a=df_book.loc[idb-1,'Units Issued']
                    df_book.loc[idb-1,'Units Issued']=a+1
                    df_book.to_csv('BOOKS AVAILABLE.csv',index=False)
                    print("BOOK ISSUED SUCCESSFULLY")
            else:
                print('id invalid. Try Again!')
        else:
            print('User invalid. Try Again!')
    df_issue.to_csv('Issue Log.csv',index=False)
    
        
            
            
            
        
        
        
        
    


# RETURN A BOOK
# --

# In[10]:


#RESET STATEMENT FOR LIBRARY CREDIT LOG.csv

# df_pay=pd.DataFrame(columns=['USER','AMOUNT','DATE'])
# df_pay.to_csv('Library Credit Log.csv',index=False)


# In[11]:


def book_return():
    import datetime
    
    df_book=pd.read_csv('BOOKS AVAILABLE.csv')
    df_issue=pd.read_csv('Issue Log.csv')
    df_pay=pd.read_csv('Library Credit Log.csv')
    
    t=user_check_admin()
    df_pay=pd.read_csv('Library Credit Log.csv')
    if t==True:
        ret=int(input('Enter Book ID to be returned: '))
        if ret in list(df_issue['book_id']):
            un=input('Enter User Name: ')
            df_book.loc[ret-1,'Units Issued']=df_book.loc[ret-1,'Units Issued']-1
            df_book.to_csv('BOOKS AVAILABLE.csv',index=False)
            
            y=df_issue[(df_issue['book_id']==ret) & (df_issue['issuer']==un)]
            if y.empty==False:
                print('Sucess')
                ind=int(y.index.values)
                df_issue.loc[ind,'date of return']=datetime.date.today()
                #issue_date_str=df_issue.loc[ind,'date of issue']
                idate=df_issue.loc[ind,'date of issue']
                issue_date=datetime.datetime.strptime(idate,'%Y-%m-%d')
                return_date=datetime.date.today()
                df_issue.to_csv('Issue Log.csv',index=False)
            
            
                #diff=(return_date.loc[0])-(issue_date.loc[0])
                diff=return_date-issue_date.date()
                amt=(diff.days) * 20 #charge per day=20
                
            
                print('Amount to be paid: ',amt)
                
                if amt==0:
                    df_issue.drop(ind, inplace=True)
                    df_issue.to_csv('Issue Log.csv',index=False)
            
            
                while amt!=0:
                    check=input('WAS THE AMOUNT PAID(Y/N): ')
                    if check.lower()=='y':
                        df_issue.drop(ind, inplace=True)
                        print('AMOUNT PAID')

                        break
                    elif check.lower()=='n':
                        df_pay.loc[df_pay.size]=[un,amt,datetime.date.today()]
                        print('Amount not paid')
                        print('Added to Credit DF')
                        df_pay.to_csv('Library Credit Log.csv',index=False)
                    
                        break
                    else:
                        print("only 'y' or 'n' ")
                        continue
            else:
                print('Book Not Issued!')
        else:
            print('NOT ISSUED!')
            
            
                    
                
    
            
            
    
                
            
            
            
        


# ADD A BOOK TO LIBRARY
# --

# In[92]:


def book_add():
    df_book=pd.read_csv('BOOKS AVAILABLE.csv')
    
    check=user_check_admin()
    
    if check==True:
        idb=df_book['ID'].size+1
        name_of_Book=input('Enter the name of the book: ')
        author_name=input('Author Name: ')
        imprint=input('Imprint: ')
        pub_grp=input('Publisher Group')
        binding=input('Binding(hardback/soft back): ')
        dateofr=input('date of release in format:- dd Mon yyyy: ')
        genre=input('Genre: (in format: rating type)(Ex: F2.1  Crime, Thriller & Adventure): ')
        unit=int(input('Enter number of units available: '))
        df_book.loc[idb-1]=[idb,name_of_Book.title(),author_name.title(),imprint.title(),pub_grp.title(),binding.title(),dateofp,genre,unit,0]
        df_book.to_csv('BOOKS AVAILABLE.csv',index=False)
        


# In[93]:


df=pd.read_csv('BOOKS AVAILABLE.csv')
df


# INITIALISATION(RESET FOR USERS)

# In[ ]:


#dic={'USERNAME':['LIBRARY'],'PASSWORD':['@lib@#']}
#df_user=pd.DataFrame(dic)
#df_user.to_csv('USER_LIST.csv',index=False)


# In[ ]:


df_user=pd.read_csv('USER_LIST.csv')
df_user


# USER ADD
# --

# In[40]:


def add_user():
    df_user=pd.read_csv('USER_LIST.csv')
    
    
    while True:
        usern=input('Enter the new user name: ')
        if usern not in list(df_user['USERNAME']):
            userp=input('New password: ')


            if userp=='':
                print('password cannot be empty')
                break

            else:
                x=df_user['USERNAME'].size
                df_user.loc[x]=[usern.lower(),userp]
                df_user.to_csv('USER_LIST.csv',index=False)
                break
        else:
            print(f'User with same name exists \n \n please try using {usern}1 or similiar')
            continue
            


# USER DELETION
# --

# In[41]:


def delete_user():
    y=user_check_admin()
    if y==True:
        df_user=pd.read_csv('USER_LIST.csv')

        un=input('Enter Name to be deleted: ')
        up=input('Enter the password: ')

        x=df_user[(df_user.USERNAME==un) & (df_user.PASSWORD==up)]
        if x.empty==True:
            print('\n \n Invalid Entry')
        else:
            df_user.drop(x.index,inplace=True)
            df_user.to_csv('USER_LIST.csv',index=False)
            print('USER DELETED SUCCESSFULLY')


# CONTINUOUS USER ADDITION
# --
#     

# In[24]:


def cont_useradd():
    while True:
        s=input('Do u want to add user(y/n): ')
        if s=='n':
            break
        elif s=='y':
            add_user()
        else:
            print('Incorrect input')
            continue


# REQUEST FOR BOOK
# --

# In[88]:


#INITIALISATION
# df_request=pd.DataFrame(columns=['Book','Author','Requested By'])
# df_request.to_csv('Book Requests.csv',index=False)


# In[89]:


def book_request():
    df_user=pd.read_csv('USER_LIST.csv')
    df_request=pd.read_csv('Book Requests.csv')
    
    un=input('Enter User Name : ')
    up=input('Enter the password: ')
    
    x=df_user[(df_user.USERNAME==un) & (df_user.PASSWORD==up)]
    if x.empty==True:
        print('\n \n Invalid Username or password')
    else:
        stb=input('Enter Name of the book: ')
        sta=input('Name of the author: ')
        l=df_request['Book'].size
        print(l)
        df_request.loc[l]=[stb,sta,un]
        df_request.to_csv('Book Requests.csv',index=False)
        
            
        
        


# GRIEVANCE OR COMMENTS
# --

# In[94]:


def lib_comments():
    df_user=pd.read_csv('USER_LIST.csv')
    
    un=input('Enter User Name : ')
    up=input('Enter the password: ')
    
    x=df_user[(df_user.USERNAME==un) & (df_user.PASSWORD==up)]
    if x.empty==True:
        print('\n \n Invalid Username or password')
    else:
        cont=input('Enter Your Comment: ')
        with open('COMMENTS BY USERS.txt','a') as fh:
            content=f"{cont}  \nGiven by by:- {un} \n \n \n"
            fh.write(content)
        
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# IMPLEMENTATION
# --

# In[97]:


def LIBRARY2022():
    print('WELCOME TO THE LIBRARY')
    print('\n\n')
    print('''WHAT DO YOU WANT TO DO?

                FOR MEMBERS:-
                1. SEARCH FOR A BOOK            
                2. REQUEST A BOOK TO BE ADDED    
                3. GRIEVANCE/COMMENTS FOR ADMIN

                FOR NEW MEMBER:-
                4. BECOME A MEMBER




                FOR LIBRARIAN:-
                5. ISSUE A BOOK TO A USER
                6. RETURN A BOOK FROM A USER
                7. ADD A BOOK TO LIBRARY
                8. REMOVE A BOOK FROM LIBRARY

                9. SEE THE ISSUE LOG
                10. SEE THE CREDIT LOG

                11. DELETE A USER
                12. VIEW ALL USERS
                ''')




    while True:
        response=int(input('Enter your response(1-12): '))
        if response in np.arange(1,13):
            break
        else:
            print('Invalid Choice')
            continue

    if choice==1:
        find_book()
    elif choice==2:
        book_request()
    elif choice==3:
        lib_comments()
    elif choice==4:
        add_user()
    elif choice==5:
        book_issue()
    elif choice==6:
        book_return()
    elif choice==7:
        book_add()
    elif choice==8:
        pass
    elif choice==9:
        z=user_check_admin()
        if z==True:
            df=pd.read_csv('Issue Log.csv')
            print(df)
    elif choice==10:
        z=user_check_admin()
        if z==True:
            df=pd.read_csv('Library Credit Log.csv')
            print(df)
    elif choice==11:
        delete_user()
    elif choice==12:
        z=user_check_admin()
        if z==True:
            df=pd.read_csv('USER_LIST.csv')
            print(df)
    

    
    
    
        


# In[ ]:





# In[ ]:





# In[ ]:




