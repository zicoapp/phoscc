
// $(window).load(function () {
//     $(document).ready(function(){

//     });
// });

jQuery(document).ready(function() {
    jQuery(".collage").justifiedGallery({
        rowHeight: 200,
        fixedHeight: false,
        maxRowHeight: '120%',
        margins: 7,
        lastRow: 'nojustify',
        captionSettings: {
        	animationDuration: 500, 
        	visibleOpacity: 1,
        	nonVisibleOpacity: 0.0
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