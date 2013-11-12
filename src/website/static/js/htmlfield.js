django.jQuery(function() {
    tinymce.init({
        selector:'textarea.wysiwyg',
        script_url : '/static/tinymce/tinymce.min.js',
        directionality : 'rtl',
        language : 'he_IL',
        menubar : false,
        toolbar_items_size : 'small',
//            content_css : "/static/m/tinymce.css",
        toolbar : "numlist bullist indent outdent blockquote | alignjustify alignright aligncenter alignleft | underline italic bold | preview fullscreen code | ltr rtl",
        plugins: ['directionality', 'fullscreen', 'code', 'preview'],
        height: 300
    });
});
