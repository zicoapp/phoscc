
// $('.bootstrap-tagsinput').change(function() {
// 	$(this).find('input').val('');
// })

jQuery(document).ready(function() {

	$('#testing').click(function() {
		alert($(".tagsinput-gen").val());
	});

    function preloadPhotos() {
        for (i = 0; i < comingPhotos.length; i++) { 
            item = comingPhotos[i];
            var $photo4tag = $("<img>");
            $photo4tag.attr("src", item['url_thumbnail']);
            $photo4tag.load(function(){
                console.log(item['url_thumbnail']);
            });
        }
    }

    preloadPhotos();

    // 获取下一组随机照片
    function nextPhotoList(switching) {
        $.getJSON('/_next4tag', {}, function(data) {
            console.log(data.result);
            var plist = jQuery.parseJSON(data.result);
            comingPhotos = comingPhotos.concat(plist);
            console.log('next group');
            // load photos for later usage
            preloadPhotos();
            if (switching) {
                nextPhoto();
            }
        });
        return false;
    }

    // 从缓存中加载下一张照片
    function nextPhoto() {
        if (comingPhotos.length != 0) {
            // Ensure photos left
            current_photo = comingPhotos.shift();
            $('.overlay').removeClass('hide');
            var $photo4tag = $("<img>");
            $photo4tag.attr("src", current_photo['url_thumbnail']);
            $photo4tag.load(function(){
                $(".photo-to-tag").attr("src", current_photo['url_thumbnail']).fadeTo('slow', 1)
                $('.overlay').addClass('hide');
                $('#photoid').attr("value", current_photo['id']);
            });
            if (comingPhotos.length <= 1) {
                nextPhotoList();
            }
        } else {
            // Next photo list
            nextPhotoList(true);
        }
        console.log(comingPhotos.length);
        return false;
    }

    $('#next-photo').click(function() {
        nextPhoto();
        return false;
    });

    // function nextphoto() {
    //     $.getJSON('/_next4tag', {}, function(data) {
    //         $('.overlay').removeClass('hide');
    //         var photo = jQuery.parseJSON(data.result);
    //         var $photo4tag = $("<img>");
    //         var photo_url = photo.photo_url + '?imageView2/2/w/600/interlace/1';
            
    //         $photo4tag.attr("src", photo_url);
    //         $photo4tag.load(function(){
    //             $(".photo-to-tag").attr("src", photo_url).fadeTo('slow', 1)
    //             $('.overlay').addClass('hide');
    //             $('#photoid').attr("value", photo.photo_id);
    //         });
    //     });
    //     return false;
    // }

    function submittags() {
        var tags = $('#tags').val();

        $('.overlay').removeClass('hide');
        
        var $this = $(this).off("click", submittags);
        $.ajax({
            url: '/tagit',
            data: { "photoid": $('#photoid').val(), "tags": tags },
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                $('#label-contributes-count').text(response.count);
                nextPhoto();
                $('#tags').tagsinput('removeAll');
                $this.click(submittags);
            },
            error: function(error) {
                console.log(error);
                $this.click(submittags);
            }
        });
    }

    $('#submit-tags').click(submittags);


    function submitcats() {
        var cats = []
        $('input:checkbox').each(function(){
            if ($(this).attr('role') == 'category' && $(this).is(':checked')) {
                cats.push($(this).val());
            }
        });
        var $this = $(this).off("click", submitcats);
        $.ajax({
            url: '/catit',
            data: { "photoid": $('#photoid').val(), "cats": cats.toString()},
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                nextPhoto();
                $this.click(submitcats);
            },
            error: function(error) {
                console.log(error);
                $this.click(submitcats);
            }
        });
    }

    $('#submit-cats').click(submitcats);

    $('<div class="bootstrap-tagsinput"></div>').keydown(function() {
        alert("Handler for keydown");
    });

        // var tags = $('#tags').val();

        // $('#submit-label').addClass('hide');
        // $('#submit-loading').removeClass('hide');
        // $('#submit-tags').unbind("click");
        // console.log("unbind click");
        // $('#submit-tags').bind("click");
        // console.log("bind click");
        // $.ajax({
        //     url: '/tagit',
        //     data: { "photoid": $('#photoid').val(), "tags": tags },
        //     type: 'POST',
        //     success: function(response) {
        //         $('#tags').tagsinput('removeAll');
        //         nextphoto();
        //         console.log(response);
        //     },
        //     error: function(error) {
        //         console.log(error);
        //     }
        // });
    // });

});