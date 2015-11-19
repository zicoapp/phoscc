
(function () {
    "use strict";
    $( "#search" ).focus(function() {
	  $( ".mask" ).fadeTo( "slow" , 0.55, null);
	});
	$( "#search" ).focusout(function() {
	  $( ".mask" ).fadeTo( "slow" , 0.2, null);
	});
})();

