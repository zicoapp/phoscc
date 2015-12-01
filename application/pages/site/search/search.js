jQuery(document).ready(function() {

    var currentPage = 1;
    var canload = true;

    jQuery(".collage").justifiedGallery({
        rowHeight: 240,
        fixedHeight: false,
        maxRowHeight: '120%',
        margins: 8,
        lastRow: 'nojustify',
        captionSettings: {
        	animationDuration: 500, 
        	visibleOpacity: 1,
        	nonVisibleOpacity: 0.0
        }
    });

    $(window).scroll(function() {
        if ($(window).scrollTop() + $(window).height() == $(document).height()) {
            console.log("scroll to end");
            if (canload) {
                canload = false;
                $.ajax({
                    url: '/_load',
                    data: {"url": window.location.href, "category": $('#id-category-input').val(), "page": currentPage+1},
                    type: 'POST',
                    dataType: 'json',
                    success: function(response) {
                        var plist = jQuery.parseJSON(response['result']);
                        if (plist.length > 0) {
                            for (var i = 0; i < plist.length; i++) {
                                photo = plist[i];
                                console.log(plist[i]['url']);
                                $('.collage').append(
                                    "<div class=\"photo-wrapper\">" +
                                    "<img src=\"" + photo['url_thumbnail'] + "\"/>" + 
                                    "<div class=\"caption\">" +
                                        "<a class=\"photo-overlay-mask\" href=\"" + photo['url'] + "\" target=\"_blank\"></a>" + 
                                        "<div class=\"caption-meta meta-left\">" +
                                            "<i class=\"iconfont icon-copyright2\"></i>" +
                                            "<i class=\"iconfont icon-copyright5\"></i>" +
                                        "</div>" +
                                        "<div class=\"caption-meta meta-right\">" +
                                            "<span class=\"meta-author\">" +
                                                "<span class=\"meta-author-by\">By </span><a href=\"http://baidu.com\">Paul Green</a>" +
                                            "</span>" +
                                            "<a class=\"meta-download\" href=\"" + photo['url'] + "?download\"><i class=\"iconfont icon-dload\"></i>" +
                                            "</a>" +
                                        "</div>" +
                                    "</div>" +
                                    "</div>"
                                );
                            }
                            $('.collage').justifiedGallery('norewind');
                            currentPage++;
                            canload = true;
                        }
                    },
                    error: function(error) {
                        console.log(error);
                        $this.click(submitcats);
                        loading = false;
                    }
                });
            }
        }
    });

});

// // Here we apply the actual CollagePlus plugin
// function collage() {
//     $('.Collage').removeWhitespace().collagePlus(
//         {
//             'fadeSpeed'     : 2000,
//             'targetHeight'  : 300,
//             'effect'        : 'effect-2',
//             'direction'     : 'vertical',
//             'allowPartialLastRow':true
//         }
//     );
// };

// // This is just for the case that the browser window is resized
// var resizeTimer = null;
// $(window).bind('resize', function() {
//     // hide all the images until we resize them
//     $('.Collage .Image_Wrapper').css("opacity", 0);
//     // set a timer to re-apply the plugin
//     if (resizeTimer) clearTimeout(resizeTimer);
//     resizeTimer = setTimeout(collage, 200);
// });