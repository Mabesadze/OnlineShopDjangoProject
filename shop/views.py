from django.shortcuts import render
from django.contrib import messages
from .forms import ContactForm
from django.views.generic import TemplateView, DetailView
from .models import Product,Category
from django.db.models import Q

# Create your views here.
      


def home(request):
    return render(request, 'shop/home.html')

def about(request):
    return render(request, 'shop/about.html')

def products(request):
    q = request.GET.get('q')
    selected_category = request.GET.getlist('category')

    products = Product.objects.all()
    
    # Search filter
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q)).distinct()
    
    # Category filter
    if selected_category:
        products = products.filter(category__in=selected_category).distinct()
    
    # Get all categories for filter
    categories = Category.objects.all().order_by('category_type')
    categories_by_type = {}
    for category in categories:
        category_type = category.category_type
        if category_type not in categories_by_type:
            categories_by_type[category_type] = []
        categories_by_type[category_type].append(category)

    context = {
        'products': products,
        'categories_by_type': categories_by_type,
        'selected_category': selected_category,
        'search_query': q,
    }
    return render(request, 'shop/products.html', context)
    
def contact(request):
    """Contact form view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data (send email, save to database, etc.)
            # For now, just show a success message
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            form = ContactForm()  # Reset form
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'shop/contact.html', context)

class ProductDetailView(DetailView):
    # Simple detail view that will render information for a single product
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
class aboutus(TemplateView):
    template_name = 'shop/about.html'