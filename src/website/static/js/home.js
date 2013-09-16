"use strict";

$(function() {
    var things = $('.things span');

    function cycle() {
        var i = things.filter('.active').index();
        things.removeClass('active').eq((i + 1) % things.length).addClass('active');

    }

    setInterval(cycle, 3000);

});
