from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
        CreateView, FormView, DetailView, TemplateView, ListView)
from django.urls import reverse_lazy
from django.db.models import Count

from django import forms
from . forms import TopicForm
from . forms import TopicCreateForm
from . forms import (
    TopicModelForm, TopicForm, CommentModelForm,
    LoginedUserTopicModelForm, LoginedUserCommentModelForm
)
from . models import Topic
from . models import Category
from . models import Comment

from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template

class TopicDetailView(DetailView):
    template_name = 'room/detail_topic.html'
    model = Topic
    context_object_name = 'topic'

def topic_create(request):
    template_name = 'room/create_topic.html'
    ctx = {}
    if request.method == 'GET':
        form = TopicForm()
        ctx['form'] = form
        return render(request, template_name, ctx)

    if request.method == 'POST':
        topic_form = TopicForm(request.POST)
        if topic_form.is_valid():
            # topic_form.save()
            topic = Topic()
            cleaned_data = topic_form.cleaned_data
            topic.title = cleaned_data['title']
            topic.message = cleaned_data['message']
            topic.user_name = cleaned_data['user_name']
            topic.category = cleaned_data['category']
            topic.save()
            return redirect(reverse_lazy('base:top'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)

class TopicCreateView(CreateView):
    template_name = 'room/create_topic.html'
    form_class = LoginedUserTopicModelForm
    model = Topic
    success_url = reverse_lazy('base:top')

    def get_form_class(self):
        '''
        ログイン状態によってフォームを動的に変更する
        '''
        if self.request.user.is_authenticated:
            return LoginedUserTopicModelForm
        else:
            return TopicModelForm

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            ctx['category'] = form.cleaned_data['category']
            return render(self.request, 'room/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'room/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            form.save(self.request.user)
            # メール送信処理
            template = get_template('room/mail/topic_mail.html')
            user_name = self.request.user.username if self.request.user else form.cleaned_data['user_name']
            mail_ctx={
                'title': form.cleaned_data['title'],
                'user_name': user_name,
                'message': form.cleaned_data['message'],
            }
            EmailMessage(
                subject='トピック作成: ' + form.cleaned_data['title'],
                body=template.render(mail_ctx),
                # form_email='hogehoge@example.com',
                to=['admin@example.com'],
                cc=['admin2@example.com'],
                bcc=['admin3@example.com'],
            ).send()
            # return super().form_valid(form)
            return redirect(self.success_url)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('base:top'))

class CategoryView(ListView):
    template_name = 'room/category.html'
    context_object_name = 'topic_list'
    paginate_by = 1 # 1ページに表示するオブジェクト数 サンプルのため1にしています。
    page_kwarg = 'p' # GETでページ数を受けるパラメータ名。指定しないと'page'がデフォルト

    def get_queryset(self):
        return Topic.objects.filter(category__url_code = self.kwargs['url_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(Category, url_code=self.kwargs['url_code'])
        return ctx

class TopicAndCommentView(FormView):
    template_name = 'room/detail_topic.html'
    form_class = LoginedUserCommentModelForm

    def get_form_class(self):
        '''
        ログイン状態によってフォームを動的に変更する
        '''
        if self.request.user.is_authenticated:
            return LoginedUserCommentModelForm
        else:
            return CommentModelForm

    def form_valid(self, form):
        # comment = form.save(commit=False)
        # comment.topic = Topic.objects.get(id=self.kwargs['pk'])
        # comment.no = Comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        # comment.save()

        # Comment.objects.create_comment(
        #     user_name=form.cleaned_data['user_name'],
        #     message=form.cleaned_data['message'],
        #     topic_id=self.kwargs['pk'],
        #     image=form.cleaned_data['image']
        # )
        kwargs = {}
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user

        form.save_with_topic(self.kwargs.get('pk'), **kwargs)
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('room:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(
                topic_id=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('no')
        return ctx

class TopicCreateViewBySession(FormView):
    template_name = 'room/create_topic.html'
    # form_class = TopicModelForm
    form_class = LoginedUserTopicModelForm

    def post(self, request, *args, **kwargs):
        ctx = {}
        if request.POST.get('next', '') == 'back':
            if 'input_data' in self.request.session:
                input_data = self.request.session['input_data']
                # form = TopicModelForm(input_data)
                form = self.form_class(input_data)
                ctx['form'] = form
            return render(request, self.template_name, ctx)
        elif request.POST.get('next', '') == 'create':
            if 'input_data' in request.session:
                form = self.form_class(request.session['input_data'])
                form.save()
                # Topic.objects.create_topic(
                #     title=request.session['input_data']['title'],
                #     user_name=request.session['input_data']['user_name'],
                #     category_id=request.session['input_data']['category'],
                #     message=request.session['input_data']['message']
                # )
                # メール送信処理
                template = get_template('room/mail/topic_mail.html')
                mail_ctx={
                    'title': form.cleaned_data['title'],
                    'user_name': form.cleaned_data['user_name'],
                    'message': form.cleaned_data['message'],
                    }
                EmailMessage(
                    subject='トピック作成: ' + form.cleaned_data['title'],
                    body=template.render(mail_ctx),
                    from_email='hogehoge@example.com',
                    to=['admin@example.com'],
                    cc=['admin2@example.com'],
                    bcc=['admin3@example.com'],
                    ).send()
                response = redirect(reverse_lazy('base:top'))
                response.set_cookie('categ_id', request.session['input_data']['category'])
                request.session.pop('input_data') # セッションに保管した情報の削除
                return response
            # return redirect(reverse_lazy('base:top'))
        elif request.POST.get('next', '') == 'confirm':
            form = TopicModelForm(request.POST)
            if form.is_valid():
                ctx = {'form': form}
                # セッションにデータを保存
                input_data = {
                    'title': form.cleaned_data['title'],
                    'user_name': form.cleaned_data['user_name'],
                    'message': form.cleaned_data['message'],
                    'category': form.cleaned_data['category'].id,
                    }
                request.session['input_data'] = input_data
                ctx['category'] = form.cleaned_data['category']
                return render(request, 'room/confirm_topic.html', ctx)
            else:
                return render(request, self.template_name, {'form': form})
    def get_context_data(self):
        ctx = super().get_context_data()
        if 'categ_id' in self.request.COOKIES:
            form = ctx['form']
            form['category'].field.initial = self.request.COOKIES['categ_id']
            ctx['form'] = form
        return ctx
