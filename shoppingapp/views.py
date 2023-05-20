from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.mail import send_mail
import random
from django.conf import settings
from sellerapp.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def index(request):
    product_list = Product.objects.all()
    # print(request.session['email'])
    try:
        u1 = User.objects.get(email=request.session['email'])
        return render(request,'index.html' , {'userdata':u1,'all_products': product_list})
    except:
        return render(request,'index.html',{'all_products': product_list})

         

def contact(request):
    try:
        u1=User.objects.get(email=request.session['email'])
        return render(request,'contact.html',{'userdata':u1})
    except:
        return render(request,'contact.html')

def faqs(request):
    try:
        u1=User.objects.get(email=request.session['email'])
        return render(request,'faqs.html',{'userdata':u1})
    except:
        return render(request,'faqs.html')
    
        
def logout(request):
    del request.session['email']
    return redirect('index')

def about(request):
    return render(request,'about.html')

def help(request):
    return render(request,'help.html')

def icons(request):
    return render(request,'icons.html')

def payment(request):
    return render(request,'payment.html')

def privacy(request):
    return render(request,'privacy.html')

def product(request):
    return render(request,'product.html')

def product2(request):
    return render(request,'product2.html')

def single(request):
    return render(request,'single.html')

def single2(request):
    return render(request,'single2.html')

def terms(request):
    return render(request,'terms.html')

def typography(request):
    return render(request,'typography.html')

def checkout(request):
    return render(request,'checkout.html')


def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        if request.POST['password'] == request.POST['cpassword']:
            try:
                u1 = User.objects.get(email = request.POST['email'])
                return render(request,'register.html',{'msg':'Email Already Exists'})
            except:
                global  c_otp, data_list
                c_otp = random.randint(1000,9999)
                data_list = [
                     request.POST['fname'],
                    request.POST['lname'],
                    request.POST['email'],
                    request.POST['password'],
                    request.POST['username']
                ]
                s = 'Welcome To E-Commerce'
                m = f'Your OTP is {c_otp}'
                fm = settings.EMAIL_HOST_USER
                rl = [request.POST['email']]
                send_mail(s, m, fm, rl)
                return render(request,'otp.html')
        else:
            return render(request,'register.html',{'msg':'Both Passwords DO Not Match'})


        

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        # print(request.POST['email'])
        try:
            u1 = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == u1.password:
                request.session['email']=request.POST['email']
                return redirect('index')
            else:
                return render(request,'login.html',{'msg':'Invalid Password'})
                        
        except:
            return render(request,'login.html',{'msg':'Email Does Not Exist'})
            
            
         
        

def otp(request):
   if int( request.POST['u_otp']) == c_otp:
       User.objects.create(
           first_name = data_list[0],
           last_name = data_list[1],
           email = data_list[2],
           password = data_list[3]
    )
       return render(request,'register.html',{'msg':'Sucessfully Account Created '})
   
   else:
       return render(request,'otp.html',{'msg':'Invalid OTP'}) 
   
   
def add_to_cart(request,pid):
    try:
       u1=User.objects.get(email = request.session['email'])
       p1=Product.objects.get(id = pid)
       Cart.objects.create(
           buyer = u1,
           product = p1
       )
       return redirect('index') 
    except:
        return redirect('login')
    
    
def cart(request):
    try:
        u1=User.objects.get(email=request.session['email'])
        c_list = Cart.objects.filter(buyer=u1)
        global amount_rupee
        amount_rupee = 0
        for i in c_list:
            amount_rupee += i.product.price
        return render(request,'cart.html',{'userdata':u1,'cart_data':c_list,'total_product':len(c_list),'total_amount':amount_rupee})
    except:
        return redirect('login')   

def del_cart_row(request,cid):
    c_obj = Cart.objects.get(id = cid)
    c_obj.delete()
    return redirect('cart')


# --------------------------------------Razorpay Function------------------------------------------

def homepage(request):
    currency = 'INR'
    amount = amount_rupee*100  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'
 
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
 
    return render(request, 'pay.html', context=context)


# -----------------------------------------SECOND FUNCTION-----------------------------------------

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = amount_rupee*100  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                   
                    u1 = User.objects.get(email = request.session['email'])
                    c_l= Cart.objects.filter(buyer = u1)
                    for i in c_l:
                        i.delete()
 
                    # render success page on successful caputre of payment
                    return redirect('index')
                except:
 
                    # if there is an error while capturing payment.
                    return HttpResponse("FAILED!!")
            else:
 
                # if signature verification fails.
                return HttpResponse("FAILED!!")
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()