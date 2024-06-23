from django.shortcuts import render, redirect, get_object_or_404
from .models import Video, Image, Category
from .forms import VideoForm, VideoDeleteForm, ImageForm, DeleteImageForm
from .forms import AssignmentForm
from .models import Assignment
from .forms import EbookForm
from .models import Ebook
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect







def index(request):
    videos = Video.objects.all()
    return render(request, 'gallery/index.html', {'videos': videos})

def upload_delete_videos(request):
    videos = Video.objects.all()

    if request.method == 'POST':
        if 'upload' in request.POST:
            form = VideoForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('gallery:upload_delete_videos')
        elif 'delete' in request.POST:
            delete_form = VideoDeleteForm(request.POST)
            if delete_form.is_valid():
                video_ids = delete_form.cleaned_data.get('video_ids')
                Video.objects.filter(id__in=video_ids).delete()
                return redirect('gallery:upload_delete_videos')
    else:
        form = VideoForm()
        delete_form = VideoDeleteForm()

    return render(request, 'gallery/upload_delete_videos.html', {
        'form': form,
        'delete_form': delete_form,
        'videos': videos
    })

def gallery(request):
    videos = Video.objects.all()
    return render(request, 'gallery/gallery.html', {'videos': videos})

def display_videos(request):
    videos = Video.objects.all()
    return render(request, 'gallery/display_videos.html', {'videos': videos})

def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        video.delete()
        return redirect('gallery:gallery')  # Redirect to the appropriate URL after deletion
    
    return render(request, 'gallery/confirm_delete_video.html', {'video': video})

def gallery_view(request):
    categories = Category.objects.all()
    images = Image.objects.all()
    return render(request, 'gallery/image_gallery.html', {'categories': categories, 'images': images})

def category_view(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    images = category.images.all()
    return render(request, 'gallery/image_gallery.html', {'categories': categories, 'images': images})

def image_gallery(request):
    categories = Category.objects.all()
    images = Image.objects.all()
    return render(request, 'gallery/image_gallery.html', {'categories': categories, 'images': images})

def upload_delete_images(request):
    if request.method == 'POST':
        # Handling Image Upload
        if 'upload' in request.POST:
            upload_form = ImageForm(request.POST, request.FILES)
            if upload_form.is_valid():
                upload_form.save()
                return redirect('gallery:upload_delete_images')
        else:
            upload_form = ImageForm()

        # Handling Image Deletion
        if 'delete' in request.POST:
            delete_form = DeleteImageForm(request.POST)
            if delete_form.is_valid():
                image_id = delete_form.cleaned_data['image_id']
                image = get_object_or_404(Image, id=image_id)
                image.delete()
                return redirect('gallery:upload_delete_images')
        else:
            delete_form = DeleteImageForm()

    else:
        upload_form = ImageForm()
        delete_form = DeleteImageForm()

    images = Image.objects.all()
    categories = Category.objects.all()
    context = {
        'upload_form': upload_form,
        'delete_form': delete_form,
        'images': images,
        'categories': categories,
    }
    return render(request, 'gallery/upload_delete_images.html', context)


def view_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'gallery/view_video.html', {'video': video})



@login_required
def upload_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.instructor = request.user
            assignment.save()
            return redirect('gallery:assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'gallery/upload_assignment.html', {'form': form})

@login_required(login_url='/login/')
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'gallery/assignment_list.html', {'assignments': assignments})




@staff_member_required
def ebook_list(request):
    ebooks = Ebook.objects.all()
    return render(request, 'gallery/ebook_list.html', {'ebooks': ebooks})

@staff_member_required
def upload_ebook(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = form.save(commit=False)
            ebook.instructor = request.user
            ebook.save()
            return redirect('gallery:ebook_list')
    else:
        form = EbookForm()
    return render(request, 'gallery/upload_ebook.html', {'form': form})

def ebook_list(request):
    ebooks = Ebook.objects.all()
    return render(request, 'gallery/ebook_list.html', {'ebooks': ebooks})