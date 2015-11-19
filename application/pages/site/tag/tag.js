
// $('.bootstrap-tagsinput').change(function() {
// 	$(this).find('input').val('');
// })

jQuery(document).ready(function() {
	$('#testing').click(function() {
		alert($(".tagsinput-gen").val());
	});

    function nextphoto() {
        $.getJSON('/_next4tag', {}, function(data) {
            $('.overlay').removeClass('hide');
            var photo = jQuery.parseJSON(data.result);
            var $photo4tag = $("<img>");
            var photo_url = photo.photo_url + '?imageView2/2/w/600/interlace/1';
            
            $photo4tag.attr("src", photo_url);
            $photo4tag.load(function(){
                $(".photo-to-tag").attr("src", photo_url).fadeTo('slow', 1)
                $('.overlay').addClass('hide');
                $('#photoid').attr("value", photo.photo_id);
            });
        });
        return false;
    }

    function submittags() {
        var tags = $('#tags').val();

        // $('#submit-label').addClass('hide');
        // $('#submit-loading').removeClass('hide');
        $('.overlay').removeClass('hide');
        
        var $this = $(this).off("click", submittags);
        $.ajax({
            url: '/tagit',
            data: { "photoid": $('#photoid').val(), "tags": tags },
            type: 'POST',
            success: function(response) {
                $('#tags').tagsinput('removeAll');
                nextphoto();
                console.log(response);
                $this.click(submittags);
            },
            error: function(error) {
                console.log(error);
                $this.click(submittags);
            }
        });
    }

    $('#submit-tags').click(submittags);
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

	$('#next-photo').click(function() {
		return nextphoto();
	});

});