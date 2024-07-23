# tasks.py
from celery import shared_task
from .models import Product, Seller
import logging
from .chat import chatBot
from django.db.models import Q

@shared_task
def generate_product_summaries():
    products = Product.objects.filter(Q(description__isnull=True) | Q(description__iexact='nan'))
    if not products.exists():
        logging.info("No products to generate summaries for")
        return
    print(products)
    batch_size = 10  # Adjust batch size as needed
    batches = [products[i:i + batch_size] for i in range(0, len(products), batch_size)]

    for batch in batches:
        prompt = "Generate summaries for these products by accounting seller's specifications and niche and general product specification. Generate summary sequentially for each product. Follow output format: ['summary for product 1', 'summary for product 2']\n"
        for product in batch:
            prompt += f"Product ID: {product.id}\n"
            prompt += f"Seller Specification: {product.seller.specialization}\n"
            prompt += f"Seller Niche: {product.seller.niche}\n"
            prompt += f"Product Name: {product.name}\n\n"

        print(prompt)
        prompt = "hello how you doing?"
        chatbot = chatBot(prompt)
        summaries = chatbot.chat_completion()
        print(summaries)
        
        for product, summary in zip(batch, summaries):
            product.description = summary.strip()
            product.save()