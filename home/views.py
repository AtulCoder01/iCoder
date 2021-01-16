from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User # for craete user
from django.contrib.auth import authenticate, login, logout # for user authonticate (Login)
from blog.models import Post


# Create your views here.
# HTML Pages
def home(request):
    # Fetch top three posts based on number of views
    views = Post.objects.values_list('views', flat=True)
    views = sorted(views)
    views.reverse()
    # print(views)
    top_three_posts = {}
    all_posts = Post.objects.all()
    count = 0
    # here we store only top 3 post
    for view in views:
        for post in all_posts:
            if post.views == view and count < 3:
                top_three_posts[post] = post
                count += 1
                continue

    # print(top_three_view)

    # print(top_three_posts)
            
    context = {'top_three_posts': top_three_posts}
    return render(request, 'home/home.html', context)
    # return HttpResponse('This is home')

def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse('This is about')

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name) < 2 or len(email) < 3 or len(phone)<4:
            # we use The messages framework django (message flashing)
            messages.error(request, 'Please fill the form correcty')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been successfully sent')

    return render(request, 'home/contact.html')

def search(request):
    # allPosts = Post.objects.all()
    # This is a very fragile solution as it requires the user to know an exact substring of the author’s name. A better approach could be a case-insensitive match (icontains), but this is only marginally better.
    query = request.GET['query']
    # we disallowed log query
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.warning(request, 'No search result found. Please refine your query.')
    params = {'allPosts':allPosts, 'query':query}
    return render(request, 'home/search.html', params)

# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for erroneous inputs
        # username should be under 10 characters
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 character.')
            return redirect('home')

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(request, 'Username should cantain letters and numbers.')
            return redirect('home')

        # password should match
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match.')
            return redirect('home')

        #Create the user in django built-in
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your iCoder account has been successfully created.')
        # print(username, fname, lname, email, pass1, pass2)
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        # Get the post parameter
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In.')
            return redirect('home')
        else:
            messages.error(request, 'Invailed Credentials, Please try again.')
            return redirect('home')

    return HttpResponse('handleLogin')

def handleLogout(request):
    # if request.method == 'POST':
    if request.method:
        logout(request)
        messages.success(request, 'Successfully Logged Out.')
        return redirect('home')
    
    return HttpResponse('handleLogout')
