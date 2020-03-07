(function ($) {
    "use strict";

    /*-------------------------------------
    Audio Player
    -------------------------------------*/
    var player = document.getElementById('audio_player');
    if(player !== null) {
        player.addEventListener("timeupdate", function () {
            var currentTime = player.currentTime,
                duration = player.duration,
                persent = Math.floor((currentTime / duration) * 100);
            $("#audio_player").parents('.audio-player-wrap').find('.progress .progress-bar').attr("aria-valuenow", persent);
            $("#audio_player").parents('.audio-player-wrap').find('.progress .progress-bar').css("width", persent + '%');
            $("#audio_player").parents('.audio-player-wrap').find('.current-duration').text(Math.floor(currentTime));
            $("#audio_player").parents('.audio-player-wrap').find('.total-duration').text(Math.floor(player.duration));
        });
    }
    $("#audioplayer").on('click', '.play', function(){
        var self = $(this);
        if (player.paused){
            player.play();
            self.addClass('btn-pause');
            self.removeClass('btn-play');
        }else{
            self.addClass('btn-play');
            self.removeClass('btn-pause');
            player.pause();
          }
    });
    
    $("#volume_control").on('change', '#rngVolume', function(){
        player.volume = $(this).val();
    });
    function stopSong(){
        player.currentTime = 0;
        player.pause();
    }


    

    /*-------------------------------------
    Tooltips
    -------------------------------------*/
    headerNsliderResize();
    var priceSlider = document.getElementById('price-range-filter');
    if (priceSlider) {
        noUiSlider.create(priceSlider, {
            start: [20, 80],
            connect: true,
            /*tooltips: true,*/
            range: {
                'min': 0,
                'max': 100
            },
            format: wNumb({
                decimals: 0
            }),
        });
        var marginMin = document.getElementById('price-range-min'),
            marginMax = document.getElementById('price-range-max');
        priceSlider.noUiSlider.on('update', function(values, handle) {
            if (handle) {
                marginMax.innerHTML = "$" + values[handle];
            } else {
                marginMin.innerHTML = "$" + values[handle];
            }
        });
    }

    // Tooltips
    $(document).on('mouseover', '.speaker-img-tooltip',
        function () {
            var self = $(this),
                tips = self.attr('data-tips');
            $tooltip = '<div class="eventalk-tooltip">' +
                '<div class="eventalk-tooltip-content">' + tips + '</div>' +
                '<div class="eventalk-tooltip-bottom"></div>' +
                '</div>';
            $('body').append($tooltip);
            var $tooltip = $('body > .eventalk-tooltip');
            var tHeight = $tooltip.outerHeight();
            var tBottomHeight = $tooltip.find('.eventalk-tooltip-bottom').outerHeight();
            var tWidth = $tooltip.outerWidth();
            var tHolderWidth = self.outerWidth();
            var top = self.offset().top - (tHeight + tBottomHeight);
            var left = self.offset().left;
            $tooltip.css({
                'top': top + 'px',
                'left': left + 'px',
                'opacity': 1
            }).show();
            if (tWidth <= tHolderWidth) {
                var itemLeft = (tHolderWidth - tWidth) / 2;
                left = left + itemLeft;
                $tooltip.css('left', left + 'px');
            } else {
                var itemLeft = (tWidth - tHolderWidth) / 2;
                left = left - itemLeft;
                if (left < 0) {
                    left = 0;
                }
                $tooltip.css('left', left + 'px');
            }
        })
        .on('mouseout', '.speaker-img-tooltip', function () {
            $('body > .eventalk-tooltip').remove();
        });

    /*-------------------------------------
    Current Day and Date
    -------------------------------------*/
    if($("#current_date").length) {
        document.getElementById("current_date").innerHTML = formatAMPM();
    }
    function formatAMPM() {
    var d = new Date(),
        months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
        days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    return days[d.getDay()]+' , '+months[d.getMonth()]+' '+d.getDate()+' , '+d.getFullYear();
    }
    
    /*-------------------------------------
    IE Fixing
    -------------------------------------*/
    function isIE() {
        var myNav = navigator.userAgent.toLowerCase();
        return (myNav.indexOf('msie') != -1 || myNav.indexOf('trident') != -1) ? true : false;
    }

    if (isIE()) {
        $('body').addClass('ie');
    }

    /*-------------------------------------
    Popup
    -------------------------------------*/
    var yPopup = $(".popup-youtube");
    if (yPopup.length) {
        yPopup.magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    }
    if ($('.zoom-gallery').length) {
        $('.zoom-gallery').each(function () { // the containers for all your galleries
            $(this).magnificPopup({
                delegate: 'a.ne-zoom', // the selector for gallery item
                type: 'image',
                gallery: {
                    enabled: true
                }
            });
        });
    }

    /*-------------------------------------
     Jquery Serch Box
     -------------------------------------*/
    $(document).on('click', '#top-search-form .search-button', function (e) {
        e.preventDefault();
        var targrt = $(this).prev('input.search-input');
        targrt.animate({
            width: ["toggle", "swing"],
            height: ["toggle", "swing"],
            opacity: "toggle"
        }, 500, "linear");
        return false;
    });

    /*-------------------------------------
    On click loadmore functionality 
    -------------------------------------*/
    $('.loadmore-four-item').on('click', function (e) {
        e.preventDefault();
        var _this = $(this),
            _parent = _this.parents('.menu-list-wrapper'),
            _target = _parent.find('.menu-list'),
            _set = _target.find('.menu-item.hidden').slice(0, 4);
        if (_set.length) {
            _set.animate({
                opacity: 0
            });
            _set.promise().done(function () {
                _set.removeClass('hidden');
                _set.show().animate({
                    opacity: 1
                }, 1000);
            });
        } else {
            _this.text('No more item to display');
        }
        return false;
    });
    /*********************************/
    $('.loadmore-one-item').on('click', function (e) {
        e.preventDefault();
        var _this = $(this),
            _parent = _this.parents('.menu-list-wrapper'),
            _target = _parent.find('.menu-list'),
            _set = _target.find('.menu-item.hidden').slice(0, 1);
        if (_set.length) {
            _set.animate({
                opacity: 0
            });
            _set.promise().done(function () {
                _set.removeClass('hidden');
                _set.show().animate({
                    opacity: 1
                }, 1000);
            });
        } else {
            _this.text('No more item to display');
        }
        return false;
    });
    /*********************************/
    $('.loadmore-three-item').on('click', function (e) {
        e.preventDefault();
        var _this = $(this),
            _parent = _this.parents('.menu-list-wrapper'),
            _target = _parent.find('.menu-list'),
            _set = _target.find('.menu-item.hidden').slice(0, 3);
        if (_set.length) {
            _set.animate({
                opacity: 0
            });
            _set.promise().done(function () {
                _set.removeClass('hidden');
                _set.show().animate({
                    opacity: 1
                }, 1000);
            });
        } else {
            _this.text('No more item to display');
        }
        return false;
    });

    /*-------------------------------------
     jQuery MeanMenu activation code
     --------------------------------------*/
    $('nav#dropdown').meanmenu({
        siteLogo: "<div class='mobile-menu-nav-back'><a href='index.html'><img src='/static/img/pycon_logo_square_60x60.png'/></a></div>"
    });

    /*-------------------------------------
    // jquery zoom activation code
    -------------------------------------*/
    var ecomZoom = $('.ex1');
    if (ecomZoom.length) {
        $('.ex1').zoom();
    }

    /*-------------------------------------
     Jquery Scollup
     -------------------------------------*/
    $.scrollUp({
        scrollText: '<i class="fa fa-angle-up"></i><p>TOP</p>',
        easingType: 'linear',
        scrollSpeed: 900,
        animation: 'fade'
    });

    /*-------------------------------------
    Offcanvas Menu activation code
    -------------------------------------*/
    $('#wrapper').on('click', '#side-menu-trigger a.menu-bar', function (e) {
        e.preventDefault();
        var $this = $(this),
            wrapper = $(this).parents('body').find('>#wrapper'),
            wrapMask = $('<div />').addClass('offcanvas-mask');
        wrapper.addClass('open').append(wrapMask);
        $this.addClass('open');
        $this.next('.menu-times').removeClass('close');
        document.getElementById('offcanvas-body-wrapper').style.right = '0';
        return false;
    });
    $('#wrapper').on('click', '#side-menu-trigger a.menu-times', function (e) {
        e.preventDefault();
        var $this = $(this);
        $("#offcanvas-body-wrapper").attr('style', '');
        $this.prev('.menu-bar').removeClass('open');
        $this.addClass('close');
        closeSideMenu();
        return false;
    });
    $('#wrapper').on('click', '#offcanvas-nav-close a', function (e) {
        closeSideMenu();
        return false;
    });
    $(document).on('click', '#wrapper.open .offcanvas-mask', function () {
        closeSideMenu();
    });
    $(document).on('keyup', function (event) {
        if (event.which === 27) {
            event.preventDefault();
            closeSideMenu();
        }
    });

    function closeSideMenu() {
        var wrapper = $('body').find('>#wrapper'),
            $this = $('#side-menu-trigger a.menu-times');
        wrapper.removeClass('open').find('.offcanvas-mask').remove();
        $("#offcanvas-body-wrapper").attr('style', '');
        $this.prev('.menu-bar').removeClass('open');
        $this.addClass('close');
    }

    /*-------------------------------------
    Select2 activation code
    -------------------------------------*/
    if ($('#archive-search select.select2').length) {
        $('#archive-search select.select2').select2({
            theme: 'classic',
            dropdownAutoWidth: true,
            width: '100%'
        });
    }

    /*-------------------------------------
     Window load function
     -------------------------------------*/
    $(window).on('load', function () {

        /*-------------------------------------
        Masonry
        -------------------------------------*/
        var galleryIsoContainer = $('#no-equal-gallery');
        if (galleryIsoContainer.length) {
            var blogGallerIso = galleryIsoContainer.imagesLoaded(function() {
                blogGallerIso.isotope({
                    itemSelector: '.no-equal-item',
                    masonry: {
                        columnWidth: '.no-equal-item'
                    }
                });
            });
        }

        /*-------------------------------------
        Page Preloader
        -------------------------------------*/
        $('#preloader').fadeOut('slow', function () {
            $(this).remove();
        });

        /*-------------------------------------
         jQuery for Isotope initialization
         -------------------------------------*/
        var iso_container = $('.ne-isotope');
        if (iso_container.length > 0) {

            iso_container.each(function () {
                var $container = $(this),
                    selector = $container.find('.isotope-classes-tab a.current').attr('data-filter');
                // Isotope initialization
                var $isotope = $container.find('.featuredContainer').isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 750,
                        easing: 'linear',
                        queue: false
                    }
                });

                // Isotope filter
                $container.find('.isotope-classes-tab').on('click', 'a', function () {

                    var $this = $(this);
                    $this.parent('.isotope-classes-tab').find('a').removeClass('current');
                    $this.addClass('current');
                    var selector = $this.attr('data-filter');
                    $isotope.isotope({
                        filter: selector,
                        animationOptions: {
                            duration: 750,
                            easing: 'linear',
                            queue: false
                        }
                    });
                    return false;

                });

            });
        }

        /*-------------------------------------
         Countdown activation code
        -------------------------------------*/
        var eventCounter = $('#countdown');
        if (eventCounter.length) {
            eventCounter.countdown('2020/09/11', function(e) {
                $(this).html(e.strftime("<div class='countdown-section'><h2>%D</h2> <h3>day%!D</h3> </div><div class='countdown-section'><h2>%H</h2> <h3>hour%!H</h3> </div><div class='countdown-section'><h2>%M</h2> <h3>minutes</h3> </div><div class='countdown-section'><h2>%S</h2> <h3>seconds</h3> </div>"))

            });
        }

        /*-------------------------------------
         jQuery for Isotope initialization
         -------------------------------------*/
        var $container = $('.ne-isotope-all');
        if ($container.length > 0) {

            var selector = $container.find('.isotope-classes-tab a.current').attr('data-filter');
            console.log(selector);
            // Isotope initialization
            var $isotope = $container.find('.featuredContainer').isotope({
                filter: selector,
                animationOptions: {
                    duration: 750,
                    easing: 'linear',
                    queue: false
                }
            });

            // Isotope filter
            $container.find('.isotope-classes-tab').on('click', 'a', function () {

                var $this = $(this);
                $this.parent('.isotope-classes-tab').find('a').removeClass('current');
                $this.addClass('current');
                var selector = $this.attr('data-filter');
                $isotope.isotope({
                    filter: selector,
                    animationOptions: {
                        duration: 750,
                        easing: 'linear',
                        queue: false
                    }
                });
                return false;

            });
        }
    });

    /*-------------------------------------
     Accordion
     -------------------------------------*/
    var accordion = $('#accordion');
    accordion.children('.panel').children('.panel-collapse').each(function () {
        if ($(this).hasClass('in')) {
            $(this).parent('.panel').children('.panel-heading').addClass('active');
        }
    });
    accordion.on('show.bs.collapse', function (e) {
        $(e.target).prev('.panel-heading').addClass('active');
    }).on('hide.bs.collapse', function (e) {
        $(e.target).prev('.panel-heading').removeClass('active');
    });

    /*-------------------------------------
     Contact Form initiating
     -------------------------------------*/
    var contactForm = $('#contact-form');
    if (contactForm.length) {
        contactForm.validator().on('submit', function (e) {
            var $this = $(this),
                $target = contactForm.find('.form-response');
            if (e.isDefaultPrevented()) {
                $target.html("<div class='alert alert-success'><p>Please select all required field.</p></div>");
            } else {
                $.ajax({
                    url: "vendor/php/contact-form-process.php",
                    type: "POST",
                    data: contactForm.serialize(),
                    beforeSend: function () {
                        $target.html("<div class='alert alert-info'><p>Loading ...</p></div>");
                    },
                    success: function (text) {
                        if (text === "success") {
                            $this[0].reset();
                            $target.html("<div class='alert alert-success'><p>Message has been sent successfully.</p></div>");
                        } else {
                            $target.html("<div class='alert alert-success'><p>" + text + "</p></div>");
                        }
                    }
                });
                return false;
            }
        });
    }

    /*-------------------------------------
    Login pop up form
    -------------------------------------*/
    $('#login-button').on('click', function (e) {
        e.preventDefault();
        var self = $(this),
            target = self.next('#login-form');
        if (self.hasClass('open')) {
            target.slideUp('slow');
            self.removeClass('open');
        } else {
            target.slideDown('slow');
            self.addClass('open');
        }
    });
    $('#login-form').on('click', '.form-cancel', function (e) {
        e.preventDefault();
        var self = $(this),
            parent = self.parents('#login-form'),
            loginButton = parent.prev('#login-button');
        parent.slideUp('slow');
        loginButton.removeClass('open');
    });

    /*-------------------------------------
     Google Map
    -------------------------------------*/
    // if ($('#googleMap').length) {
    //     var initialize = function() {
    //             var mapOptions = {
    //                 zoom: 15,
    //                 scrollwheel: false,
    //                 center: new google.maps.LatLng(48.153429, 17.071716),
    //                 styles: [{
    //                     stylers: [{
    //                         saturation: -100
    //                     }]
    //                 }]
    //             };
    //             var map = new google.maps.Map(document.getElementById("googleMap"), mapOptions);
    //             var marker = new google.maps.Marker({
    //                 position: map.getCenter(),
    //                 animation: google.maps.Animation.BOUNCE,
    //                 icon: 'img/map-marker.png',
    //                 map: map
    //             });
    //         }
    //         // Add the map initialize function to the window load function
    //     google.maps.event.addDomListener(window, "load", initialize);
    // }

    /*-------------------------------------
     Carousel slider initiation
     -------------------------------------*/
    $('.et-carousel').each(function () {
        var carousel = $(this),
            loop = carousel.data('loop'),
            items = carousel.data('items'),
            margin = carousel.data('margin'),
            stagePadding = carousel.data('stage-padding'),
            autoplay = carousel.data('autoplay'),
            autoplayTimeout = carousel.data('autoplay-timeout'),
            smartSpeed = carousel.data('smart-speed'),
            dots = carousel.data('dots'),
            nav = carousel.data('nav'),
            navSpeed = carousel.data('nav-speed'),
            rXsmall = carousel.data('r-x-small'),
            rXsmallNav = carousel.data('r-x-small-nav'),
            rXsmallDots = carousel.data('r-x-small-dots'),
            rXmedium = carousel.data('r-x-medium'),
            rXmediumNav = carousel.data('r-x-medium-nav'),
            rXmediumDots = carousel.data('r-x-medium-dots'),
            rSmall = carousel.data('r-small'),
            rSmallNav = carousel.data('r-small-nav'),
            rSmallDots = carousel.data('r-small-dots'),
            rMedium = carousel.data('r-medium'),
            rMediumNav = carousel.data('r-medium-nav'),
            rMediumDots = carousel.data('r-medium-dots'),
            rLarge = carousel.data('r-Large'),
            rLargeNav = carousel.data('r-Large-nav'),
            rLargeDots = carousel.data('r-Large-dots'),
            center = carousel.data('center');
        carousel.owlCarousel({
            loop: (loop ? true : false),
            items: (items ? items : 4),
            lazyLoad: true,
            margin: (margin ? margin : 0),
            autoplay: (autoplay ? true : false),
            autoplayTimeout: (autoplayTimeout ? autoplayTimeout : 1000),
            smartSpeed: (smartSpeed ? smartSpeed : 250),
            dots: (dots ? true : false),
            nav: (nav ? true : false),
            navText: ['<i class="fa fa-angle-left" aria-hidden="true"></i>', '<i class="fa fa-angle-right" aria-hidden="true"></i>'],
            navSpeed: (navSpeed ? true : false),
            center: (center ? true : false),
            responsiveClass: true,
            responsive: {
                0: {
                    items: (rXsmall ? rXsmall : 1),
                    nav: (rXsmallNav ? true : false),
                    dots: (rXsmallDots ? true : false)
                },
                480: {
                    items: (rXmedium ? rXmedium : 2),
                    nav: (rXmediumNav ? true : false),
                    dots: (rXmediumDots ? true : false)
                },
                768: {
                    items: (rSmall ? rSmall : 3),
                    nav: (rSmallNav ? true : false),
                    dots: (rSmallDots ? true : false)
                },
                992: {
                    items: (rMedium ? rMedium : 4),
                    nav: (rMediumNav ? true : false),
                    dots: (rMediumDots ? true : false)
                },
                1200: {
                    items: (rLarge ? rLarge : 5),
                    nav: (rLargeNav ? true : false),
                    dots: (rLargeDots ? true : false)
                }
            }
        });
    });

    /*-------------------------------------
     Window onLoad and onResize event trigger
     -------------------------------------*/
    $(window).on('load resize', function () {
        var wHeight = $(window).height(),
            mLogoH = $('a.logo-mobile').outerHeight();
        wHeight = wHeight - 50;
        $('.mean-nav > ul').css('height', wHeight + 'px');

        /* add top margin */
        var target = $(".add-top-margin"),
            mHeight = $(".header-menu-fixed").outerHeight();
        target.css({
            "margin-top": mHeight + 'px'
        });
        var windowWidth = $(window).width();
        if (windowWidth < 991) {
            $('body.mean-container').css('margin-top', 0);
        }

    });

    /*-------------------------------------
     Jquery Stiky Menu at window Load
     -------------------------------------*/
    $(window).on('scroll', function() {
        var s = $('#sticker'),
            w = $('body'),
            h = s.outerHeight(),
            windowpos = $(window).scrollTop(),
            windowWidth = $(window).width(),
            h1 = s.parent('#header-one'),
            h2 = s.parent('#header-two'),
            h3 = s.parent('#header-three'),
            h3H = h3.find('.header-top-bar').outerHeight(),
            topBar = s.prev('.header-top-bar'),
            tempMenu;
        if (windowWidth > 991) {
            w.css('padding-top', '');
            var topBarH, mBottom = 0;
            if (h1.length) {
                topBarH = h = 1;
                mBottom = 0;
            } else if (h2.length) {
                mBottom = h2.find('.main-menu-area').outerHeight();
                topBarH = w.find("#top-slider").outerHeight();
                topBarH = mBottom + topBarH;
            } else if (h3.length) {
                topBarH = topBar.outerHeight();
                if (windowpos <= topBarH) {
                    if (h3.hasClass('header-fixed')) {
                        h3.css('top', '-' + windowpos + 'px');
                    }
                }
            }
            if (windowpos >= topBarH) {
                if (h3.length || h1.length) {
                    s.addClass('stick');
                }
                if (h3.length) {
                    if (h3.hasClass('header-fixed')) {
                        h3.css('top', '-' + topBarH + 'px');
                    } else {
                        w.css('padding-top', h + 'px');
                    }
                } else if (h2.length) {
                    h2.addClass('hide-menu');
                    tempMenu = h2.find('.main-menu-area').clone();
                    tempMenu.addClass('temp-main-menu stick').attr("id", '');
                    tempMenu.css({ opacity: 0 });
                    if (h2.find('.temp-main-menu.stick').length == 0) {
                        h2.append(tempMenu);
                        h2.find('.temp-main-menu.stick').animate({ opacity: 1 }, 100);
                    }
                    if (h2.find('.temp-main-menu.stick').length > 1) {
                        h2.find('.temp-main-menu.stick').last().remove();
                    }
                }
            } else {
                s.removeClass('stick');
                if (h3.length) {
                    w.css('padding-top', 0);
                } else if (h2.length) {
                    h2.removeClass('hide-menu');
                    h2.find('.stick.temp-main-menu').remove();
                }
            }
        }
    });

    function headerNsliderResize() {
        var Hh3 = $('#header-one'),
            wWidth = $(window).width(),
            Hh3slider = Hh3.parents('#wrapper').find("#fixed-type-slider"),
            mHeight = Hh3.outerHeight();
        if (wWidth < 992) {
            mHeight = $('body > .mean-bar').outerHeight();
            $("#downFromTop").css("margin-top", mHeight + 'px');
        }
        Hh3slider.css("margin-top", mHeight + 'px');
    }

    /*-------------------------------------
     Masonry
     -------------------------------------*/
     if($('.masonry-items').length){
        $('.masonry-items').masonry({
            itemSelector: '.masonry-item',
            columnWidth: '.masonry-item',
        });
     }
    
    /*-------------------------------------
     Input Quantity Up & Down activation code
     -------------------------------------*/
    $('#quantity-holder,#quantity-holder2').on('click', '.quantity-plus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity > 0) {
            $quantity = $quantity + 1;
            $target.val($quantity);
        } else {
            $target.val($quantity);
        }

    }).on('click', '.quantity-minus', function() {

        var $holder = $(this).parents('.quantity-holder');
        var $target = $holder.find('input.quantity-input');
        var $quantity = parseInt($target.val(), 10);
        if ($.isNumeric($quantity) && $quantity >= 2) {
            $quantity = $quantity - 1;
            $target.val($quantity);
        } else {
            $target.val(1);
        }

    });

    $('.menu-trigger').on('click', function() {
        var targetHolder = $('#main-nav-wrap'),
            target = $('#main-nav', targetHolder),
            targetMenu = target.find(' > ul').not('.temp-main-nav'),
            $tempMenu = target.find('ul.temp-main-nav'),
            self = $(this);
        if ($tempMenu.length) {
            self.find('i').removeClass('flaticon-unchecked').addClass('flaticon-menu');
            $tempMenu.animate({ top: '-100%' }, 500, function() {
                $(this).animate({ opacity: 0 }, 200, function() {
                    $(this).remove()
                });
            });
        } else {
            self.find('i').removeClass('flaticon-menu').addClass('flaticon-unchecked');
            var tempMenu = targetMenu.clone();
            tempMenu.css({
                visibility: 'visible',
                position: 'absolute',
                top: '-100%',
                left: 0,
                opacity: 0,
                width: targetMenu.outerWidth()
            }).addClass('temp-main-nav');
            target.append(tempMenu);
            tempMenu.animate({ opacity: 1 }, 200, function() {
                $(this).animate({ top: 0 }, 500);
            });
        }
    });

})(jQuery);
