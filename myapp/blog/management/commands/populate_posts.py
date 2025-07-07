from blog.models import Post,Category
from django.core.management.base import BaseCommand 
from typing import Any
import random



class Command(BaseCommand):
    help =" This command inserts post data"
    def handle(self, *args, **options):
        # Delete Exiting Data

        Post.objects.all().delete()
        title = [
        'The Future of AI',
        'Building Scalable Web Applications',
        'Introduction to Machine Learning',
        'Understanding Django Framework',
        'Data Structures and Algorithms in Python',
        'Cybersecurity Best Practices',
        'Cloud Computing Essentials',
        'Blockchain Technology Explained',
        'The Rise of Quantum Computing',
        'Deep Learning for Beginners',
        'Natural Language Processing with Python',
        'The Impact of AI on Society',
        'Internet of Things (IoT) Revolution',
        'Full-Stack Web Development Guide',
        'Mastering Python for Machine Learning',
        ]


        content = [
            "Artificial Intelligence is rapidly evolving, shaping industries like healthcare, finance, and transportation. The future of AI includes advancements in deep learning, autonomous systems, and ethical AI frameworks.",
            "Scalability is crucial for modern web applications. This includes load balancing, database optimization, caching mechanisms, and cloud deployment strategies to handle increasing user demands.",
            "Machine Learning enables computers to learn patterns from data without explicit programming. It includes supervised, unsupervised, and reinforcement learning techniques used in various applications.",
            "Django is a high-level Python web framework that enables rapid development and clean design. It follows the MVT (Model-View-Template) pattern and comes with built-in security features.",
            "Mastering data structures like arrays, linked lists, stacks, and queues, along with algorithms like sorting and searching, is essential for efficient coding and problem-solving.",
            "Cybersecurity involves protecting systems from threats like malware, phishing, and hacking. Best practices include using strong passwords, encryption, and multi-factor authentication.",
            "Cloud computing provides on-demand computing resources over the internet. Popular services include IaaS, PaaS, and SaaS, with providers like AWS, Google Cloud, and Azure.",
            "Blockchain is a decentralized ledger technology used for secure transactions. It powers cryptocurrencies like Bitcoin and has applications in finance, supply chain, and data security.",
            "Quantum computing leverages quantum mechanics to perform complex computations at unprecedented speeds. It has potential applications in cryptography, optimization, and AI.",
            "Deep learning is a subset of machine learning that uses neural networks to process data. It is used in image recognition, natural language processing, and self-driving cars.",
            "NLP enables computers to understand and generate human language. Python libraries like NLTK and spaCy are widely used for tasks such as text classification, sentiment analysis, and chatbot development.",
            "AI is transforming industries, creating new job opportunities while raising ethical concerns. It is crucial to balance innovation with responsible AI development.",
            "IoT connects devices to the internet for automation and data exchange. Smart homes, wearable devices, and industrial automation are key IoT applications.",
            "Full-stack development involves frontend (HTML, CSS, JavaScript) and backend (Python, Node.js, Django) technologies to create dynamic and interactive web applications.",
            "Python is widely used in data science for data analysis, visualization, and machine learning. Libraries like Pandas, NumPy, and Matplotlib make data manipulation easier."
        ]


        img_url=[
            'https://picsum.photos/id/1/800/300',
            'https://picsum.photos/id/2/800/300',
            'https://picsum.photos/id/3/800/300',
            'https://picsum.photos/id/4/800/300',
            'https://picsum.photos/id/5/800/300',
            'https://picsum.photos/id/6/800/300',
            'https://picsum.photos/id/7/800/300',
            'https://picsum.photos/id/8/800/300',
            'https://picsum.photos/id/9/800/300',
            'https://picsum.photos/id/10/800/300',
            'https://picsum.photos/id/11/800/300',
            'https://picsum.photos/id/12/800/300',
            'https://picsum.photos/id/13/800/300',
            'https://picsum.photos/id/14/800/300',
            'https://picsum.photos/id/15/800/300',
            
            
        ]

        categories=Category.objects.all()
        for title,content,img_url in zip(title,content,img_url):
            category=random.choice(categories)
            Post.objects.create(title=title,content=content,img_url=img_url,category=category)


        self.stdout.write(self.style.SUCCESS("completed inserting Data!!"))