# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Product, Seller

@shared_task
def generate_product_summaries():
    products = Product.objects.filter(description__isnull=True)
    if not products.exists():
        return

    batch_size = 10  # Adjust batch size as needed
    batches = [products[i:i + batch_size] for i in range(0, len(products), batch_size)]

    for batch in batches:
        prompt = ""
        for product in batch:
            prompt += f"Seller Specification: {product.seller.specialization}\n"
            prompt += f"Seller Niche: {product.seller.niche}\n"
            prompt += f"Product Name: {product.name}\n\n"

        #implement grok calling application here

        summaries = ["summary1", "summary2", "summary3"]

        for product, summary in zip(batch, summaries):
            product.description = summary.strip()
            product.save()

        # notify_users.delay([product.seller.email for product in batch])

# @shared_task
# def notify_users(emails):
#     for email in emails:
#         send_mail(
#             'Product Descriptions Generated',
#             'Summaries for your products have been generated.',
#             'from@example.com',
#             [email],
#             fail_silently=False,
#         )
