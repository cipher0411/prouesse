from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Category, Item, ItemImage, Cart, CartItem, Order
from .forms import NewItemForm, EditItemForm



def items(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False).order_by('-created_at')
    
    if category_id:
        items = items.filter(category_id=category_id)
    
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    if not items.exists():
        return render(request, 'item/items_not_found.html', {
            'query': query,
            'categories': categories,
            'category_id': int(category_id)
        })
    
    paginator = Paginator(items, 18)  # Adjusted to 18 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'item/items.html', {
        'items': page_obj,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[:3]
    
    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            for file in request.FILES.getlist('images'):
                ItemImage.objects.create(item=item, image=file)
            
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        
        if form.is_valid():
            form.save()
            
            for file in request.FILES.getlist('images'):
                ItemImage.objects.create(item=item, image=file)
            
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()
    
    return redirect('dashboard:index')

@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        subtotal = sum((item.item.sale_price if item.item.is_sale else item.item.price) * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        subtotal = 0

    if request.method == 'POST':
        for cart_item in cart_items:
            quantity = request.POST.get(f'quantity_{cart_item.id}', cart_item.quantity)
            if quantity:
                cart_item.quantity = int(quantity)
                cart_item.save()

        subtotal = sum((item.item.sale_price if item.item.is_sale else item.item.price) * item.quantity for item in cart_items)

    return render(request, 'item/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': subtotal,
    })

@require_POST
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

    return JsonResponse({'success': True, 'cart_quantity': cart_quantity})

@require_POST
@login_required
def remove_from_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
        cart_item.delete()
        
        cart_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

        return JsonResponse({'success': True, 'cart_quantity': cart_quantity})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart not found'})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found in cart'})

@require_POST
@login_required
def update_cart(request, item_id):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, item_id=item_id)
        quantity = int(request.POST.get('quantity', cart_item.quantity))

        if quantity <= 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()

        cart_quantity = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
        item_price = (cart_item.item.sale_price if cart_item.item.is_sale else cart_item.item.price) * cart_item.quantity
        subtotal = sum((item.item.sale_price if item.item.is_sale else item.item.price) * item.quantity for item in CartItem.objects.filter(cart=cart))
        total = subtotal

        return JsonResponse({
            'success': True,
            'cart_quantity': cart_quantity,
            'item_price': item_price,
            'subtotal': subtotal,
            'total': total,
        })
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart not found'})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found in cart'})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid quantity'})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'item/my_orders.html', context)










