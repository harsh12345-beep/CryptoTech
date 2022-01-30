from email import message
from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from Shop.models import OrderItem, order, product,art
import random
from Shop import views
def addtocart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            product_check = product.objects.get(id=prod_id)
            if(product_check):
                if(art.objects.filter(user=request.user.id, product_id=prod_id)):
                    return JsonResponse({'status':"product already in cart"})
                else:
                    product_qty = int(request.POST.get('product_qty'))
                    if product_check.quantity >= product_qty:
                       art.objects.create(user=request.user,product_id=prod_id,product_qty=product_qty)
                       return JsonResponse({'status':"product added successfully"})
                       
                    else:
                        return JsonResponse({'status':"only "+str(product_check.quantity)+"quantity available"})
                        
                    
                
            else:
                return JsonResponse({'status':"No Such product found"})    
        else:
            return JsonResponse({'status':"Login to Continue"})    
    return redirect("/")

@login_required(login_url='login')
def viewcart(request):
    cart =art.objects.filter(user=request.user)
    context = {'cart':cart}
    return render(request,"Shop/inc/cart.html",context)


def update(request):
    if request.method == 'POST':
        prod_id = request.POST.get('product_id')
        if(art.objects.filter(user = request.user, product_id = prod_id)):
            prod_qty = request.POST.get('product_qty')
            car = art.objects.get(product_id=prod_id, user=request.user)
            car.product_qty = prod_qty
            car.save()
            return JsonResponse({'status':"Updated Successfully"})
    return redirect("/")        

def delete(request):
    if request.method =="POST":
        prod_id = request.POST.get('product_id')
        if(art.objects.filter(user = request.user, product_id = prod_id)):
            cartitem = art.objects.get(product_id = prod_id, user= request.user)
            cartitem.delete()
            return JsonResponse({'status':"Deleted Successfully"})
    return redirect("/")


@login_required(login_url='login')
def checkout(request):
    raw = art.objects.filter(user = request.user)
    for item in raw:
        if item.product_qty > item.product.quantity:
            art.objects.delete(id=item.id)
    cartitems = art.objects.filter(user = request.user)
    totalprice = 0
    for item in cartitems:
        totalprice = totalprice + item.product.selling_price * item.product_qty
        
    context ={'cartitems':cartitems,'totalprice':totalprice}        
    return render(request, "Shop/inc/checkout.html",context)

@login_required(login_url='login')
def placeorder(request):
    if request.method == 'POST':
        neworder = order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.Address = request.POST.get('address')
        neworder.city = request.POST.get('City')
        neworder.State = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pin = request.POST.get('pin')
        neworder.adhar = request.POST.get('addhar')
        cart = art.objects.filter(user=request.user)
        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + item.product.selling_price * item.product_qty
        
        neworder.total_price = cart_total_price
        track_no = 'crypto' +str(random.randint(1111111,9999999))
        while order.objects.filter(tracking_no=track_no) is None:
            track_no = 'crypto' +str(random.randint(1111111,9999999))
        neworder.tracking_no = track_no
        neworder.save()
        
        
        neworderitems = art.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order = neworder,
                Product = item.product,
                price = item.product.selling_price,
                quantity = item.product_qty
            )
            orderproduct = product.objects.filter(id=item.product_id).first()
            orderproduct.quantity =  orderproduct.quantity - item.product_qty
            orderproduct.save()
        art.objects.filter(user = request.user).delete()
        messages.success(request, "Your Order has been Placed Successfuly")
    

    return redirect("Index")
@login_required(login_url='login')    
def myorders(request):
    orders = order.objects.filter(user=request.user)
    context={'orders':orders}
    return render(request,"Shop/inc/order.html", context)
@login_required(login_url='login')
def orderview(request, t_no):
    Order =order.objects.filter(tracking_no = t_no).filter(user=request.user).first()
    Orderitem = OrderItem.objects.filter(order = Order)
    context={'order':Order,'Orderitem':Orderitem}
    return render(request, "Shop/inc/orderview.html",context)
@login_required(login_url='login')    
def wallet(request):
    return render(request,'Shop/wallet/index.html')

def me(request):
    return render(request,'Shop/wallet/me.html')

