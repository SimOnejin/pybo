$(function() {

        $(window).scroll(function(){

      var sct = $(this).scrollTop();

      //console.log(sct);

      $('.fly').stop().animate({

        top: sct

      })

    })

    })