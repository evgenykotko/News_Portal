# News_Portal - List of commands for DjangoShell

from newsportal.models import *

us1 = User.objects.create_user("Andrew")

us2 = User.objects.create_user("Evgeny")
 
aut1 = Author.objects.create(user=us1)

aut2 = Author.objects.create(user=us2)
 
catf = Category.objects.create(name="films") 

catm = Category.objects.create(name="music") 

cata = Category.objects.create(name="art")   

cats = Category.objects.create(name="sculpture") 

post1 = Post.objects.create(title_post="Rock", body_post="Рок (англ. Rock) — обобщающее название ряда направлений популярной музыки. Слово rock (в переводе с англ. - качать, укачивать, качаться) возникло как сокращение от названия рок-н-ролла, хронологически первого жанра рок-музыки, и обозначает характерные для рок-н-ролла ритмические ощущения, связанные с определённой формой движения, по аналогии с roll, twist, swing, shake. Чаще всего (но не обязательно) рок исполняется с использованием электрогитар и ударных. Для рок-музыкантов характерно исполнение композиций собственного сочинения. Однако сами по себе эти элементы ещё не делают музыку роком, а потому принадлежность некоторых стилей музыки к року оспаривается.", author_post=aut1)                     

post1.category_post.add(catm)

post2 = Post.objects.create(title_post="Impressionism", body_post="Импрессиони́зм (фр. impressionnisme ← impression впечатление) — одно из крупнейших течений в искусстве последней трети XIX — начала XX веков, зародившееся во Франции и затем распространившееся по всему миру[1]. Представители импрессионизма стремились разрабатывать методы и приёмы, которые позволяли наиболее естественно и живо запечатлеть реальный мир в его подвижности и изменчивости, передать свои мимолётные впечатления. Основой импрессионистического метода, который можно охарактеризовать как квинтэссенцию живописи, является восприятие и изображение объектов окружающей художника действительности не автономно, а в отношениях к окружающей пространственной и световоздушной среде: рефлексах, бликах, тепло-холодных отношениях света и тени; шире — запечатлеть само пространство и время. В этом заключаются и сильные, и слабые стороны импрессионистического метода. Сосредоточив своё внимание на тональных отношениях и валёрах, живописцы ослабили рисунок, композицию, чувство формы и материальности изображаемых предметов.", author_post=aut2) 

post2.category_post.add(cata)

news1 = Post.objects.create(type_post="news", title_post="News Today", body_post="В мистической драме Александра Велединского о поствоенном синдроме и поисках себя в мирной жизни прозвучат три песни группы Сплин: Сиануквиль, Праздник и Романс. по ходу повествования фильма главный герой Кир вместе с призраками своих боевых товарищей оказываются на концерте, где Сплины исполняют Романс и когда призраки, которых разумеется никто, кроме Кира не видит, покидают зал, Васильев и Николенко кивают им головами.", author_post=aut1) 

news1.category_post.add(catf)                                                                                                

news1.category_post.add(cats)

com1 = Comment.objects.create(text_comm="Cool!!!", post=post1, user=us1) 

com2 = Comment.objects.create(text_comm="Execelent!", post=post2, user=us2) 

com3 = Comment.objects.create(text_comm="Wow, is interest!", post=news1, user=us2)          

com4 = Comment.objects.create(text_comm="Oh, no! Again!", post=news1, user=us1)

post1.like()

post1.like()

post1.like()

post1.dislike()

post2.like()  

post2.like()

post2.like()

post2.like()

post2.like()

post2.dislike()

news1.like()  

news1.like()

news1.like()

news1.like()

news1.dislike()

com1.like()  

com1.like()

com1.dislike()
 
com2.like() 

com2.like()

com2.like()

com2.dislike()
 
com3.like()

com3.dislike() 
 
com4.like() 

com4.like()

com4.like()

com4.like()

com4.like()

com4.dislike()

aut = Author.objects.filter(pk=1)[0]

aut.update_rating()

aut1 = Author.objects.filter(pk=2)[0] 

aut1.update_rating()

Author.objects.all().order_by("-rating").values("user__username","rating")

post = Post.objects.filter(type_post="post").order_by("-rate_post")[0]

str(post.date_post.date()) + ", " + str(post.author_post.user) + ", " + str(post.rate_post) + ", " + post.title_post + ". " +  post.preview()

Comment.objects.filter(pk=post.pk).values("date_comm", "rate_comm", "user__username", "text_comm")
