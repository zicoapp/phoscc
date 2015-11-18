
// $('.bootstrap-tagsinput').change(function() {
// 	$(this).find('input').val('');
// })

jQuery(document).ready(function() {
	$('#testing').click(function() {
		alert($(".tagsinput-gen").val());
	});

	$('#next-photo').click(function() {
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

            // var $downloadingImage = $("<img>");
            // $downloadingImage.load(function(){
            //   $("#index-cover").css({ 'background-image': 'url(' +  photo.cover  + ')' }).fadeTo('slow', 1)
            //   $("a#cover-download").attr('href', photo.original);
            //   $("#cover-loading").addClass('hide');
            // });
            // $("a#next-cover").blur();
            // $downloadingImage.attr("src", photo.cover);
        });
        return false;
	});
});