from django.shortcuts import render


def ordenes_compra(request):	
	return render(request,'ordenes_compra.html')

def nueva_orden(request):	
	return render(request,'nueva_orden.html')