from django.shortcuts import redirect, render,HttpResponse
from e_app.models import product,orders,OrderUpdate
from math import ceil
from e_app import keys
from django.conf import settings
from django.contrib import messages
MERCHANT_KEY=keys.MK
import json
from django.views.decorators.csrf import csrf_exempt
from payTm import Checksum

# Create your views here.
def home(request):
    return render(request,'index.html')


def purchase(request):
    current_user = request.user
    print(current_user)
    allProds = []
    catprods = product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,'purchase.html',params)


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/e_auth/login')
    if request.method=="post":
        items_json = request.POST.get('itemjson','')
        name = request.POST.get('name','')
        amount = request.POST.get('amt')
        email = request.POST.get('email','')
        address1 = request.POST.get("address1",'')
        address2 = request.POST.get("address2",'')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code =request.POST.get('zip_code','')
        phone = request.POST.get('phone','')


        order =orders(items_json=items_json,name=name,amount=amount,email=email,address1=address1,address2=address2,city=city,state=state,zip_code=zip_code,phone=phone)
        print(amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,update_desc="the order has been placed")
        update.save()
        thank = True
        #payment integration
        id = order.order_id
        oid = str(id)+"AISPACEX"
        param_dict ={

            'MID':keys.MID,
            'ORDER_id':oid,
            'TNX_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE' :'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/handlerequest/'

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})
    return render(request,'checkout.html')

def tracker(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/e_auth/login')
    if request.method=="POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        try:
            order = orders.objects.filter(order_id=orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time' : item.timestamp})
                    response = json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{no orders}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request,'tracker.html')       


    

@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    form =request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i] = form [i]
        if i =='CHECKSUMHASH':
            checksum = form[i]
    verify = checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('order successful') 
            a=response_dict['ORDERID']
            b=response_dict['TXNAMOUNT'] 
            rid=a.replace("AISPACEX","")

            print(rid)
            filter2=orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for post1 in filter2:
                post1.oid=a
                post1=amountpaid=b
                post1=paymentstatus="PAID"
                post1.save() 
            print("run agede function")
        else:
            print('order was not successful'+response_dict['RESPMSG'])
    return render(request,'paymentstatus.html',{'response':response_dict})                     

