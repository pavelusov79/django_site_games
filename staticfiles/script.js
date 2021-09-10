document.querySelector(".pull").onclick = function() {
	this.classList.toggle("pull-active");
	document.querySelector(".menu ul").classList.toggle("active");
} 

var showLarge = document.querySelector(".product_left .big");
var markImg = document.querySelector(".product_left div");
var img = document.querySelectorAll(".product_left div img");
var path = window.location.pathname;


for(var i = 0; i<img.length; i++) {
	img[i].onclick = function(e) {
		for (var j = 0; j<img.length; j++) {
			img[j].classList.remove("select");
		}
		e.target.classList.add("select");
		showLarge.src = e.target.src;
	}
}


$(function() {
  // при нажатии на кнопку arrow
  $('.arrow').click(function() {
    // переместиться в верхнюю часть страницы
    $("html, body").animate({
      scrollTop:0
    },1000);
  })
})
// при прокрутке окна (window)
$(window).scroll(function() {
  // если пользователь прокрутил страницу более чем на 200px
  if ($(this).scrollTop()>800) {
    // то сделать кнопку arrow видимой
    $('.arrow').fadeIn();
  }
  // иначе скрыть кнопку arrow
  else {
    $('.arrow').fadeOut();
  }
});

var news = document.querySelector(".show_news");
var news_p = document.querySelectorAll(".show_text");
if(path == "/") {
	news.addEventListener("click", (e) => {
		for(var i = 0; i < news_p.length; i++) {
			news_p[i].children[1].className = 'hide';
			news_p[i].children[0].innerHTML = "&#43";
		}
		e.target.children[0].innerHTML = "&#45";
		e.target.children[1].className = 'text_r';
	});
}

window.onload = function() {
	var block = document.querySelectorAll('.col-7');

	for(var i=0; i<block.length; i++) {
		block[i].onclick = function(e) {
			console.log(e.target);
			if(e.target == this.children[1].children[1] & this.children[1].children[1].innerHTML == "read more...") {
				this.children[1].children[0].style.display = "block";
				this.children[1].children[1].innerHTML = "hide text...";
			} else {
				this.children[1].children[0].style.display = "none";
				this.children[1].children[1].innerHTML = "read more...";
			}
		}
	}
}


$('#sub_form').submit(function() {
    var url = $(this).attr('action');
    var type = $(this).attr('method');
    $.ajax({
        type: type,
        url: url,
        data: $(this).serialize(),
        success: function(response) {
            console.log('success');
            $('#sub_form').css('display', 'none');
            $('#subscription').css('display', 'block').html('Thank you for subscription!');
        }
    });
    return false;
});
