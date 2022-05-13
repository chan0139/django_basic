from django.shortcuts import render
from django.http import HttpResponse
from .models import GuessNumbers
from .forms import PostForm
from django.shortcuts import render, redirect

def index(request):

    lottos = GuessNumbers.objects.all()
    #{"lottos:lottos"} <- context
    return render(request, 'lotto/default.html', {"lottos":lottos})

    # generate 함수 여기서 가능
    # row.lottos = ""
    # origin = list(range(1,46)) # 1~46의 숫자 리스트
    # # 6개 번호 set 갯수만큼 1~46 뒤섞은 후 앞의 6개 골라내어 sorting
    # for _ in range(0, self.num_lotto):
    #     random.shuffle(origin)
    #     guess = origin[:6]
    #     guess.sort()
    #     row.lottos += str(guess) +'\n' # 로또 번호 str에 6개 번호 set 추가
    # row.update_date = timezone.now()
    # row.save() # GuessNumbers object를 DB에 저장
    #
    # return HttpResponse('<h1>Hello, world!</h1>')

def hello(request):
    return HttpResponse("<h1 style='color:red;'>Hello, world!</h1>")

def post(request):
    if request.method == "POST":
        # print(request.POST) # 주석을 풀면 새로운 로또 번호 생성 후 cmd에서 이 값을 확인할 수 있음
        # print(request.method) # 주석을 풀면 새로운 로또 번호 생성 후 cmd에서 이 값을 확인할 수 있음
        # 사용자로부터 넘겨져 온 POST 요청 데이터를 담아 PostForm 객체 생성
        form = PostForm(request.POST) # filled form
        # print(type(form)) # <class 'lotto.forms.PostForm'>
        # print(form)
        if form.is_valid():
	    # 사용자로부터 입력받은 form 데이터에서 추가로 수정해주려는 사항이 있을 경우 save를 보류함
            lotto = form.save(commit = False) # 최종 DB 저장은 아래 generate 함수 내부의 .save()로 처리
            print(type(lotto)) # <class 'lotto.models.GuessNumbers'>
            print(lotto)
            lotto.generate()
            return redirect('index') # urls.py의 name='index'에 해당
            # -> 상단 from django.shortcuts import render, redirect 수정
    else:
        form = PostForm() # empty form
        return render(request, "lotto/form.html", {"form": form})

def detail(request, lottokey):
    lotto = GuessNumbers.objects.get(pk = lottokey)
    return render(request, "lotto/detail.html", {"lotto": lotto})
