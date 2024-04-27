from typing import Any
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from product.forms import ProductFilterForm,ProductForm
from product.models import ProductImage, ProductVariantPrice, Variant,Product,ProductVariant
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class CreateProductView(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = '/products/created' 

    def form_valid(self, form):
        
        product = form.save()

       
        variants_data = self.request.POST.getlist('variants')
        for variant_id in variants_data:
            variant = Variant.objects.get(id=variant_id)
            product.variants.add(variant)

        

        price_data = self.request.POST.getlist('prices')
        for price in price_data:
            price_obj = ProductVariantPrice(price=price, product=product)
            price_obj.save()

        
        image_data = self.request.FILES.getlist('images')
        for image in image_data:
            image_obj = ProductImage(product=product, file=image)
            image_obj.save()

        return super().form_valid(form)

class ShowProductList(generic.ListView):
    

    def get(self, request, **kwargs):
        
        products = Product.objects.all()
    
        # variant_prices_dict = {}

        # for product in products:
        #     variant_prices = ProductVariantPrice.objects.filter(product=product)
          
        #     variant_prices_dict.update({'varient_prices':variant_prices})

         
        # Pagination
        paginator = Paginator(products, 10)
        page = request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        if request.method == 'GET':
            form = ProductFilterForm(request.GET)
      
        context = {
            'products': products,
            # 'variant_prices_dict': variant_prices_dict,
            
        }
      
        return render(request, 'products/list.html', context=context)
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'  
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return self.get_queryset().get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object  

      
        variants = product.productvariant_set.all()
        images = product.productimage_set.all()

       
        data_summary = {
            'title': product.title,
            'description': product.description,
            'sku': product.sku,
            'variants': list(variant.variant_title for variant in variants),
            'images': list(image.file_path for image in images)
        }

        
        context['data_summary'] = data_summary
        return context    
def filter_products(request):
    
    form = ProductFilterForm(request.GET)

    
    queryset = Product.objects.all()  

    
   
    if form.is_valid():
      
        title = form.cleaned_data.get('title')
        variant = form.cleaned_data.get('variant')
        price_from = form.cleaned_data.get('price_from')
        price_to = form.cleaned_data.get('price_to')
        date = form.cleaned_data.get('date')

       
        if title:
            queryset = queryset.filter(title__icontains=title)
        if variant:
            queryset = queryset.filter(productvariant__icontains=variant)
        if price_from:
            queryset = queryset.filter(productvariantprice__gte=price_from)
        if price_to:
            queryset = queryset.filter(productvariantprice__lte=price_to)
        if date:
            queryset = queryset.filter(created_at=date)

        context = {
        'form': form,
        'products': queryset
    }


    return render(request, 'products/list.html', context=context)
from django.db.models import Count

def product_variants(request):
  
    product_variant_prices = ProductVariantPrice.objects.all()

    grouped_prices = {}
    for price in product_variant_prices:
        
        key = (price.product_variant_one, price.product_variant_two, price.product_variant_three)
        if key not in grouped_prices:
            grouped_prices[key] = []
        grouped_prices[key].append(price)

    context = {
        'grouped_prices': grouped_prices,
    }
    return render(request, 'products/create.html', context)

class ProductUpdateView(generic.UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_edit.html'
    success_url = reverse_lazy('list.product')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()  # Retrieve the product object

        
        form = ProductForm(instance=product)
        context['form'] = form

        return context