from django.shortcuts import render, redirect   
from .models import *
# Create your views here.


def seller_register(request):
     if request.method == 'POST':
            Seller.objects.create(
            full_name = request.POST['full_seller_name'],
            email = request.POST['your_email'],
             pic = request.FILES['your_picture'],
             password = request.POST['your_password'],
             gst_no = request.POST['your_Gst_no']
        )
            return render(request,'seller_registration.html',{'smessage':'Sucessfully Created!!'})
    
     else:
        return render(request,'seller_registration.html')

def seller_login(request):
   try:
        if request.method=='GET':
            
            return render(request,'seller_login.html')
        else:
            u1=Seller.objects.get(email=request.POST['seller_email'])
            if request.POST['seller_password'] == u1.password:
                request.session['seller_email'] = request.POST['seller_email']
                return redirect('seller_index')
                
            else:
                return render(request,'seller_login.html',{'msg':"Invalid Password"})            
            
   except:
       return render(request,'seller_login.html',{'msg':"Email does not exist"})
    
    
def seller_index(request):
    try:
        request.session['seller_email']
        s1 = Seller.objects.get(email = request.session['seller_email'] )
        return render(request,'seller_index.html',{'sellerdata':s1})
        
    except:
        return redirect('seller_login')

def seller_profile(request):
    try:
        request.session['seller_email']
        s1 = Seller.objects.get(email = request.session['seller_email'] )
    
        return render(request,'seller_profile.html',{'sellerdata':s1})
        
    except:
        return redirect('seller_login')
    

def add_product(request):
    try:
        s1 = Seller.objects.get(email = request.session['seller_email'] )
        if request.method == 'GET':
             return render(request,'add_product.html',{'sellerdata':s1})
        else:
            Product.objects.create(
                name = request.POST['product_name'],
                des = request.POST['description'],
                price = request.POST['product_price'],
                pic = request.FILES['product_picture'],
                seller = s1   
            )
            return render(request,'add_product.html',{'sellerdata':s1,'msg':'Sucessfully Created..!!'}) 
    except:
        return redirect('seller_login')


def seller_logout(request):
    del request.session['seller_email'] 
    return redirect('seller_login') 