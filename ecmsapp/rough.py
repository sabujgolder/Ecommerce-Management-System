def product_order(request,pk):
    product = Products.objects.get(id=pk)
    orders = product.order_set.all()
