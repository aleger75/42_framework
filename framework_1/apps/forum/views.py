from .forms import AnswerForm, CommentForm, NewThreadForm
from .models import SubCategory, Category, Thread, Answer, Comment
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin


class ForumView(ListView):
    model = Category
    template_name = 'forum.html'

    def get_queryset(self):
        categories = self.model.objects.all()

        return [(category, SubCategory.objects.filter(parent_category=category)) for category in categories]


class ForumViewCategory(ListView):
    model = SubCategory
    template_name = 'forum_category.html'
    context_object_name = 'subcategories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_pk = self.kwargs.get('pk')
        category = Category.objects.get(pk=category_pk)
        context['category'] = category

        threads = Thread.objects.filter(category_related=category)
        context['threads'] = threads

        return context

    def get_queryset(self):
        category_pk = self.kwargs.get('pk')
        category = Category.objects.get(pk=category_pk)

        return self.model.objects.filter(parent_category=category)


class ForumViewSubCategory(ListView):
    model = Thread
    template_name = 'forum_subcategory.html'
    context_object_name = 'threads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_pk = self.kwargs.get('c_pk')
        context['category'] = Category.objects.get(pk=category_pk)

        subcategory_pk = self.kwargs.get('sc_pk')
        context['subcategory'] = SubCategory.objects.get(pk=subcategory_pk)

        return context

    def get_queryset(self):
        subcategory_pk = self.kwargs.get('sc_pk')
        subcategory = SubCategory.objects.get(pk=subcategory_pk)

        return self.model.objects.filter(category_related=subcategory)


class ForumViewThread(DetailView):
    model = Thread
    template_name = 'forum_view_thread.html'
    pk_url_kwarg = 't_pk'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_object = Category.objects.filter(pk=self.kwargs.get('c_pk'))
        context['category'] = category_object[0] if len(category_object) else None

        subcategory_object = SubCategory.objects.filter(pk=self.kwargs.get('sc_pk'))
        context['subcategory'] = subcategory_object[0] if len(subcategory_object) else None

        answers = Answer.objects.filter(thread_related=self.get_object())
        context['answers'] = [(answer, Comment.objects.filter(answer_related=answer)) for answer in answers]

        context['answer_form'] = AnswerForm()
        context['comment_form'] = CommentForm()

        return context


class ForumAnswer(SingleObjectMixin, FormView):
    form_class = AnswerForm
    model = Thread
    pk_url_kwarg = 't_pk'

    def custom_redirect(self):
        self.object = self.get_object()
        c_pk = self.kwargs.get('c_pk')
        t_pk = self.object.pk
        if 'sc_pk' in self.kwargs:
            sc_pk = self.kwargs.get('sc_pk')
            return redirect('forum_view_subcategory_thread', c_pk=c_pk, sc_pk=sc_pk, t_pk=t_pk)
        else:
            return redirect('forum_view_category_thread', c_pk=c_pk, t_pk=t_pk)

    def get(self, request, *args, **kwargs):
        return self.custom_redirect()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            body = form.cleaned_data.get('body')
            author = request.user
            thread_related = self.object
            new_answer = Answer(body=body, author=author, thread_related=thread_related)
            new_answer.save()
            messages.success(request, _('Answer successfully created'))
        else:
            messages.error(request, _('Invalid answer'))
        return self.custom_redirect()


class ForumComment(SingleObjectMixin, FormView):
    form_class = CommentForm
    model = Answer
    pk_url_kwarg = 'a_pk'

    def custom_redirect(self):
        self.object = self.get_object()
        c_pk = self.kwargs.get('c_pk')
        t_pk = self.kwargs.get('t_pk')
        if 'sc_pk' in self.kwargs:
            sc_pk = self.kwargs.get('sc_pk')
            return redirect('forum_view_subcategory_thread', c_pk=c_pk, sc_pk=sc_pk, t_pk=t_pk)
        else:
            return redirect('forum_view_category_thread', c_pk=c_pk, t_pk=t_pk)

    def get(self, request, *args, **kwargs):
        return self.custom_redirect()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            body = form.cleaned_data.get('comment')
            author = request.user
            answer_related = self.object
            new_comment = Comment(body=body, author=author, answer_related=answer_related)
            new_comment.save()
            messages.success(request, _('Comment successfully added'))
        else:
            messages.error(request, _('Invalid comment'))
        return self.custom_redirect()


class ForumNewThread(FormView):
    form_class = NewThreadForm
    template_name = 'forum_create_thread.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_object = Category.objects.filter(pk=self.kwargs.get('c_pk'))
        context['category'] = category_object[0] if len(category_object) else None

        subcategory_object = SubCategory.objects.filter(pk=self.kwargs.get('sc_pk'))
        context['subcategory'] = subcategory_object[0] if len(subcategory_object) else None

        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        category_pk = self.kwargs.get('c_pk')
        category = Category.objects.get(pk=category_pk)
        subcategory = None
        if 'sc_pk' in self.kwargs:
            subcategory_pk = self.kwargs.get('sc_pk')
            subcategory = SubCategory.objects.get(pk=subcategory_pk)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            author = request.user
            new_thread = Thread(title=title, category_related=category) if not subcategory else Thread(title=title,
                                                                                                       category_related=subcategory)
            new_thread.save()
            new_answer = Answer(author=author, body=body, thread_related=new_thread)
            new_answer.save()
            messages.success(request, _('Thread successfully created'))
            if subcategory:
                return redirect('forum_view_subcategory_thread', c_pk=category.pk, sc_pk=subcategory.pk, t_pk=new_thread.pk)
            else:
                return redirect('forum_view_category_thread', c_pk=category_pk, t_pk=new_thread.pk)
        else:
            messages.error(request, _('Could not create thread'))
            return redirect('forum_view')