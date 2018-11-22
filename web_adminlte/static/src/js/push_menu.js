$(function () {
    'use strict';

    $('[data-toggle="control-sidebar"]').controlSidebar(); // 切换控制面板

    // $('[data-toggle="push-menu"]').pushMenu(); // 切换菜单

    var mySkins = [
        'skin-blue',
        'skin-black',
        'skin-red',
        'skin-yellow',
        'skin-purple',
        'skin-green',
        'skin-blue-light',
        'skin-black-light',
        'skin-red-light',
        'skin-yellow-light',
        'skin-purple-light',
        'skin-green-light'
    ];

    function get(name) {
        if (typeof (Storage) !== 'undefined') {
            return localStorage.getItem(name)
        } else {
            window.alert('Please use a modern browser to properly view this template!')
        }
    }

    function store(name, val) {
        if (typeof (Storage) !== 'undefined') {
            localStorage.setItem(name, val)
        } else {
            window.alert('Please use a modern browser to properly view this template!')
        }
    }

    function changeSkin(cls) {
        $.each(mySkins, function (i) {
            $('body').removeClass(mySkins[i])
        });

        $('body').addClass(cls);
        store('skin', cls);
        return false
    }

    function setup() {
        var tmp = get('skin');
        if (tmp && $.inArray(tmp, mySkins))
            changeSkin(tmp);

        // Add the change skin listener
        $('[data-skin]').on('click', function (e) {
            if ($(this).hasClass('knob'))
                return;
            e.preventDefault();
            changeSkin($(this).data('skin'))
        })
    }

    setup()
});
