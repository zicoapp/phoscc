jQuery(document).ready(function() {

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
        $.getJSON('/_next4cat', {}, function(data) {
            console.log(data.result);
            var plist = jQuery.parseJSON(data.result);
            plist.shift();
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
            if (comingPhotos.length == 0) {
                nextPhotoList();
            }
        } else {
            // Next photo list
            nextPhotoList(true);
        }
        console.log(comingPhotos.length);
        return false;
    }

    function submitcats() {
        $('.overlay').removeClass('hide');
        $(this).blur();
        var cats = [];
        $('input:checkbox').each(function(){
            if ($(this).attr('role') == 'category' && $(this).is(':checked')) {
                cats.push($(this).val());
            }
        });
        var $this = $(this).off("click", submitcats);
        $.ajax({
            url: '/catit',
            data: { "photoid": $('#photoid').val(), "cats": cats.toString() },
            type: 'POST',
            dataType: 'json',
            success: function(response) {
                $('#label-categorized-count').text(response.count);
                $('input:checkbox').each(function(){
                    $(this).prop('checked', false);
                });
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

});