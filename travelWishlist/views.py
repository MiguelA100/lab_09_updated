from pickle import FALSE

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.shortcuts import render
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.
@login_required()
def place_list(request):
    if request.method == 'POST':
            # create new place
            # create a form
        form = NewPlaceForm(request.POST)  # creating a form from data in request
        place = form.save(commit=False) # creating a model object form here
        place.user = request.user
        if form.is_valid():  # validation against DB connections
            place.save()  # save place to db
            return redirect('place_list')  # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()   # create HTML
    return render(request, 'travelWishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})

@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travelWishlist/visited.html', {'visited': visited})

@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    # return redirect('place_list')
    return redirect('place_list')


#def about(request):

 #   author = 'Miguel'
  #  # data from part of response
   # about = ('A website to create a list of places to visit')
    #return render(request, 'travelWishlist/about.html', {'author': author, 'about': about})



@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    # return render(request, 'travelWishlist/place_detail.html', {'place': place})

    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()

    # is this a GET request (show data + form), or a POST request (update Place object)?
    
    # if POST request, validate form data and update.
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary, refine later

        return redirect('Place_details', place_pk=place_pk)


    else:
        # if GET request, show Place infor and form
        # If place is visited, show form; if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travelWishlist/place_detail.html', {place: place, 'review_form':review_form})
        else:
            return render(request, 'travelWishlist/place_detail.html', {place: place})

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()