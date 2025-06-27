from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "বি.দ্র.: আপনি যদি home() ফাংশন urls.py ফাইলে রাখতে চান, তাহলে ইমপোর্ট করা দরকার নেই। তখন home() ফাংশনটা শুধু একবার রাখলেই হবে। তবে best practice হলো views আলাদা ফাইলে রাখা।"
    )
